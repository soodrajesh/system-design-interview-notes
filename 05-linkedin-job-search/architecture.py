import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from lanes import build

lanes = [
 {"name": "SEARCH PATH  ·  job seeker (GET /jobs/search)", "color": "#1a73e8",
  "nodes": [("Job seeker", "user", "actor", "location · role · org"),
            ("API gateway", "lb", "network", "auth · rate limit\nload balancing"),
            ("Search jobs\nservice", "run", "compute", "find → rank → decorate"),
            ("Profile cache", "bolt", "ops", "~50 GB · 15-30 min TTL"),
            ("Elasticsearch", "db", "data", "active jobs: id · location\nrole · org tags (+ hot-key cache)")],
  "edges": [(0, "search + filters", "Seeker calls GET search-jobs with optional filters (location, role, org); token identifies the user; results paginated"),
            (1, "", "Gateway authenticates (token / client id), throttles abusive callers, spreads load"),
            (2, "profile lookup", "If filters are missing, the service loads the user's profile (cached; changes rarely)"),
            (3, "query", "Query Elasticsearch on the searchable tags to get candidate job ids (~10M active jobs)")]},
 {"name": "RANK + DECORATE", "color": "#F29900",
  "nodes": [("Search jobs\nservice", "run", "compute", "candidate job ids"),
            ("Ranking\nservice", "chart", "compute", "fallback: posted date /\nclick count"),
            ("Personalization\n(LLM / ML)", "sparkle", "ai", "scores per job from\nclicks · views · applies"),
            ("Jobs store", "db", "data", "DynamoDB · full job\napply link · images · status"),
            ("Job seeker", "user", "actor", "ranked page of jobs")],
  "edges": [(0, "candidates", "Candidate ids go to the ranking service"),
            (1, "score", "Ranking asks the personalization model for a relevance score per job (applying to a company is a strong signal, a view a weak one)"),
            (2, "top-N ids", "If personalization fails, ranking degrades to simple rules (newest first) instead of failing the request"),
            (3, "decorate", "Service fetches full job details by id from the NoSQL jobs store and returns the ranked page")]},
 {"name": "EMPLOYER WRITE PATH  ·  keeps search index in sync", "color": "#00897b",
  "nodes": [("Employer", "user", "actor", "create · update · delete"),
            ("Job manager\nservice", "run", "compute", "CRUD"),
            ("Jobs store", "db", "data", "DynamoDB · source of truth\nall fields, any status"),
            ("Elasticsearch", "db", "data", "only ACTIVE jobs,\nonly searchable fields")],
  "edges": [(0, "post job", "Employer posts, edits or closes a job"),
            (1, "write", "Job manager persists the complete record"),
            (2, "sync", "Active jobs are synced to the search index; expired or deleted jobs are removed (low write rate vs. very high read rate)")]},
]
build(os.path.join(os.path.dirname(__file__), "architecture.svg"), "Design LinkedIn (job search)",
      "Job seeker search · Elasticsearch for retrieval · NoSQL for detail · ML ranking with graceful fallback", lanes,
      notes=["Scale: 100M DAU, ~40% (40M) search jobs, ~4 searches each; 10M active jobs; target <200 ms backend, <1 s perceived",
             "Eventual consistency is fine: a brand-new posting appearing in the next result set is acceptable",
             "Availability: replicas, multi-AZ, region-local data stores for GDPR; degrade ranking rather than fail"])
