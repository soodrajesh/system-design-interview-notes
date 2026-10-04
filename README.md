# System design interview notes

Notes and architecture diagrams from system design interview material: the [IGotAnOffer: Engineering](https://www.youtube.com/@IGotAnOffer-Engineering/videos) YouTube channel (entries 01-16) [Hello Interview](https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly) written breakdowns (entries 17-22), and [TechPrep](https://www.youtube.com/@TechPrepYT) videos (entries 23-26). See [ROADMAP.md](ROADMAP.md) for what is planned next. Each folder covers one video or article: a README with scope, estimates, API/data model, components and the reasoning given for them, deep dives, and what the coach said about interview technique, plus an architecture diagram (`architecture.png`, source in `architecture.py`).

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
| 17 | [URL shortener (Bit.ly)](17-url-shortener/) | Hello Interview | counter + base62, 302 vs 301, cache + CDN + edge, disjoint counter ranges |
| 18 | [Distributed rate limiter](18-rate-limiter/) | Hello Interview | gateway placement, token bucket in Redis with atomic Lua, sharding, fail-open vs fail-closed |
| 19 | [Ticketmaster](19-ticketmaster/) | Hello Interview | Redis TTL seat locks, no double booking, Elasticsearch via CDC, virtual waiting room |
| 20 | [Web crawler](20-web-crawler/) | Hello Interview | pipelined stages, SQS backoff + DLQ, politeness, DNS, content dedup, crawler traps |
| 21 | [Ad click aggregator](21-ad-click-aggregator/) | Hello Interview | Flink stream aggregation, signed impression ids, hot-shard salting, Lambda-style reconciliation |
| 23 | [Distributed task scheduler](23-job-scheduler/) | TechPrep | Redis sorted-set timer, tenant queues, visibility timeouts, OCC + idempotency keys |
| 24 | [Metrics monitoring and alerting](24-metrics-monitoring/) | TechPrep | Gorilla compression, Flink alert rules via CDC, tiered rollups, cardinality limits |
| 25 | [Digital wallet (Cash App)](25-digital-wallet/) | TechPrep | double-entry ledger, sorted-lock deadlock avoidance, saga + transactional outbox, reconciliation |
| 26 | [Distributed cache (Redis)](26-distributed-cache/) | TechPrep | consistent hashing with virtual nodes, event loop + epoll, gossip failover, key salting |

## Interview technique videos

| # | Video | Gist |
|---|---|---|
| 09 | [10 key principles](09-ten-key-principles/) | scope the problem, draw about a third of the way in, working solution before optimising, explain choices, show your maths |
| 10 | [10 ways to impress](10-signals-interviewers-look-for/) | the communication, judgment and problem-solving signals interviewers score, plus yellow flags |
| 22 | [Delivery framework and levels](22-delivery-framework-and-levels/) | requirements → entities → API → design → deep dives; breadth vs depth expected at mid, senior and staff |

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

Entries 17-21 summarise Hello Interview's written articles (not their videos) and credit them as the source; entries 23-26 come from TechPrep video transcripts. Where Hello Interview's page for a topic is Premium-only, only the public outline is cited. Where a spoken calculation in a video was inconsistent, the README states the corrected figure and says so (for example the Instagram storage estimate, the Twitter storage estimate, the recommendation-system event rate, and the phone-billing monthly call count). Architectures are as described in each video, not how the real companies build these systems.

## Regenerating the diagrams

```sh
python3 -m venv .venv && .venv/bin/pip install playwright
PY=.venv/bin/python tools/build.sh 03-spotify     # writes architecture.svg and architecture.png
```

`tools/lanes.py` lays out each flow as a horizontal lane of service tiles; `tools/archlib.py` is a small dependency-free SVG library; `tools/render.py` renders the SVG to PNG with headless Chrome.

Not covered from the IGotAnOffer channel (behavioural, résumé, salary, leadership, compilation): the channel also has talks on Googleyness, CTO/leadership interviews, résumé review and salary negotiation, which are not system designs.
