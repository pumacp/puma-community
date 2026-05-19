# Oracle Cloud auxiliary deployment

## Status

> **Status:** Design proposal. **NOT implemented** as of PUMA Community
> v1.0.0. Revisit when demand from the community justifies an
> always-on auxiliary service.

## Overview

PUMA Community v1 is fully serverless. Every piece of infrastructure
lives inside GitHub: the repository content, the GitHub Actions workflows
that validate and auto-merge submissions, the Wiki pages, and the
outbound mirror workflows that push merged submissions to Hugging Face,
Zenodo, and Kaggle. This document describes an optional v2 extension —
an always-on auxiliary service hosted on Oracle Cloud Always Free — that
complements the GitHub-native setup without replacing any part of it.
The canonical source of truth remains
[`pumacp/puma-community`](https://github.com/pumacp/puma-community);
the auxiliary service is a read-only consumer of that repository.

## Motivation

The following capabilities would benefit from an always-on host but are
not present in v1:

- A read-only HTTP API over the submission archive, with filters by
  `model`, `scenario`, `from`/`to` date range, and hardware `profile`.
- A static leaderboard page rendered nightly from the merged
  submissions.
- A faster badge endpoint with longer cache headers than the shields.io
  endpoint can provide out of the box.
- A simple full-text search index over submission metadata.
- A staging area for previewing schema-v2 migrations before they ship
  to the canonical repository.

None of these are required for v1; each becomes unlocked by an always-on
host.

## Why Oracle Cloud?

Three reasons:

1. **Cost.** The Oracle Cloud "Always Free" tier has no expiration
   date (unlike most 12-month trial tiers offered by other providers).
   At the time of writing, it covers the proposed deployment at
   $0/month.
2. **Capacity.** The Arm-based Ampere A1 allocation is generous enough
   for a small Python service plus its dependencies, with headroom for
   periodic data syncs and caching.
3. **No vendor lock-in for data.** All data served by the auxiliary
   service is the same data already on GitHub at
   `pumacp/puma-community`. The source of truth never moves; the
   service is a read-only mirror.

Oracle adjusts the Free Tier periodically; consult the current
specifications at <https://www.oracle.com/cloud/free/> rather than
relying on numbers in this document.

## Proposed architecture

A single VM running three cooperating components:

- **nginx** as a TLS-terminating reverse proxy. Certificates are
  obtained automatically from Let's Encrypt (e.g. via the embedded
  Caddy ACME client or `certbot`).
- **A Python FastAPI service** exposing three routes:
  - `GET /api/v1/submissions` — paginated list with filters
    (`?model=`, `?scenario=`, `?from=`, `?to=`, `?profile=`).
  - `GET /api/v1/submissions/{submission_id}` — single submission JSON.
  - `GET /api/v1/stats` — aggregate counts (per model, per scenario,
    rolling-window counts over time).
- **A periodic sync job** (cron, every 5-15 minutes) that runs
  `git pull` on a local clone of `pumacp/puma-community/main` and
  re-builds an in-memory or on-disk SQLite index of the submissions.
  Indexing is idempotent; the job is safe to re-run.
- **(Optional) A static leaderboard page** at `/leaderboard`,
  regenerated whenever the sync job detects new submissions and served
  directly by nginx (no Python on the hot path).

```
              ┌────────────────────────────┐
              │  pumacp/puma-community     │
              │  (GitHub — source of truth)│
              └──────────────┬─────────────┘
                             │ git pull (cron, 5-15 min)
                             ▼
   ┌──────────────────────────────────────────────────────────┐
   │  Oracle Cloud VM                                          │
   │                                                           │
   │   ┌────────┐    ┌──────────────┐    ┌─────────────────┐  │
   │   │ nginx  ├───►│ FastAPI app  ├───►│ SQLite index    │  │
   │   │ (TLS)  │    │ (read-only)  │    │ (regenerated)   │  │
   │   └────────┘    └──────────────┘    └─────────────────┘  │
   └──────────────────────────────────────────────────────────┘
                             ▲
                             │ HTTPS (anonymous)
                        public clients
```

## Deployment sketch

Each step requires more detail before deployment; the future
`pumacp/puma-community-api` repository will hold the production
configuration.

1. Sign up for Oracle Cloud Free Tier; provision one Ampere A1
   instance.
2. SSH in and install Docker and Docker Compose.
3. Clone the future `pumacp/puma-community-api` repository (placeholder
   — does not exist yet).
4. Configure DNS (optional: a free DDNS subdomain, or serve on the
   bare IP for the initial bring-up).
5. `docker compose up -d`, then set up a cron entry that invokes the
   sync job on the desired cadence.

## Cost analysis

At the time of writing, the Always Free tier covers the proposed
deployment at $0/month. Three cost risks worth tracking:

- **Tier changes by Oracle.** Free-tier policies have changed before
  in the cloud industry; the project should re-evaluate annually.
- **Outbound bandwidth** if the API becomes popular. The Always Free
  tier caps egress per month; popular API consumers should be steered
  toward the static leaderboard or the GitHub raw-content URLs.
- **TLS certificate management.** Let's Encrypt is free and
  automated; no paid alternative is needed. The renewal job should be
  monitored.

## Trust model

- **Read-only.** No write surface; clients cannot create or modify
  submissions through the API.
- **Public data only.** Everything served is already public in
  `pumacp/puma-community`. There is no PII handling concern beyond
  what the client-side scan in `puma share-results` already enforces
  before submissions reach the canonical repository.
- **No authentication.** The API is anonymous-only; per-IP rate
  limiting is applied by nginx.
- **Source of truth unchanged.** A failure or compromise of the Oracle
  Cloud instance does not affect the canonical repository on GitHub;
  re-provisioning the VM is the recovery path.
- **Disaster recovery.** A fresh instance can be provisioned in
  under an hour from the deployment recipe once that recipe lives in
  the future `puma-community-api` repository.

## Future work

- Create the `pumacp/puma-community-api` repository with the FastAPI
  service code, the nginx configuration, and the Docker Compose stack.
- Provision a staging instance before promoting to production.
- Add Terraform or Ansible scripts for reproducible provisioning.
- Add a per-IP rate-limit dashboard so operators can see when nginx
  starts throttling.
- Evaluate adding a write-side review queue if the community grows
  beyond what a manual Pull Request flow can absorb (very long-term).

## Decision

- **v1:** **NOT implemented.** PUMA Community is fully serverless and
  this is by design — it keeps the project sustainable for one or two
  maintainers.
- **Trigger for v2:** revisit when the community produces more than
  500 submissions, OR when external researchers request programmatic
  access (an HTTP API), whichever comes first.
- **Owner:** the project maintainers, working with any community
  member interested in operating the auxiliary service.
