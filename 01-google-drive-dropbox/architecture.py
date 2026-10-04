import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from archlib import Diagram

W, H = 1250, 1030
d = Diagram(W, H, "Design Google Drive / Dropbox", "File sync: pre-signed S3 transfers, relational metadata, pub/sub notifications, CDN reads")

d.group(240, 150, 560, 350, "Region (replicable: NA / EU / APAC)", "#1a73e8", dash=False, fill="#f8faff", label_w=290)

d.node("ca", 90, 230, "Client A", "user", "actor", "desktop · mobile · web")
d.node("lb", 290, 230, "Load balancer", "lb", "network", "ELB")
d.node("api", 480, 230, "API servers", "run", "compute", "stateless · auth\nupload/download/revisions")
d.node("rds", 690, 230, "Metadata DB", "db", "data", "MySQL (RDS)\nprimary + replicas")
d.node("sns", 690, 420, "Pub/Sub", "bolt", "compute", "SNS · per-user topic")
d.node("s3", 960, 420, "Object storage", "bucket", "data", "S3 · multipart\nresumable · versioning")
d.node("cdn", 480, 620, "CDN", "globe", "network", "edge cache")
d.node("cb", 90, 620, "Client B", "user", "actor", "second device")

d.edge("ca", "lb", "h", num=1, label="POST /upload")
d.edge("lb", "api", "h")
d.path([(480, 200), (480, 122), (110, 122), (110, 200)], num=2, label="pre-signed URL", lab_at=(300, 122))
d.path([(70, 200), (70, 100), (1130, 100), (1130, 420), (990, 420)], num=3, label="direct multipart upload (bytes never touch API servers)", lab_at=(700, 100), color="#00897b")
d.edge("api", "rds", "h", num=4, label="file + version row")
d.path([(510, 250), (580, 250), (580, 360), (690, 360), (690, 390)], num=5, label="publish change", lab_at=(580, 335))
d.path([(660, 420), (90, 420), (90, 590)], num=6, label="push: new version", lab_at=(380, 420), color="#F29900")
d.path([(120, 620), (215, 620), (215, 250), (260, 250)], num=7, label="GET /download", lab_at=(215, 520))
d.edge("cb", "cdn", "h", num=8, label="302 → signed URL")
d.path([(510, 620), (870, 620), (870, 420), (930, 420)], num=9, label="cache miss → origin", lab_at=(700, 620))

d.legend(34, 700, "Flow", [
 ("1", "Client calls POST /upload (file metadata) through the load balancer"),
 ("2", "API authenticates, returns a short-lived pre-signed S3 URL (multipart, resumable)"),
 ("3", "Client compresses/encrypts locally and uploads straight to S3, bypassing API servers"),
 ("4", "On completion client confirms; API commits file + file_version rows (strong consistency)"),
 ("5", "API publishes a change event to the pub/sub notification service"),
 ("6", "Other devices of the same user are notified and learn a new version exists"),
 ("7", "Device B calls GET /download/{id}; API returns a redirect, not the bytes"),
 ("8", "Client follows the temporary signed URL to the CDN"),
 ("9", "CDN serves from edge, or fetches from S3 on a miss and caches it"),
], w=760)
d.key(34, 975)
if __name__ == "__main__":
    d.save(os.path.join(os.path.dirname(__file__), "architecture.svg"))
