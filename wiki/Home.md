# PUMA Community Wiki

PUMA Community is a public hub where users of the PUMA benchmarking tool
share their local LLM evaluation results. Every submission is
cryptographically integrity-checked, schema-validated, and PII-scanned before
publication. The submission flow lives entirely on GitHub — there is no
central server, no account beyond your GitHub account, and no fee.

## Why this exists

Local LLM benchmarks depend heavily on hardware: a 7-billion-parameter model
behaves differently on a 4 GB GPU than on a 24 GB GPU than on CPU. No
commercial benchmark captures that diversity. By pooling verified results
across machines, PUMA Community builds a community-owned record of how local
models actually perform across the configurations practitioners run.

## Explore the Wiki

- [Why PUMA Community?](Why-PUMA-Community) — the rationale and the value
  proposition for sharing your results.
- [Running a Benchmark](Running-A-Benchmark) — a short overview of running
  PUMA locally; the full reference lives in the PUMA Wiki.
- [Submitting Results](Submitting-Results) — step-by-step submission flow,
  including PAT creation, dry-run, and publish.
- [Submission Format](Submission-Format) — what's inside a submission JSON,
  what every field means, and accepted values.
- [Anonymity and Privacy](Anonymity-And-Privacy) — what is and isn't
  published, how the PII scanner works, how to withdraw a submission.
- [Validation Process](Validation-Process) — what happens after you open a
  submission PR.
- [Mirror Locations](Mirror-Locations) — status of Hugging Face, Zenodo, and
  Kaggle mirrors.
- [FAQ](FAQ) — common questions about validation, hardware, models, and
  integrity hashes.
- [For Maintainers](For-Maintainers) — operator-facing guide for those with
  write access to this repository.

## Quick links

- [PUMA Community repo](https://github.com/pumacp/puma-community) — the
  canonical submission archive and the schema.
- [PUMA tool repo](https://github.com/pumacp/puma) — the benchmarking
  framework that produces the submissions.
- [Latest badges](https://github.com/pumacp/puma-community#readme) —
  submission count, model count, scenario count, latest submission.
