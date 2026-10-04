import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from lanes import build

lanes = [
 {"name": "CREATE SHORT URL  ·  rare, write path", "color": "#1a73e8",
  "nodes": [("Client", "user", "actor", "POST /urls\n(long url, alias?, expiry?)"),
            ("API gateway / LB", "lb", "network", "auth · rate limit"),
            ("Write service\n(horizontally scaled)", "run", "compute", "validate · pick code"),
            ("Redis counter", "key", "security", "INCR; each instance leases\n1,000 ids at a time"),
            ("Postgres", "db", "data", "short_code PK (unique) →\nlong_url, expires_at, ...")],
  "edges": [(0, "shorten", "Client submits a long URL, optionally a custom alias and expiry"),
            (1, "", "Routed to any write-service instance"),
            (2, "get id batch", "Counter value (not a hash) guarantees uniqueness; batching avoids a Redis call per URL"),
            (3, "base62 + insert", "Counter is base62-encoded (1B urls = 6 chars) and inserted; the UNIQUE key is the final safety net")]},
 {"name": "REDIRECT  ·  ~1000x more frequent, read path", "color": "#00897b",
  "nodes": [("Browser", "user", "actor", "GET /{short_code}"),
            ("CDN / edge", "globe", "network", "edge function caches\nhot mappings"),
            ("Read service", "run", "compute", "no auth, stateless"),
            ("Redis cache", "bolt", "ops", "code → long url, LRU,\nTTL ≤ expiry"),
            ("Postgres", "db", "data", "primary key lookup (B-tree)\non cache miss")],
  "edges": [(0, "short link", "User clicks the short link"),
            (1, "miss", "Popular codes are answered at the edge, never reaching the origin"),
            (2, "lookup", "Read service checks Redis first"),
            (3, "miss", "On a miss, read the indexed row, then fill the cache; expired rows return 410 Gone, otherwise 302 to the long URL")]},
]
build(os.path.join(os.path.dirname(__file__), "architecture.svg"), "Design a URL shortener (Bit.ly)",
      "Counter + base62 codes · cache-heavy redirects · split read and write services · 302 redirects", lanes,
      notes=["Scale: 1B URLs, 100M DAU × 5 redirects ≈ 5.8k/s average, ~600k/s with a 100x spike allowance; ~100k new URLs/day ≈ 1 write/s",
             "Storage: ~500 B/row × 1B = ~500 GB, fits one modern SSD-backed Postgres (replicate for HA; shard only if needed)",
             "Multi-region: give each region a disjoint counter range. A few skipped counter values after a Redis failover are fine: only uniqueness matters"])
