# System design interview notes

Notes and architecture diagrams from the system design videos on the [IGotAnOffer: Engineering](https://www.youtube.com/@IGotAnOffer-Engineering/videos) YouTube channel. Each folder covers one video: a README with scope, estimates, API/data model, components and the reasoning given for them, deep dives, and what the coach said about interview technique, plus an architecture diagram (`architecture.png`, source in `architecture.py`).

These are my own summaries written from the video transcripts. All credit for the designs and commentary goes to the interviewees and IGotAnOffer; follow the links to watch the originals. This repository is not affiliated with IGotAnOffer.

## Design walkthroughs

| # | System | Interviewee | Key ideas |
|---|---|---|---|
| 01 | [Google Drive / Dropbox](01-google-drive-dropbox/) | ex-Shopify EM | pre-signed S3 uploads, relational metadata, pub/sub sync, CDN, S3 key prefixes |
| 02 | [WhatsApp / Telegram](02-whatsapp-telegram/) | ex-Google EM | DynamoDB, consistent hashing, asynchronous message distributor |
| 03 | [Spotify](03-spotify/) | ex-Google EM | blob vs metadata split, hot-song caching (phone → CDN → server → S3) |
| 04 | [TikTok](04-tiktok/) | ex-Google EM | blob + key-value + SQL, ML "For You" feed with exclusion guardrails, read-ahead |
| 05 | [LinkedIn job search](05-linkedin-job-search/) | Amazon senior SWE | Elasticsearch retrieval + NoSQL detail, ML ranking with fallback, caches |
| 06 | [Google sponsored ads](06-google-ads/) | Atlassian senior EM | Kafka click pipeline, Redis sorted sets, offset-based idempotency |
| 07 | [Uber](07-uber/) | ex-Google SWE | per-city sharding, read / write / ride-data paths, exclusive driver offers, consensus |
| 08 | [Phone company billing](08-phone-billing-system/) | Amazon senior SWE | batch pipeline, shard by phone number, queue + elastic workers |
| 11 | [Instagram](11-instagram/) | ex-Meta data engineer | pre-generated feeds, celebrity problem, object storage + sharded SQL + NoSQL |
| 12 | [Twitter](12-twitter/) | senior engineer / manager | Kafka fan-out into Redis timelines, Cassandra wide rows, Snowflake IDs |
| 13 | [Robinhood](13-robinhood/) | ex-Google SWE (HFT) | NBBO aggregation, three scalable layers, WebSockets, state machine replication |
| 14 | [YouTube](14-youtube/) | FAANG senior SWE | transcoding pipeline, adaptive bitrate, CDN controller, keyword search |
| 15 | [Slack](15-slack/) | ex-Apple EM | WebSockets, Kafka ordering by chat id, Redis pub/sub with TTL leases, inbox for offline users |
| 16 | [Product recommendation system](16-product-recommendation-system/) | ex-Amazon principal engineer | feature store + embeddings + ranker, Kafka/Flink online, Spark offline, A/B testing |

## Interview technique videos

| # | Video | Gist |
|---|---|---|
| 09 | [10 key principles](09-ten-key-principles/) | scope the problem, draw about a third of the way in, working solution before optimising, explain choices, show your maths |
| 10 | [10 ways to impress](10-signals-interviewers-look-for/) | the communication, judgment and problem-solving signals interviewers score, plus yellow flags |

## Patterns that recur across the designs

- **Never stream big files through application servers.** Hand out a pre-signed URL (Drive, Spotify, YouTube, Slack, Google Ads) and let the client talk to object storage or the CDN.
- **Split storage by access pattern.** Blob/object store for bytes, relational for queried metadata, key-value/NoSQL for hot, high-volume lookups (feeds, messages, clicks).
- **Precompute reads.** Feeds, timelines, top-N ads and recommendations are built ahead of time (Redis, fan-out workers) because reads dwarf writes; special-case the celebrity / hot-item.
- **Decouple with a log or queue.** Kafka between ingestion and processing absorbs bursts, keeps per-key order (partition by chat, ad, or tweet id) and lets many consumers hang off one stream.
- **Make consumers idempotent.** Track offsets/ids so a replay after a crash does not double-count (ads scoring, client message de-dupe).
- **Separate the strongly-consistent core from the eventually-consistent edge.** Uber's ride state machine and Robinhood's stateful publishers are small and replicated; the read-heavy paths scale freely.
- **Degrade gracefully.** Fall back to simple ranking, contextual recommendations or on-demand feed construction rather than failing the request.
- **Layered caching and CDN** close to the user, with regional replication for latency and data residency.

## Notes on accuracy

Where a spoken calculation in a video was inconsistent, the README states the corrected figure and says so (for example the Instagram storage estimate, the Twitter storage estimate, the recommendation-system event rate, and the phone-billing monthly call count). Architectures are as described in each video, not how the real companies build these systems.

## Regenerating the diagrams

```sh
python3 -m venv .venv && .venv/bin/pip install playwright
PY=.venv/bin/python tools/build.sh 03-spotify     # writes architecture.svg and architecture.png
```

`tools/lanes.py` lays out each flow as a horizontal lane of service tiles; `tools/archlib.py` is a small dependency-free SVG library; `tools/render.py` renders the SVG to PNG with headless Chrome.

Videos not covered here (behavioural, résumé, salary, leadership, compilation): the channel also has talks on Googleyness, CTO/leadership interviews, résumé review and salary negotiation, which are not system designs.
