# System design interviews: 10 key principles

**Source:** [System Design Interviews: 10 Key Principles (with ex-Google EM)](https://www.youtube.com/watch?v=8dG0qzNAVXI) · IGotAnOffer: Engineering · 41 min
**Speaker:** Mark, ex-Google engineering manager (13 years, hundreds of system design interviews), interviewed by Tom.

There is no architecture here; the video is about how to run the interview. The first principle frames the rest: **a real design takes days, an interview gives you 45-50 minutes, so efficiency is everything.**

| # | Principle | What it means in practice |
|---|---|---|
| 1 | **Communicate efficiently; align mental models** | The interviewer should always know what you are thinking and drawing. They need not agree with the design, only follow it. |
| 2 | **Scope the problem** | "Design Spotify/YouTube" is far too big. Narrow it to a few use cases, drop features, pick an interface point (e.g. start at the API, not the phone UI). Interviewers are sometimes deliberately vague, so fill the gaps with questions and stated assumptions. Follow the interviewer if they steer elsewhere. |
| 3 | **Start drawing about a third of the way in** | ~15 minutes of a 45-minute slot, once requirements, scope and maybe the API are clear. Drawing too early means you did not understand the problem; too late and you will not finish. A visual aid lowers the interviewer's effort. |
| 4 | **Reach a working solution before optimising** | Start simple; do not add requirements that were not asked for (e.g. tiered storage). It is fine to say "I'd add a cache here, I'll come back to it". The same advice appears in Google's own guidance for coding rounds (brute force first) and mirrors building an MVP. |
| 5 | **Breadth first, then depth on request** | Name the building blocks you know (caching, load balancing, storage tiers) in ten seconds each to signal breadth. If the interviewer asks, go deep and negotiate the time. |
| 6 | **Understand the problem; use your own API** | Engineers jump to solutions. Spend a few minutes pretending you are the client of your API: happy path, error paths, edge cases. It surfaces hidden assumptions ("how do I signal the last call?"). A full spec is impossible, so some requirements will be discovered along the way. |
| 7 | **Practise (and record yourself)** | The knowing-doing gap is real; practice builds confidence and lowers stress, "like going to the gym". Use a coach for domain feedback and anyone, even a non-engineer, for communication feedback. Review recordings. Leave enough time for a mock plus feedback. |
| 8 | **Explain your technology choices** | Not "a database" but "SQL because the data is structured, multi-table, needs joins, and I may shard later". The interviewer is looking for judgment, and again does not have to agree. |
| 9 | **Back-of-envelope maths, shown** | Translate "1B queries/day" to QPS using ~100,000 s/day (≈10k QPS), mention a peak factor (e.g. ×5 → 50k), estimate servers (1k req/s each → 50, plus autoscaling). Know the unit ladder (each 1,000× apart) and bits vs bytes for bandwidth (≈10 bits per byte as shorthand, 8 exactly). Calculators are fine only if you show the logic. |
| 10 | **Master the drawing tool** | Know the tool the company uses (e.g. Excalidraw at Meta, Google Drawings at Google; ask the recruiter). You need only boxes, text and arrows. Colours, perfect connectors and grouping do not matter; you are graded on the answer, not the diagram. Moving or deleting boxes when the design changes is fine. |

## Quick checklist

1. Restate the problem, ask questions, state assumptions.
2. Cut scope; confirm with the interviewer.
3. Define the API/interface and sanity-check it as a client.
4. Do rough numbers (QPS, peak, storage, bandwidth).
5. Around minute 15, draw the simplest end-to-end working design.
6. Justify each technology choice in a sentence.
7. Mention (don't build) caching, tiering, replication; go deep only when asked.
8. Walk a use case through the design to find bottlenecks, then optimise.
