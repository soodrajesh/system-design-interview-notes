import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from lanes import build

lanes = [
 {"name": "UPLOAD PATH", "color": "#1a73e8",
  "nodes": [("TikTok app", "user", "actor", "creator"),
            ("Load balancer", "lb", "network", ""),
            ("Upload service", "run", "compute", "microservice"),
            ("Blob storage", "bucket", "data", "S3 · tiered to cold\nregional replicas"),
            ("Metadata store", "db", "data", "DynamoDB (key-value)\nid · url · likes · features")],
  "edges": [(0, "upload video", "Creator uploads a finished ~1 MB, 10 s, 1080x1920 clip"),
            (1, "", "Load balancer routes to an upload-service instance (separate from the feed service)"),
            (2, "raw + encodings", "Video bytes go to blob storage; optional async re-encodes per device type get their own URLs"),
            (3, "register video", "Metadata row written (video id, URL, creator, timestamp, likes, duration, algorithm features)")]},
 {"name": "FEED / STREAM PATH  ·  'For You'", "color": "#00897b",
  "nodes": [("TikTok app", "user", "actor", "reads ahead 10-20 videos"),
            ("App service", "run", "compute", "feed API"),
            ("'For You'\ngenerator", "sparkle", "ai", "ML ranking +\nrule-based exclusions"),
            ("Metadata store", "db", "data", "video info by id"),
            ("User store", "db", "data", "RDS / Spanner\nprofile · follows · history")],
  "edges": [(0, "what's next?", "App constantly asks for the next batch of videos (read-ahead) so playback has no spinner"),
            (1, "rank for user", "App service asks the generator which videos suit this user"),
            (2, "video ids", "Generator returns video ids, using the user's features/profile and per-video algorithm features"),
            (3, "profile", "Exclusion profile (blocked users etc.) is applied so unambiguous rules override the ML output")]},
 {"name": "VIDEO DELIVERY PATH", "color": "#8e44ad",
  "nodes": [("App service", "run", "compute", "returns metadata + URLs"),
            ("TikTok app", "user", "actor", "fetches each URL"),
            ("CDN", "globe", "network", "regional edge caches"),
            ("Blob storage", "bucket", "data", "origin on cache miss")],
  "edges": [(0, "metadata + URLs", "Small structured payload (title, creator, likes, video URLs) comes via the app service"),
            (1, "GET video URL", "Heavy video bytes never go through the app service; the app fetches each URL directly"),
            (2, "cache miss", "CDN serves popular videos from its regional cache, otherwise pulls from blob storage and may cache")]},
]
build(os.path.join(os.path.dirname(__file__), "architecture.svg"), "Design TikTok",
      "Back-end for video upload and streaming · blob + NoSQL + SQL split · ML-generated feed · CDN", lanes,
      notes=["1B users in 150 countries, 1B views/day, 10B uploads/yr ≈ 30M/day ≈ 300/s (≈1k/s peak ≈ 10 Gbps ingress)",
             "Storage: 10B × 1 MB = 10 PB/yr raw, ≈100 PB/yr with replication and encodings; metadata ≈ 10 TB; views ≈ 10k/s ≈ 100 Gbps egress",
             "Success metric: time in app (~1 h/day). Bottleneck: real-time feed generation → read-ahead, possibly run model on-device"])
