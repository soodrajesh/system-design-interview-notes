import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from lanes import build

lanes = [
 {"name": "FIND MUSIC  ·  metadata only", "color": "#1a73e8",
  "nodes": [("Spotify app", "user", "actor", "search / filters"),
            ("Load balancer", "lb", "network", "bandwidth-aware"),
            ("Web servers", "run", "compute", "stateless"),
            ("Metadata DB", "db", "data", "RDS / MySQL\nsongs · users · artists")],
  "edges": [(0, "find music", "User searches by artist / genre; app sends a find-music request"),
            (1, "", "Load balancer picks a web server (balanced on network bandwidth / open streams, not just CPU)"),
            (2, "SQL query", "Web server runs a relational query (genre, artist) and returns ~100 song rows; the MP3 store is never touched")]},
 {"name": "PLAY SONG  ·  first request", "color": "#00897b",
  "nodes": [("Spotify app", "user", "actor", "tap play"),
            ("Web servers", "run", "compute", "in-memory song cache"),
            ("Metadata DB", "db", "data", "song id → audio link"),
            ("Audio store", "bucket", "data", "S3 · ~5 MB MP3s\n3x replicated"),
            ("Spotify app", "user", "actor", "local song cache")],
  "edges": [(0, "play(song id)", "App asks the web server to play a song id"),
            (1, "lookup link", "Server looks up the audio link in the metadata DB"),
            (2, "fetch MP3", "Server reads the whole ~5 MB file from S3 into memory (small enough, avoids streaming lag from the DB)"),
            (3, "stream chunks", "Server streams chunks to the app; frequently played songs are cached on the phone")]},
 {"name": "HOT SONG  ·  new release spike", "color": "#8e44ad",
  "nodes": [("Web servers", "run", "compute", "heat map of requests"),
            ("CDN", "globe", "network", "edge song cache\n(CloudFront)"),
            ("Audio store", "bucket", "data", "origin"),
            ("Spotify app", "user", "actor", "redirected to edge")],
  "edges": [(0, "hot → push", "Web servers track recent request counts; when a song gets hot they tell the CDN to pull it"),
            (1, "pull from origin", "CDN fetches the file from S3 once instead of 10M origin reads"),
            (2, "serve from edge", "Later requests get a redirect (or a CDN check) and stream from the nearest edge, cutting load on web servers and S3")]},
]
build(os.path.join(os.path.dirname(__file__), "architecture.svg"), "Design Spotify",
      "Find and play music · metadata vs audio split · multi-layer caching", lanes,
      notes=["1B users, 100M songs, ~5 MB/song → ~500 TB raw, ~1.5 PB with 3x replication; metadata only ~10-100 GB, user data ~1 TB",
             "Two stores because access patterns differ: immutable blobs (S3) vs queried/updated rows (RDS)",
             "Cache layers: phone → CDN edge → web-server memory → S3. Geo-aware replication keeps regional music near its listeners"])
