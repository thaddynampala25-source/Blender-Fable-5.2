-- Anonymous practice counts (metric 3, "visitors who practise").
-- One number per day and kind: how many browsers started that kind of practice that day.
-- No user id, no IP, no cookie, no device id: a browser remembers on its own device that it has already counted today.
CREATE TABLE IF NOT EXISTS practice_daily (
  day TEXT NOT NULL,          -- YYYY-MM-DD (UTC)
  kind TEXT NOT NULL,         -- speak | game | shadow | lesson | any
  n INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (day, kind)
);
