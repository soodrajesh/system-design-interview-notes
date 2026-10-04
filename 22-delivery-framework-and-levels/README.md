# A delivery framework and what each level must show

**Source:** the Hello Interview problem breakdowns used in [17](../17-url-shortener/), [18](../18-rate-limiter/), [19](../19-ticketmaster/), [20](../20-web-crawler/) and [21](../21-ad-click-aggregator/), all of which follow the same "Delivery Framework" (the full guide lives at [hellointerview.com](https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery)). This note collects the technique that repeats across those articles. It complements [09](../09-ten-key-principles/) and [10](../10-signals-interviewers-look-for/), which come from the IGotAnOffer channel.

## The sequence

1. **Requirements.** Functional ("users should be able to…") and non-functional ("the system should…"). Keep the top 3-4 features above the line, and explicitly list others as "below the line". Ask for scale. Quantified non-functional requirements ("<10 ms", "10k clicks/s", "99.99%") are what you design against later.
2. **Core entities.** A short list is enough; flesh out columns once the design takes shape.
3. **API or system interface.** For user-facing products: REST endpoints mapping 1:1 to functional requirements. For data-processing problems (crawler, click aggregator): define inputs and outputs and the **data flow** instead. Start simple and say you will evolve it.
4. **High-level design.** Go through functional requirements one at a time, building the simplest system that satisfies each.
5. **Deep dives.** Use the non-functional requirements as the agenda. This is why good non-functional requirements matter: they stop you running out of things to say. Pick the interesting 2-3 and update the diagram as you go.
6. **Defer back-of-envelope maths** until a decision needs it (for example, sizing the crawler fleet or the cache), instead of opening with a wall of numbers.

## How answers are scored: breadth vs depth by level

| Level | Breadth : depth | What the interviewer looks for |
|---|---|---|
| Mid-level | ~80 : 20 | A working high-level design for the functional requirements; basic component knowledge (they will probe "what does an API gateway do?"); you lead early, they lead later |
| Senior | ~60 : 40 | Speed through basics; proactive about bottlenecks; trade-off articulation; hands-on depth in your areas of experience |
| Staff+ | ~40 : 60 | Deep dives into 2-3 (or 3+) areas, grounded in real experience, with minimal steering; the interviewer should learn something new |

## Patterns the articles name

- **Scaling reads** (URL shortener, Ticketmaster, rate limiter hot keys): cache, CDN/edge, replicas.
- **Scaling writes** (ad clicks, rate limiter): stream buffering, pre-aggregation, partitioning by key, hot-key salting.
- **Dealing with contention** (Ticketmaster reservations, rate-limiter token buckets): make the whole read-modify-write atomic (Lua script, short transaction with expiry check, `SET NX EX`).
- **Real-time updates** (waiting room, seat maps): SSE vs WebSockets vs polling.

## Habits worth copying

- Present options as bad / good / great and say why, including the trade-off of the one you pick.
- Push back on reflexive answers when context makes them unnecessary (for example, Flink checkpointing with one-minute windows).
- Mention the alternative technology and where it would win (TSDB vs OLAP, Kafka vs SQS, 301 vs 302).
- Visual clarity matters: your interviewer reads your diagram the next day while writing feedback.
- Pick a failure mode on purpose and defend it (fail-open vs fail-closed).
