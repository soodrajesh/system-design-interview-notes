import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from lanes import build

lanes = [
 {"name": "INPUTS  ·  existing carrier systems (taken as given)", "color": "#5f6368",
  "nodes": [("Call control\nframework", "pipeline", "dev", "places & handles calls"),
            ("Call records DB", "db", "data", "from · to · start · duration\nsharded by phone number"),
            ("Customer mgmt /\nplan system", "user", "actor", "enrols customers,\nsets plans & numbers"),
            ("Customer DB", "db", "data", "name · address · plan · lines")],
  "edges": [(0, "writes CDRs", "Every call produces a record (from number, to number, start, duration) in the call records DB"),
            (2, "writes profile", "Customer management populates the customer DB; billing only reads both (arrows show information flow)")]},
 {"name": "BILL GENERATION  ·  batch, 24 h SLA after cycle end", "color": "#1a73e8",
  "nodes": [("Orchestrator", "chart", "ops", "finds customers whose\ncycle ended · sizes workload"),
            ("Bill queue", "bolt", "compute", "bills to generate\nthis day"),
            ("Billing workers\n(elastic)", "run", "compute", "read both DBs, apply\nplan rules, rate calls"),
            ("Billing DB", "db", "data", "NoSQL document store\none bill document / cycle")],
  "edges": [(0, "enqueue", "Periodic job scans the customer DB for billing cycles that ended; staggered cycles smooth the load"),
            (1, "pull", "Workers take jobs from the queue; the orchestrator scales workers up or down with queue depth"),
            (2, "bill document", "Each worker reads the customer's ~300 calls for the period (shard found from phone number) plus the plan, then writes one bill document per customer per cycle; history kept indefinitely")]},
 {"name": "DELIVERY", "color": "#00897b",
  "nodes": [("Billing DB", "db", "data", "bill documents"),
            ("Customer billing\nportal", "globe", "network", "only public surface\nreverse proxy · WAF"),
            ("Bill generation\nservice", "pipeline", "dev", "PDF · email · printed mail"),
            ("Customer", "user", "actor", "views / pays bill")],
  "edges": [(0, "read", "Portal reads bill documents; payment itself is out of scope"),
            (1, "", "Bill-generation service renders each bill as PDF / email / physical mail"),
            (2, "deliver", "Customer receives and pays; paid-state can be written back to the customer DB")]},
]
build(os.path.join(os.path.dirname(__file__), "architecture.svg"), "Design a phone company billing system",
      "Batch pipeline · shard call records by phone number · queue + elastic workers · document-store output", lanes,
      notes=["Scale: 50M subscribers × 10 billable calls/day = 500M calls/day ≈ 15B/month; 50M bills/month; bills ready within 24 h of cycle end",
             "Sharding: by phone number (area code / exchange, merged for sparse areas), or hash the whole number where no geography exists (e.g. UK)",
             "Availability: ≥2 copies per shard, redundant orchestrators/workers, no single point of failure; security: internal-only network, encryption at rest, hardened portal"])
