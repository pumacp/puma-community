# Anonymity and Privacy

PUMA Community is designed so that submitting results exposes only what is
scientifically relevant. No personally identifiable information leaves your
machine, and the local PUMA client refuses to publish a submission that
contains anything that pattern-matches as PII.

## What is published

When you submit a result, the public archive receives:

- The **model** tag and **prompting strategy** you ran.
- The **scenario** name and the **number of instances** evaluated.
- The full **metric tables**: F1-macro, precision and recall, MAE, MdAE,
  ECE, latency percentiles, tokens/second, robustness deltas, fairness
  deltas, and so on.
- The **hardware profile** name (`cpu-lite`, `cpu-standard`, `gpu-entry`,
  `gpu-mid`, or `gpu-pro`) — **not** your specific CPU model, your GPU
  model, your VRAM size, or your hostname.
- The **PUMA version** that produced the run.
- Your **self-chosen submitter alias** — any string of your choice; it can
  be a pseudonym, a project name, an organisation name, or simply
  `anonymous`.
- **Aggregate sustainability data**: total gCO₂eq for the run and the
  country grid code used by CodeCarbon.

## What is NOT published

- Your **GitHub username**. The PR is opened from a fork using your PAT,
  but your username is not embedded in the submission body. (It is, of
  course, visible on the PR itself; if that matters to you, open the PR
  from a pseudonymous GitHub account.)
- Your **IP address**.
- Your **machine hostname**.
- Your **file system paths** (the local validator strips and rejects any
  absolute path string).
- The **raw prompts** sent to the model and the **raw model responses**.
  Only aggregated metrics survive into the submission.
- Any **environment variables**.

## The PII scanner

Before any submission — including dry-runs — the local validator scans the
serialised submission for patterns that look like:

- email addresses
- phone numbers (international and national formats)
- IPv4 and IPv6 addresses
- absolute file system paths (`/home/...`, `C:\...`, etc.)
- GitHub Personal Access Tokens (`github_pat_...`, `ghp_...`, `ghs_...`)
- AWS access key IDs

If any pattern matches, the submission is **blocked locally** and you are
shown which field carries the problematic content. The PR is never opened.

## Cryptographic integrity

Every submission includes a **SHA-256 hash over a deterministic summary of
the predictions**. The hash certifies that the published metrics correspond
to the predictions the submitter generated — it does not expose the
predictions themselves. The validation pipeline recomputes the hash and
refuses any submission whose hash doesn't match.

## Your right to withdraw

If you submit and later decide you want it removed, open an issue at
[pumacp/puma-community/issues](https://github.com/pumacp/puma-community/issues)
with the submission ID. Submissions can be revoked: a maintainer will open
a removal PR that deletes the file under `submissions/`. The badge counts
refresh on the next push.
