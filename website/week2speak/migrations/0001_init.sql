-- Week2Speak accounts (Cloudflare D1). Apply with: npx wrangler d1 migrations apply week2speak --remote
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  pw_hash TEXT NOT NULL,
  pw_salt TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'student',          -- student | tutor
  country TEXT,
  lang TEXT NOT NULL DEFAULT 'es',
  phone TEXT,
  source TEXT,                                    -- "how did you find us"
  created_at INTEGER NOT NULL,
  last_seen INTEGER
);
CREATE TABLE IF NOT EXISTS sessions (
  id TEXT PRIMARY KEY,                            -- SHA-256 of the cookie token
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at INTEGER NOT NULL,
  expires_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS sessions_user ON sessions(user_id);
CREATE TABLE IF NOT EXISTS usage (
  user_id TEXT NOT NULL,
  day TEXT NOT NULL,                              -- YYYY-MM-DD (UTC)
  kind TEXT NOT NULL,                             -- speak | game | shadow | lesson
  n INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, day, kind)
);
CREATE TABLE IF NOT EXISTS enrollments (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  status TEXT NOT NULL,                           -- pending | paid | cancelled | refunded
  start_date TEXT,                                -- the Monday the Sprint starts
  tier TEXT, currency TEXT, amount INTEGER,       -- amount in minor units (pence, cents)
  created_at INTEGER NOT NULL,
  paid_at INTEGER,
  stripe_session TEXT
);
CREATE TABLE IF NOT EXISTS progress (
  user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  data TEXT NOT NULL,                             -- JSON: Sprint ticks, streak, XP, recordings list
  updated_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS notes (                -- messages from the tutor, shown on the student's Tutor page
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  body TEXT NOT NULL,
  created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS resets (                -- one-time password reset links made by the tutor
  id TEXT PRIMARY KEY,                            -- SHA-256 of the token
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  expires_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS waitlist (
  email TEXT PRIMARY KEY,
  name TEXT,
  country TEXT,
  created_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS throttle (             -- login and sign-up attempts per hashed IP and hour
  key TEXT NOT NULL,
  hour TEXT NOT NULL,
  n INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (key, hour)
);
