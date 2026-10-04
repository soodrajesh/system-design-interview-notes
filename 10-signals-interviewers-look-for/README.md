# System design interviews: 10 ways to impress your interviewer

**Source:** [System design interviews: 10 ways to IMPRESS your interviewer (with ex-Google EM)](https://www.youtube.com/watch?v=PSYdvx0lwLg) · IGotAnOffer: Engineering · 40 min
**Speaker:** Mark, ex-Google engineering manager. The video itself is about the **signals** an interviewer looks for, grouped into three categories. There is no architecture diagram because this is not a design.

## 1. Communication (pervasive, foundational)

| Signal | What the interviewer wants to see |
|---|---|
| **Listening** | You restate the problem, pause before reacting, nod, and take notes while the question is read. |
| **Conciseness** | Notes and drawings capture the salient points; you are not transcribing. Identifying what matters is itself a signal. |
| **Sharing your mindset** | Tell them your process, assumptions and mental model ("I'll take notes and think out loud, bear with me"). This lowers the interviewer's cognitive load. |

## 2. Judgment

| Signal | What the interviewer wants to see |
|---|---|
| **Focus on the core problem** | Most of your time on the business logic of the system. Mention standard parts (API gateway, load balancer, CDN) briefly, don't dwell. |
| **Avoid scope creep and premature optimisation** | Don't add requirements. Use a **"parking lot"** text box on the canvas for ideas (data placement, tiered storage, multi-layer caching) so you can say them, forget them, and return if time permits. This also leaves a record for the interviewer's write-up. A key meta-signal: **you can reach a working solution in the time allowed.** |
| **Flexibility** | You change your mind with a reason (e.g. "I need strong consistency here, so relational over NoSQL"), or when the interviewer adds a requirement, or when time forces a cut. Be explicit about why, in a sentence. |

Reading the interviewer: follow-up questions are usually either clarification requests or **hints** that something will not work. Too many hints is a common cause of "did not meet the bar".

## 3. Problem solving

| Signal | What the interviewer wants to see |
|---|---|
| **Domain knowledge** | You know what the building blocks are good for: queues, CDN, relational vs NoSQL vs graph vs blob storage. Applied knowledge, not encyclopedic. Exact S3 limits are not required. Awareness of current tech, such as where AI could help, is a plus. |
| **Reasonable design choices** | Each component has a short "why". Example: a queue between stateless servers and workers, because their load differs and they must scale independently. The interviewer need not agree. |
| **Testing your design** | Walk the main flows end to end, be self-critical, and note an **edge case or failure mode**: at scale, anything that can happen will. Finding one tricky distributed-systems edge case shows you think beyond the happy path. |
| **Scaling** | Back-of-envelope maths you can explain (QPS, storage, bandwidth, CPU) and good judgment about *which* numbers matter. Cheat sheets are fine; just pasting a result from a calculator or ChatGPT is not. Confusing TB with PB is not okay, being an order of magnitude off may be. |

## Yellow and red flags

- **Defensiveness** when the interviewer questions your design. It is the opposite of flexibility and humility; reframe and explain differently instead.
- **Diving straight in** without understanding the problem.
- **Spending 40 minutes on requirements**, trying to extract a full PRD, so you never reach a solution.

## Takeaways

Communication errors are the cheapest to fix with practice; they apply beyond system design. Practice out loud, because under pressure even simple arithmetic evaporates.
