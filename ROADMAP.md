# Roadmap: what to add next

Compiled from one research pass (web search plus the Hello Interview pages already summarised here). Channel rankings come from a 2026 "best system design channels" roundup and Reddit/Blind threads, so treat them as community consensus rather than measurement.

## Sources worth mining

| Source | Why it is useful | Best for | Notes on using it here |
|---|---|---|---|
| [Hello Interview](https://www.youtube.com/@hello_interview) (+ written breakdowns) | Single repeatable framework (requirements, entities, API, high-level design, deep dives), explicit "what is expected at each level", free long-form articles | Interview structure, level calibration | **Started**: entries 17-21 and note 22 come from the written breakdowns. Many more problems available |
| [ByteByteGo](https://www.youtube.com/@ByteByteGo) (Alex Xu) | Visual explainers of patterns and real company architectures; the book chapters follow the interviewer/candidate dialogue style | Patterns, fundamentals, "how does X really work" | Summarise concepts (e.g. rate-limit algorithms, consistent hashing) and cite the chapter; don't reproduce the paid book |
| [Jordan Has No Life](https://www.youtube.com/@jordanhasnolife5163) | Deep distributed-systems detail (replication, consensus, stream processing); long series of numbered problems (e.g. [rate limiter](https://www.youtube.com/watch?v=VzW41m4USGs), [web crawler](https://www.youtube.com/watch?v=MdWvMX4J-Vc)) | Senior/staff depth | Pair his depth with the shorter interview-style versions of the same problem |
| [Gaurav Sen](https://www.youtube.com/@gkcs) | Conceptual grounding; e.g. [DoorDash: geohashing and WebSockets](https://www.youtube.com/watch?v=iRhSAR3ldTw) | Fundamentals, location-based systems | Good source for a proximity-service entry |
| [Exponent](https://www.youtube.com/@tryexponent) | Many real mock interviews with commentary | Communication, pacing | Same format as the IGotAnOffer entries |
| [TechPrep](https://www.youtube.com/@TechPrepYT) ([playlist](https://www.youtube.com/playlist?list=PLRtLu6rCuAlkO-HiER3AKoKkSG5DPp9TX)) | Short (10-22 min) walkthroughs of Ticketmaster, task scheduler, metrics monitoring, Cash App, Kafka, Redis | Fast revision, infrastructure-style problems | Good for the backlog entries below |
| [CodeKarle](https://www.youtube.com/@codeKarle), [Tech Dummies](https://www.youtube.com/@TechDummiesNarendraL), [Arpit Bhayani](https://www.youtube.com/@AsliEngineering), [Hussein Nasser](https://www.youtube.com/@hnasr) | Question walkthroughs, HLD/LLD balance, database/caching internals, protocols and backend depth | Specific deep dives | Use for single-topic notes |
| NeetCode, Success in Tech | Combined coding + design prep; career context | Whole-loop planning | Optional |

Also worth linking: the free **System Design Primer** GitHub repository (community favourite alongside the YouTube channels).

## Problems to add (ranked by how often they come up, minus what's already covered)

Already covered: Drive, WhatsApp/Slack, Spotify, TikTok/Instagram/Twitter feeds, LinkedIn search, Google Ads, Uber, billing, Robinhood, YouTube, recommendations, URL shortener, rate limiter, Ticketmaster, web crawler, ad click aggregator.

| Priority | Problem | Why it earns a slot | Likely source |
|---|---|---|---|
| 1 | **Notification system** (push/SMS/email) | Fan-out, retries, dedup, user preferences, third-party providers | ByteByteGo chapter, Hello Interview |
| ✅ 2 | **Distributed cache** (Redis-like) | Eviction, replication, consistent hashing, hot keys | Hello Interview, TechPrep playlist |
| ✅ 3 | **Payment system / wallet** (Cash App / Stripe-style) | Idempotency, double-entry ledger, reconciliation, exactly-once effects | TechPrep, ByteByteGo |
| ✅ 4 | **Distributed job scheduler** | Leasing, retries, at-least-once vs exactly-once, time-based triggers | Hello Interview, TechPrep |
| ✅ 5 | **Metrics monitoring and alerting** | Time-series storage, downsampling, alert evaluation | TechPrep, ByteByteGo |
| 6 | **Proximity service** (Yelp / DoorDash) | Geohash vs quadtree, location updates over WebSockets | Gaurav Sen, ByteByteGo |
| 7 | **Typeahead / autocomplete** | Trie vs prefix index, ranking, caching, update pipeline | ByteByteGo, Jordan |
| 8 | **Collaborative editor** (Google Docs) | OT vs CRDT, presence, real-time updates | Hello Interview |
| 9 | **Distributed message queue** (Kafka-like) | Partitioning, replication, consumer groups, ordering, delivery semantics | TechPrep, Jordan |
| 10 | **Key-value store** (Dynamo-style) | Quorum reads/writes, gossip, vector clocks, anti-entropy | ByteByteGo |
| 11 | Top-K / leaderboard, online auction, hotel booking, Tinder, online judge | Common variants that reuse the patterns above | Hello Interview |
| 12 | **LLM / RAG / agent system design** | Increasingly asked; vector stores, evaluation, cost and latency | Hello Interview, ByteByteGo (AI content) |

Done in entries 23-26 (TechPrep). Several of the Hello Interview pages for these problems are Premium-only, so they are linked for their public outline but not summarised.

## Technique notes to add

1. **Estimation cheat sheet**: powers of two and ten, latency numbers, seconds-in-a-day rounding, common throughput of Redis/Postgres/Kafka/NIC, with worked conversions (builds on [09](09-ten-key-principles/)).
2. **Consistency and availability vocabulary**: CAP/PACELC, quorum, linearizability vs eventual, when each is right (appears in Slack, Ticketmaster, Uber).
3. **Idempotency and delivery guarantees**: offsets, idempotency keys, outbox, dedupe windows (ads, payments, crawler, notifications).
4. **Sharding and hot keys**: key choice, consistent hashing, salting (rate limiter, ad clicks, tweets).
5. **Caching patterns**: read-through/write-through/write-behind, invalidation, stampede protection, multi-layer (Spotify, URL shortener, Ticketmaster).
6. **ID generation**: counters, Snowflake, hashes, UUID trade-offs (Twitter, URL shortener, Slack).
7. **Real-time delivery**: polling vs SSE vs WebSockets, connection management, presence (Slack, Robinhood, Ticketmaster, Uber).
8. **Failure modes**: fail-open vs fail-closed, graceful degradation, retries with backoff and jitter, DLQs.
9. **Communicating in the room**: the signals list in [10](10-signals-interviewers-look-for/) plus level expectations in [22](22-delivery-framework-and-levels/); add a one-page "first five minutes" script and a time budget.
10. **Cross-company calibration**: Uber is product-first; Google/Meta weigh breadth and communication; add what the sources say per company.

## Format improvements

- A **"pick a pattern" index** mapping each problem to the patterns it exercises, so you can study by pattern.
- A **side-by-side comparison** of different channels' answers to the same question (Hello Interview vs IGotAnOffer vs Jordan on rate limiter, URL shortener, Uber, YouTube, web crawler), which is where differing opinions show up.
- Keep corrected arithmetic notes whenever a source's maths is off (already done for four entries).

## Ground rules for new entries

Write in my own words, link the source, state what was read (transcript vs article), skip paywalled/premium material, and keep the diagram format (`tools/lanes.py`).
