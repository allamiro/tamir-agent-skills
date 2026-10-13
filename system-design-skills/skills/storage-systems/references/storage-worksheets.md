# Storage worksheets

Illustrative numbers.

## 1. Overhead and tolerance comparison

Raw data to protect: 1 PB.

| Scheme | Raw storage consumed | Overhead | Tolerates losing |
|---|---|---|---|
| 3× replication | 3 PB | 3.0× | 2 copies |
| Erasure coding k=6, m=3 | 1.5 PB | (6+3)/6 = 1.5× | any 3 of 9 shards |
| Erasure coding k=10, m=4 | 1.4 PB | (10+4)/10 = 1.4× | any 4 of 14 shards |
| Erasure coding k=10, m=4 across 14 failure domains | 1.4 PB | 1.4× | up to 4 domains |

Savings of k=10,m=4 vs 3× replication = 3.0 − 1.4 = 1.6 PB per PB protected. Costs: reading a
whole shard set to repair one lost shard moves k shards of traffic (for k=10, about 10 times
the lost shard's size), reconstructing on read when a shard is missing adds latency, and
small objects waste space. Shards must live on distinct failure domains for the stated
tolerance to hold.

## 2. Part-size planning (multipart upload)

Given file size F, part size P: parts = ceil(F / P). Constraints: provider minimum part
size and maximum part count (VERIFY current values). For F = 50 GB and P = 64 MiB →
parts = ceil(50×10^9 / 67,108,864) ≈ 746. Smaller P = more requests and calls, finer retry;
larger P = fewer requests, costlier retry of a failed part. Choose P so that a part uploads
in a few seconds to a few tens of seconds on the slowest expected client link.

## 3. Lifecycle rule examples (generic)

| Rule | Condition | Action |
|---|---|---|
| Abort stale multipart | Incomplete for > 7 days | Abort and delete parts |
| Tier down | Not read for 30 days | Move to infrequent tier |
| Archive | Age > 180 days | Move to archive tier |
| Expire noncurrent versions | Version older than 30 days and ≥ 3 newer exist | Delete |
| Expire temp | Prefix `tmp/`, age > 1 day | Delete |

Set the day counts from access logs and retention requirements; tiers may have minimum
storage durations and retrieval fees.

## 4. Metadata schema sketch

```sql
CREATE TABLE file_object (
  id            uuid PRIMARY KEY,
  owner_id      uuid NOT NULL,
  display_name  text NOT NULL,
  storage_key   text NOT NULL UNIQUE,   -- opaque, generated
  size_bytes    bigint,
  sha256        bytea,
  content_type  text,
  state         text NOT NULL,          -- INIT | READY | DELETED
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX ON file_object(owner_id, created_at DESC);
```

## 5. Choosing storage: quick table

| If the data is ... | Use |
|---|---|
| Database files / VM disk | Block volume (with platform replication and snapshots) |
| Shared documents needing directory semantics | Network file system |
| User uploads, images, video, backups, logs, static assets | Object storage + metadata DB (+ CDN for reads) |
| Small structured records | Database (`database-selection`) |
| Frequently updated partial content | Database or file/block, not object |

## 6. Restore drill checklist

- [ ] Restore a deleted object by version
- [ ] Restore a full prefix from the independent backup
- [ ] Verify checksums against recorded values
- [ ] Measure time to restore N TB; compare with RTO
- [ ] Verify access controls on restored data
