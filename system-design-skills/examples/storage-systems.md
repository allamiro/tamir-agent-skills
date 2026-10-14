# `storage-systems`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Users upload videos up to 20 GB. Design the uploads, metadata, storage tiers and lifecycle rules, and compare replication with erasure coding on cost.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 5,659 | 6,845 |
| Input tokens read across all turns (including cached context) | 30,365 | 113,662 |
| Extra input tokens when the skill is installed | | +83,297 |
| Cost, US dollars at list price | 0.173 | 0.291 |
| Skills invoked in the sample run | none | `storage-systems` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 200 tokens for its name and description, which are in every session where the skill is installed, and about 3,800 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Video upload and storage design (videos up to 20 GB)

## 0. Assumptions

You didn't give a workload, so I picked one. The numbers below are illustrative and costs scale linearly with them.

| Input | Assumed |
|---|---|
| Uploads | 100k/day, average 1 GB (median ~300 MB, long tail to 20 GB) |
| Originals ingested | ~100 TB/day |
| Transcoded versions (resolution ladder plus thumbnails) | ~0.5× the original → ~50 TB/day |
| Logical growth | ~150 TB/day ≈ **4.5 PB/month ≈ 55 PB/year** |
| Reads | Very uneven: a few % of videos get most views; most are rarely watched after 30 days |
| Retention | Originals kept until the user deletes them; deleted items recoverable for 30 days |

## 1. Data sets and where they go

| Data set | Shape | Store |
|---|---|---|
| Originals | 0–20 GB, written once, read once by the transcoder, then rarely | Object storage |
| Transcoded versions (HLS/DASH segments) | 2–10 s segments of 1–5 MB, read often | Object storage behind a CDN |
| Thumbnails, posters, manifests | KB to low MB, read very often | Object storage behind a CDN |
| In-flight upload parts | Temporary | Object storage multipart upload |
| Metadata, state, ownership, search | Small rows, queried | Relational database (e.g. Postgres) |

Bytes are stored under **opaque generated keys** such as `orig/{video_id}/{upload_id}` and `r/{video_id}/{rendition}/{seg}.m4s`. A user's file name is never used as a key. It is stored as `display_name`.

## 2. Upload path (resumable, direct to storage)

```
Client ──POST /uploads {size, type, part_size}──▶ API ──▶ DB: upload_session(INIT)
                                                    └──▶ Store: CreateMultipartUpload
Client ◀── upload_id + first batch of signed part URLs (15–60 min TTL)
loop parts (4–8 in parallel, each retried on its own):
  Client ──PUT part N + CRC32C/SHA-256──▶ Store ──▶ ETag
  Client ──GET /uploads/{id}/urls?from=N──▶ API     (refresh URLs as they expire)
Client ──POST /uploads/{id}/complete {parts, ETags}──▶ API ──▶ Store: CompleteMultipart
                                                       └──▶ DB: UPLOADED ──▶ queue event
Worker: ffprobe check → malware/content scan → transcode → versions written → DB: READY
```

**Part size**
- The ceiling is 20 GB. S3's documented limits (from memory, so check them) are a 5 MiB minimum part, 10,000 parts maximum and 5 TB per object. That means 20 GB fits with parts of 2 MiB or more, so the part-count limit is not a concern.
- Default to **32 MiB parts**: a 20 GB file is ~600 parts. At 10 Mbit/s one part takes ~27 s, which bounds the work lost on a retry.
- Let the client adjust between 16 and 128 MiB based on measured throughput. Fast links use bigger parts and fewer requests.

**How long an upload takes**
- 20 GB at 50 Mbit/s is ~53 minutes. At 10 Mbit/s it is ~4.4 hours.
- So signed URLs must be **issued in batches and refreshed**. One URL valid for 5 hours would be a security liability.
- An upload session stays resumable for **7 days**.

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Video upload and storage design (videos up to 20 GB)

## 1. Upload path

The main rule is that video bytes never pass through the API servers. Clients upload straight to object storage using presigned multipart URLs.

```
Client ──(1) POST /uploads {size, sha256?, mime}──▶ Upload API ──▶ Metadata DB (session row)
       ◀─(2) upload_id, part_size, presigned URLs for parts 1..N (batched, 1h TTL)
Client ──(3) PUT part i (parallel 4–8, CRC32C per part)──▶ Object store (staging bucket)
Client ──(4) POST /uploads/{id}/complete {part ETags+checksums}──▶ API ──▶ CompleteMultipartUpload
Object store ──(5) ObjectCreated event──▶ Queue ──▶ Validator → Transcoder → Packager
```

| Decision | Choice | Why |
|---|---|---|
| Part size | 64 MB (adaptive: 16 MB on mobile, 128 MB on fast links) | 20 GB / 64 MB = 320 parts, well under the 10,000-part limit. A failed part retries in seconds. |
| Parallelism | 4–8 parts in flight | Fills the uplink without causing head-of-line stalls. |
| Integrity | CRC32C per part, checked by the store; optional full-file SHA-256 | Catches corruption per part, so only the bad part is resent. The full hash enables deduplication. |
| Resume | `GET /uploads/{id}` returns the confirmed parts (from ListParts plus the DB) | Works after a crash, network switch or app restart. Sessions live for 7 days. |
| URL issuance | Batches of about 50 presigned URLs, refreshed on demand | Keeps responses small, and leaked URLs expire quickly. |

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
