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

Metrics (one row each; "per" columns compare with the 7 days before):
  1 visits (Cloudflare, page views and unique visitors)    5 Sprint purchases (paid enrolments)
  2 new free accounts                                      6 revenue (by currency, minor units -> major)
  3 active learners (accounts with any practice)           7 refunds and cancellations
  4 practice actions (speak, game, shadow, lesson)         8 waitlist sign-ups and Sprint places left
The operating-system doc names eight weekly metrics in its section 8; this script could not read that doc from the
session that wrote it, so check the list against it and adjust the queries here.
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


def window(start, end):
    a, b = int(start.timestamp()), int(end.timestamp())
    m = {}
    def get(name, fn):
        try: m[name] = fn()
        except Exception as e: m[name] = 'not available: ' + str(e).splitlines()[0][:160]
    one = lambda sql: d1(sql)[0]
    get('1 visits', lambda: visits(start, end))
    get('2 new accounts', lambda: one(f"SELECT COUNT(*) AS n FROM users WHERE role = 'student' AND created_at >= {a} AND created_at < {b}")['n'])
    da, db = start.date().isoformat(), end.date().isoformat()
    get('3 active learners', lambda: one(f"SELECT COUNT(DISTINCT user_id) AS n FROM usage WHERE day >= '{da}' AND day < '{db}'")['n'])
    get('4 practice actions', lambda: {r['kind']: r['n'] for r in d1(f"SELECT kind, SUM(n) AS n FROM usage WHERE day >= '{da}' AND day < '{db}' GROUP BY kind")})
    get('5 Sprint purchases', lambda: one(f"SELECT COUNT(*) AS n FROM enrollments WHERE status = 'paid' AND paid_at >= {a} AND paid_at < {b}")['n'])
    get('6 revenue', lambda: {r['currency'] or '?': r['total'] / 100 for r in d1(f"SELECT currency, SUM(amount) AS total FROM enrollments WHERE status IN ('paid', 'refunded') AND paid_at >= {a} AND paid_at < {b} GROUP BY currency")})
    get('7 refunds and cancellations', lambda: {r['status']: r['n'] for r in d1(f"SELECT status, COUNT(*) AS n FROM enrollments WHERE status IN ('refunded', 'cancelled') AND created_at < {b} GROUP BY status")})
    get('8 waitlist sign-ups', lambda: one(f"SELECT COUNT(*) AS n FROM waitlist WHERE created_at >= {a} AND created_at < {b}")['n'])
    if os.environ.get('STRIPE_READ_KEY'):
        get('Stripe: paid checkouts', lambda: sum(1 for s in stripe(f'checkout/sessions?limit=100&created[gte]={a}&created[lt]={b}')['data'] if s.get('payment_status') == 'paid'))
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--end', help='last day to include, YYYY-MM-DD (UTC); default: now')
    ap.add_argument('--md', action='store_true', help='print a Markdown table instead of JSON')
    o = ap.parse_args()
    end = (dt.datetime.fromisoformat(o.end) + dt.timedelta(days=1)) if o.end else dt.datetime.utcnow()
    end = end.replace(tzinfo=dt.timezone.utc)
    start, prev = end - dt.timedelta(days=7), end - dt.timedelta(days=14)
    this, last = window(start, end), window(prev, start)
    if not o.md:
        print(json.dumps({'from': start.isoformat(), 'to': end.isoformat(), 'this_week': this, 'week_before': last}, indent=1, default=str)); return
    print(f"\n## Week to {(end - dt.timedelta(seconds=1)).date()} (UTC)\n\n| Metric | This week | Week before |\n| --- | --- | --- |")
    fmt = lambda v: json.dumps(v, ensure_ascii=False).replace('|', '/') if not isinstance(v, (int, float, str)) else str(v)
    for k in this: print(f'| {k} | {fmt(this[k])} | {fmt(last.get(k, ""))} |')
    print('\nSource: ops/weekly_metrics.py (read-only). Unique visitors are summed per day, so one person on two days counts twice.')


if __name__ == '__main__':
    sys.exit(main())
