import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from lanes import build

lanes = [
 {"name": "REQUEST ROUTING  ·  per-city shard (cloud region / own network)", "color": "#1a73e8",
  "nodes": [("Rider / Driver\napp", "user", "actor", "GPS + persistent\nconnection"),
            ("Load balancer\ncluster", "lb", "network", "enters private network\nearly · TLS"),
            ("City router", "globe", "network", "location → city shard\n(GDPR: data stays in region)"),
            ("City cluster\n(e.g. Berlin)", "run", "compute", "write path + read path\n+ ride-data path")],
  "edges": [(0, "HTTPS / WebSocket", "Phone sends its GPS location; a long-lived connection carries location beacons (the coach's missing piece)"),
            (1, "", "Load balancer pulls traffic onto the company's own low-latency network, spreads load, survives node loss"),
            (2, "route by city", "Request metadata (location) selects the city's shard; each city has its own servers and data boundary")]},
 {"name": "INSIDE A CITY  ·  three differently-scaled paths", "color": "#00897b",
  "nodes": [("Read path\nfleet", "run", "compute", "snapshot of available cars\neventually consistent · 5-100 nodes"),
            ("Ride-data path\n(per-ride)", "pipeline", "compute", "location beacons / 5 s\nsharded by ride id · 10k+ QPS"),
            ("Write path\n(source of truth)", "shield", "security", "ride state machine\nsynchronised · <1k writes/s"),
            ("Consensus group", "key", "data", "3 or 5 nodes · leader election\none driver ↔ one rider")],
  "edges": [(0, "feed of updates", "Read replicas subscribe to a feed of fleet state: stale by seconds is fine for 'cars near me'"),
            (1, "ride events", "Ride-specific data (share-my-ride link, live position) never conflicts across rides, so it shards freely"),
            (2, "replicate (Raft/Paxos)", "Mutations (request, accept, cancel, start, end, tip) go through one logical authority replicated for durability")]},
 {"name": "MATCHING  ·  life of a ride", "color": "#F29900",
  "nodes": [("Rider\nrequests", "user", "actor", "pickup · dropoff · car type\n· party size"),
            ("Instant-book\ndrivers", "bolt", "compute", "auto-accept; 4 s to refuse"),
            ("Nearest driver\nselector", "chart", "compute", "one driver at a time\n7 s to accept, else next"),
            ("Pickup mode", "pod", "compute", "live GPS · cancel allowed\n· PIN/QR confirmation"),
            ("In-ride", "money", "ops", "trip → payment → rating,\ntip")],
  "edges": [(0, "request", "Rider requests a ride; the system looks for a driver instead of broadcasting"),
            (1, "else", "Drivers with instant-book get priority and 4 s to say no"),
            (2, "accepted", "Otherwise offer to the best nearby driver exclusively for ~7 s, then the next, so drivers never race each other"),
            (3, "confirmed", "Confirmed by GPS, driver confirmation or rider code. After this the trip runs and ends with payment and ratings")]},
]
build(os.path.join(os.path.dirname(__file__), "architecture.svg"), "Design Uber",
      "Two-sided marketplace · per-city sharding · read path vs write path vs ride-data path · exclusive driver offers", lanes,
      notes=["Objective: keep drivers busy (supply is the scarce side); price is platform-set (surge), not bid by riders",
             "Invariant: a driver can never accept two riders. Mutating requests per city are <1k/s, so one consensus group can own them",
             "Intentionally skipped: database choice, maps/routing (use a third party), regulation, Uber Eats"])
