#!/usr/bin/env python3
"""Week2Speak weekly numbers. Read-only: it never writes to D1, Stripe or Cloudflare.

    python3 ops/weekly_metrics.py                 # the last 7 days up to now (UTC)
    python3 ops/weekly_metrics.py --end 2026-11-30 --md >> ops/metrics.md

Sources and what each needs (a missing one prints "not available" and the rest still run):
  D1 (accounts, usage, enrolments, waitlist)  `npx wrangler@4 d1 execute week2speak --remote`, needs
      CLOUDFLARE_API_TOKEN (D1 read) and CLOUDFLARE_ACCOUNT_ID. Only aggregate COUNT/SUM queries: no emails or names.
  Cloudflare visits                          GraphQL Analytics API, needs the token to have Zone > Analytics > Read
      for week2speak.com. Server-side counts, no tracker on the site.
  Stripe                                     STRIPE_READ_KEY: a restricted key with read access to Checkout
      Sessions and Charges only. Without it, paid enrolments come from D1 (filled by the webhook).

Metrics: the eight in section 8 of "Week2Speak Operating System: Audit and 7-Day Plan" (20 Nov 2026), each for
the 7 days to --end and the 7 days before:
  1 Link clicks            clicks on the link in bio, per platform: copied by hand from each platform (--clicks)
  2 Site visitors          daily unique visitors and page views (Cloudflare, server-side; includes bots)
  3 Visitors who practise  browsers that practised, per day (anonymous first-party counts; on once COUNT_PRACTICE is "1")
  4 New free accounts      student accounts created, split by "how did you find us"
  5 Activated accounts     new accounts with a game round, scene reply or Imita clip on their sign-up day or the next
                           (usage is stored per day, so "within 24 hours" is read as "same or next day")
  6 Places held and paid   bookings made (pending) and paid in the window, with revenue per currency
  7 Sprint completion      paid students with the Day 7 talk rehearsed (k7_5) or given to Mei (k7_6), out of all paid
  8 Failed payments, errors  bookings left unpaid for 2+ days; Stripe unpaid or expired checkouts (STRIPE_READ_KEY);
                           Worker requests that errored (Cloudflare Workers analytics)
"""
import argparse, datetime as dt, json, os, subprocess, sys, urllib.request

ZONE = 'week2speak.com'
DB = 'week2speak'
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)


def d1(sql):
    """Run one read-only aggregate query on the live D1 and return its rows."""
    head = sql.lstrip().split(None, 1)[0].upper()
    if head not in ('SELECT', 'WITH'): raise ValueError('read-only: SELECT only')
    env = dict(os.environ, WRANGLER_SEND_METRICS='false')
    r = subprocess.run(['npx', '--yes', 'wrangler@4', 'd1', 'execute', DB, '--remote', '--json', '--command', sql],
                       cwd=SITE, env=env, capture_output=True, text=True, timeout=120)
    if r.returncode: raise RuntimeError(r.stderr.strip()[-300:] or r.stdout.strip()[-300:])
    out = json.loads(r.stdout)
    return out[0]['results'] if isinstance(out, list) else out['results']


def cf_graphql(query, variables):
    tok = os.environ.get('CLOUDFLARE_API_TOKEN')
    if not tok: raise RuntimeError('CLOUDFLARE_API_TOKEN not set')
    req = urllib.request.Request('https://api.cloudflare.com/client/v4/graphql', method='POST',
                                 data=json.dumps({'query': query, 'variables': variables}).encode(),
                                 headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as f: out = json.load(f)
    if out.get('errors'): raise RuntimeError('; '.join(e.get('message', '?') for e in out['errors']))
    return out['data']


def zone_id():
    tok = os.environ.get('CLOUDFLARE_API_TOKEN')
    req = urllib.request.Request('https://api.cloudflare.com/client/v4/zones?name=' + ZONE, headers={'Authorization': 'Bearer ' + (tok or '')})
    with urllib.request.urlopen(req, timeout=30) as f: out = json.load(f)
    if not out.get('result'): raise RuntimeError('zone not visible to this token (needs Zone > Zone > Read or Analytics > Read on ' + ZONE + ')')
    return out['result'][0]['id']


def visits(start, end):
    q = '''query($z: String!, $a: Date!, $b: Date!) { viewer { zones(filter: {zoneTag: $z}) {
             httpRequests1dGroups(limit: 31, filter: {date_geq: $a, date_lt: $b}) { sum { pageViews requests } uniq { uniques } dimensions { date } } } } }'''
    rows = cf_graphql(q, {'z': zone_id(), 'a': start.date().isoformat(), 'b': end.date().isoformat()})['viewer']['zones'][0]['httpRequests1dGroups']
    return {'page_views': sum(r['sum']['pageViews'] for r in rows), 'unique_visitors_daily_sum': sum(r['uniq']['uniques'] for r in rows), 'days': len(rows)}


def stripe(path):
    key = os.environ.get('STRIPE_READ_KEY')
    if not key: raise RuntimeError('STRIPE_READ_KEY not set')
    req = urllib.request.Request('https://api.stripe.com/v1/' + path, headers={'Authorization': 'Bearer ' + key})
    with urllib.request.urlopen(req, timeout=30) as f: return json.load(f)


def worker_errors(start, end):
    acc = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
    if not acc: raise RuntimeError('CLOUDFLARE_ACCOUNT_ID not set')
    q = """query($acc: String!, $a: Time!, $b: Time!) { viewer { accounts(filter: {accountTag: $acc}) {
             workersInvocationsAdaptive(limit: 10000, filter: {datetime_geq: $a, datetime_lt: $b, scriptName: "week2speak"}) {
               sum { requests errors } } } } }"""
    rows = cf_graphql(q, {'acc': acc, 'a': start.strftime('%Y-%m-%dT%H:%M:%SZ'), 'b': end.strftime('%Y-%m-%dT%H:%M:%SZ')})['viewer']['accounts'][0]['workersInvocationsAdaptive']
    req = sum(r['sum']['requests'] for r in rows); err = sum(r['sum']['errors'] for r in rows)
    return {'worker_requests': req, 'worker_errors': err}


def window(start, end, clicks=None):
    a, b = int(start.timestamp()), int(end.timestamp())
    m = {}
    def get(name, fn):
        try: m[name] = fn()
        except Exception as e: m[name] = 'not available: ' + str(e).splitlines()[0][:160]
    one = lambda sql: d1(sql)[0]
    da, db = start.date().isoformat(), end.date().isoformat()
    m['1 Link clicks'] = clicks if clicks else 'enter by hand from each platform (--clicks "TikTok=12,Instagram=5")'
    get('2 Site visitors', lambda: visits(start, end))
    def practise():
        rows = d1(f"SELECT kind, SUM(n) AS n FROM practice_daily WHERE day >= '{da}' AND day < '{db}' GROUP BY kind")
        return {r['kind']: r['n'] for r in rows} or 'none counted (COUNT_PRACTICE off, or no practice yet)'
    get('3 Visitors who practise', practise)
    get('4 New free accounts', lambda: {(r['source'] or 'not given'): r['n'] for r in d1(
        f"SELECT source, COUNT(*) AS n FROM users WHERE role = 'student' AND created_at >= {a} AND created_at < {b} GROUP BY source")})
    get('5 Activated accounts', lambda: one(
        f"SELECT COUNT(*) AS n FROM users u WHERE u.role = 'student' AND u.created_at >= {a} AND u.created_at < {b} AND EXISTS "
        f"(SELECT 1 FROM usage g WHERE g.user_id = u.id AND g.kind IN ('game', 'speak', 'shadow') AND g.n > 0 AND "
        f"g.day IN (date(u.created_at, 'unixepoch'), date(u.created_at + 86400, 'unixepoch')))")['n'])
    def places():
        held = one(f"SELECT COUNT(*) AS n FROM enrollments WHERE created_at >= {a} AND created_at < {b}")['n']
        paid = d1(f"SELECT currency, COUNT(*) AS n, SUM(amount) AS total FROM enrollments WHERE status IN ('paid', 'refunded') AND paid_at >= {a} AND paid_at < {b} GROUP BY currency")
        refunds = one(f"SELECT COUNT(*) AS n FROM enrollments WHERE status IN ('refunded', 'cancelled') AND created_at < {b}")['n']
        return {'held': held, 'paid': sum(r['n'] for r in paid), 'revenue': {(r['currency'] or '?'): r['total'] / 100 for r in paid}, 'refunded_or_cancelled_to_date': refunds}
    get('6 Places held and paid', places)
    get('7 Sprint completion', lambda: one(
        "SELECT COUNT(*) AS paid, COALESCE(SUM(CASE WHEN json_extract(p.data, '$.app.sprint.k7_5') OR json_extract(p.data, '$.app.sprint.k7_6') THEN 1 ELSE 0 END), 0) AS finished "
        "FROM enrollments e LEFT JOIN progress p ON p.user_id = e.user_id WHERE e.status = 'paid'"))
    def failures():
        out = {'unpaid_bookings_2d': one(f"SELECT COUNT(*) AS n FROM enrollments WHERE status = 'pending' AND created_at < {b - 2 * 86400} AND created_at >= {a - 2 * 86400}")['n']}
        if os.environ.get('STRIPE_READ_KEY'):
            ss = stripe(f'checkout/sessions?limit=100&created[gte]={a}&created[lt]={b}')['data']
            out['stripe_unpaid_or_expired'] = sum(1 for x in ss if x.get('payment_status') != 'paid')
        else: out['stripe'] = 'not read (no STRIPE_READ_KEY)'
        try: out.update(worker_errors(start, end))
        except Exception as e: out['worker'] = 'not available: ' + str(e).splitlines()[0][:120]
        return out
    get('8 Failed payments and errors', failures)
    get('Also: waitlist sign-ups', lambda: one(f"SELECT COUNT(*) AS n FROM waitlist WHERE created_at >= {a} AND created_at < {b}")['n'])
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--end', help='last day to include, YYYY-MM-DD (UTC); default: now')
    ap.add_argument('--md', action='store_true', help='print a Markdown table instead of JSON')
    ap.add_argument('--clicks', help='link clicks for this week, copied from each platform, e.g. "TikTok=12,Instagram=5"')
    o = ap.parse_args()
    end = (dt.datetime.fromisoformat(o.end) + dt.timedelta(days=1)) if o.end else dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    end = end.replace(tzinfo=dt.timezone.utc)
    start, prev = end - dt.timedelta(days=7), end - dt.timedelta(days=14)
    clicks = dict(x.split('=', 1) for x in o.clicks.split(',')) if o.clicks else None
    this, last = window(start, end, clicks), window(prev, start)
    if not o.md:
        print(json.dumps({'from': start.isoformat(), 'to': end.isoformat(), 'this_week': this, 'week_before': last}, indent=1, default=str)); return
    print(f"\n## Week to {(end - dt.timedelta(seconds=1)).date()} (UTC)\n\n| Metric | This week | Week before |\n| --- | --- | --- |")
    fmt = lambda v: json.dumps(v, ensure_ascii=False).replace('|', '/') if not isinstance(v, (int, float, str)) else str(v)
    for k in this: print(f'| {k} | {fmt(this[k])} | {fmt(last.get(k, ""))} |')
    print('\nSource: ops/weekly_metrics.py (read-only), the eight metrics of section 8 of the operating-system doc. Visitors are Cloudflare'
          ' server-side counts: they include bots, and one person on two days counts twice.')


if __name__ == '__main__':
    sys.exit(main())
