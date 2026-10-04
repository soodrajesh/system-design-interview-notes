import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from lanes import build

lanes = [
 {"name": "REQUEST CHECK  ·  at the edge, before any app server", "color": "#1a73e8",
  "nodes": [("Client", "user", "actor", "user id · IP · API key"),
            ("API gateway /\nrate limiter", "lb", "network", "identify client, pick rules,\nreturn 429 + headers"),
            ("Redis Cluster", "db", "data", "token bucket per client\n(tokens, last_refill)\nsharded by hash of client id"),
            ("App servers", "run", "compute", "never see blocked traffic")],
  "edges": [(0, "request", "Request arrives with identity in headers (JWT user id, X-Forwarded-For IP, X-API-Key)"),
            (1, "Lua script", "Gateway sends one atomic Lua script: refill by elapsed time, test, decrement, set EXPIRE"),
            (2, "allowed", "Allowed requests are forwarded; rejected ones get HTTP 429 + X-RateLimit-Limit / -Remaining / -Reset and Retry-After")]},
 {"name": "AVAILABILITY + CONFIG", "color": "#d93025",
  "nodes": [("Redis primary\n(shard)", "db", "data", "one of ~10+ shards\n~100k checks/s each"),
            ("Replica", "db", "data", "auto-promoted on failure\n(Redis Cluster)"),
            ("Failure policy", "shield", "security", "fail-closed chosen: viral spikes\nshouldn't flood the backend"),
            ("Rules store", "policy", "ops", "per-user · per-IP · global ·\nper-endpoint limits"),
            ("Gateways", "lb", "network", "poll every ~30 s, or push\nvia ZooKeeper")],
  "edges": [(0, "replicate", "Each shard has one or more replicas; replication lag is small"),
            (1, "on outage", "If a shard is unreachable the gateway needs a policy: fail-open (availability, risk of cascade) or fail-closed"),
            (2, "monitor", "Alert on Redis CPU/memory/connectivity and on entering fail-open mode"),
            (3, "update rules", "Rules are changed without deploys; push is faster for emergencies, polling is simpler")]},
]
build(os.path.join(os.path.dirname(__file__), "architecture.svg"), "Design a distributed rate limiter",
      "API-gateway placement · token bucket in Redis (atomic Lua) · sharded by client id · 1M req/s", lanes,
      notes=["Scale: 1M requests/s, 100M DAU, < 10 ms overhead per check; eventual consistency across nodes is acceptable",
             "Algorithms: fixed window (boundary bursts), sliding window log (exact but memory-heavy), sliding window counter (cheap approximation), token bucket (bursts + steady rate): chosen",
             "Hot keys: client-side limiting, blocklists for abusers, DDoS protection upstream; connection pooling and regional deployments for latency"])
