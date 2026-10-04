import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from lanes import build

lanes = [
 {"name": "SEND PATH  ·  synchronous", "color": "#1a73e8",
  "nodes": [("Sender app", "user", "actor", "iOS · Android"),
            ("Load balancer", "lb", "network", "round robin /\nleast loaded"),
            ("API servers", "run", "compute", "~100 · auto-scaled\nstateless"),
            ("Hash ring", "policy", "network", "user id → partition"),
            ("NoSQL store", "db", "data", "DynamoDB\nmessages + users")],
  "edges": [(0, "POST /messages/v1", "Sender calls POST /messages/v1 {sender_id, recipient_id, text}; auth token in header"),
            (1, "", "Load balancer spreads requests over stateless API servers"),
            (2, "partition by id", "API server maps the user id to a partition with consistent hashing (built into DynamoDB)"),
            (3, "write", "Row written: message_id, sender, recipient, timestamp, status = undelivered. Returns 200 immediately")]},
 {"name": "DELIVERY PATH  ·  asynchronous (eventual consistency)", "color": "#F29900",
  "nodes": [("NoSQL store", "db", "data", "undelivered messages"),
            ("Message\ndistributor", "bolt", "compute", "partitioned workers"),
            ("NoSQL store", "db", "data", "recipient unread-id list"),
            ("Recipient app", "user", "actor", "check → read → mark read")],
  "edges": [(0, "scan status", "Distributor loops over messages whose status is undelivered (partitioned across the user space)"),
            (1, "add unread id", "For each one, appends the message id to the recipient's unread list and flips status to delivered"),
            (2, "GET unread ids", "Recipient app calls check-messages: a fast key+column query returns unread ids; read-message then fetches the body and moves the id to read")]},
]
build(os.path.join(os.path.dirname(__file__), "architecture.svg"), "Design WhatsApp / Telegram",
      "1:1 text messaging · NoSQL store · asynchronous message distributor", lanes,
      notes=["Scale: 10B msgs/day ≈ 100k/s, peak ≈ 500k/s, doubling in a year; ~1 TB/day (100 B/msg)",
             "NoSQL (DynamoDB) over SQL: a petabyte in 3 years does not fit one relational box; eventual consistency is acceptable",
             "Bottleneck: the distributor scanning an ever-growing table; split delivered / undelivered tables and shard the distributors"],
      boundary=None)
