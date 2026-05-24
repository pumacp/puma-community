<p align="center">
  <img src="https://raw.githubusercontent.com/pumacp/puma/main/assets/img/PUMA.png" alt="PUMA Logo" width="220">
</p>

<h1 align="center">PUMA Community</h1>

<p align="center">
  <em>Public submission hub for community-contributed local-LLM benchmark results in ICT Project Management tasks.</em>
</p>

<p align="center">
  <!-- Group A: repository status -->
  <a href="https://github.com/pumacp/puma-community/actions/workflows/validate-submission.yml">
    <img src="https://github.com/pumacp/puma-community/actions/workflows/validate-submission.yml/badge.svg" alt="Validate submissions">
  </a>
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License: MIT">
  <img src="https://img.shields.io/badge/schema-v1.0.0-green" alt="Schema v1.0.0">
  <br>
  <!-- Group B: dynamic content -->
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pumacp/puma-community/main/badges/submission-count.json" alt="Submissions">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pumacp/puma-community/main/badges/models-count.json" alt="Models">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pumacp/puma-community/main/badges/scenarios-count.json" alt="Scenarios">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pumacp/puma-community/main/badges/latest-submission.json" alt="Latest">
  <br>
  <!-- Group C: ecosystem mirrors (target URLs may evolve as namespaces are claimed) -->
  <a href="https://huggingface.co/datasets/pumaproject/puma-community-submissions">
    <img src="https://img.shields.io/badge/%F0%9F%A4%97-Hugging%20Face-yellow" alt="Hugging Face dataset">
  </a>
  <a href="https://zenodo.org/communities/pumacp">
    <img src="https://img.shields.io/badge/Zenodo-DOI-blue" alt="Zenodo community">
  </a>
  <a href="https://www.kaggle.com/datasets/pumacp/puma-community-submissions">
    <img src="https://img.shields.io/badge/Kaggle-Dataset-blue" alt="Kaggle dataset">
  </a>
</p>

<p align="center">
  <a href="https://github.com/pumacp/puma">PUMA Benchmark Tool</a> ·
  <a href="../../wiki">Wiki</a> ·
  <a href="docs/colab-demo.md">Colab Demo</a> ·
  <a href="CONTRIBUTING.md">Contribute</a> ·
  <a href="../../issues">Issues</a>
</p>

---

## Overview

PUMA Community is the public archive of benchmark results contributed by users
of the open-source PUMA Benchmark Tool. PUMA evaluates local, open-weight
language models on ICT Project Management tasks — issue triage, story-point
estimation, backlog prioritisation — and produces a self-contained JSON
report for every run. This repository accepts those reports as Pull Requests,
validates each one against the published schema, and merges the valid ones
automatically. The merged archive is mirrored outward to Hugging Face
Datasets, Zenodo, and Kaggle so that downstream researchers and tool builders
can consume the data anywhere it is convenient.

There is no application code in this repository. The benchmark engine lives
at [`pumacp/puma`](https://github.com/pumacp/puma); this repo is the public
data layer. Submissions are immutable once merged, so historical results
remain stable for downstream analyses, leaderboards, and DOI-stamped
archives.

## Why PUMA Community?

- **Reproducible.** Every submission carries a deterministic SHA-256 hash
  computed over the canonical serialisation of the run's predictions. Anyone
  can re-derive the hash and detect after-the-fact tampering.
- **Transparent.** Every submission reports full energy use and carbon
  footprint via CodeCarbon (`co2_grams_total`, `energy_kwh_total`,
  `tracking_mode`) alongside the quality metrics, so accuracy can be
  compared honestly against environmental cost.
- **Open.** MIT-licensed, schema-versioned (Draft 2020-12), and mirrored to
  Hugging Face, Zenodo, and Kaggle. The schema preserves v1 documents
  indefinitely; future revisions land at `schema/submission.v2.json`,
  `submission.v3.json`, and so on without breaking older readers.

## Quick start

1. **Run the demo notebook in Colab — zero install.**
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pumacp/puma-community/blob/main/notebooks/puma_community_demo.ipynb)
   The notebook downloads the schema, validates a sample submission, and
   browses the public archive via the anonymous GitHub API. No tokens, no
   account required.

2. **Submit via the PUMA tool — three commands.**

   ```bash
   puma auth login github                      # store a Personal Access Token (one-off)
   puma share-results --dry-run --run-id <id>  # preview the payload as a local JSON file
   puma share-results --run-id <id>            # fork, branch, commit, and open the PR
   ```

   The PUMA tool builds the payload from your local SQLite results, scans for
   personal data, signs the integrity hash, and opens the Pull Request on
   your behalf. The tool lives at
   [`pumacp/puma`](https://github.com/pumacp/puma).

3. **Submit manually.** Read [`CONTRIBUTING.md`](CONTRIBUTING.md) for the
   JSON-based path: name the file `submissions/<submission_id>.json`,
   validate locally with `python -m jsonschema -i submission.json
   schema/submission.v1.json`, push to a branch, and open the PR.

## How submissions work

Every Pull Request that adds or modifies a file under `submissions/` is
processed by the [`validate-submission`](.github/workflows/validate-submission.yml)
GitHub Actions workflow. The workflow validates the JSON against
`schema/submission.v1.json` and verifies that the filename matches the
`submission_id` field. Valid PRs receive the `valid` label and are
auto-merged with the squash strategy by the
[`auto-merge-valid`](.github/workflows/auto-merge-valid.yml) workflow. Invalid
PRs receive the `invalid` label and a sticky comment summarising the failure;
fix the issue locally, push a new commit, and the workflow re-runs.

After merge, the [`update-badges`](.github/workflows/update-badges.yml)
workflow refreshes the four dynamic counts shown in the badge row above
(submission total, distinct models, distinct scenarios, latest-submission
date). Optional mirror workflows (Hugging Face, Zenodo, Kaggle) propagate
the submission to public dataset repositories; see
[`docs/mirrors-setup.md`](docs/mirrors-setup.md) for the trust model. Two
optional notifier workflows (Discord, Telegram) can also announce new
submissions to project channels; see
[`docs/notifiers-setup.md`](docs/notifiers-setup.md).

The canonical personal-data scan runs **client-side** inside `puma
share-results` before the submission payload is ever constructed: the tool
inspects every free-text field against a rich catalogue of patterns and
refuses to build the payload if any match. The CI workflow's
defence-in-depth is intentionally narrow — schema validity plus filename
consistency — so the recommended submission path (`puma share-results`) is
the only trusted source of PII filtering.

## Repository structure

```
puma-community/
├── .github/workflows/    # GitHub Actions: validation, mirrors, notifiers, wiki sync
├── badges/               # Dynamic shields.io endpoint JSONs
├── docs/                 # Maintainer documentation
├── notebooks/            # Colab demo notebook and sample submission
├── schema/               # JSON Schema for submissions (v1.0.0)
├── scripts/              # Python helpers (badge generation, mirror, notify, notebook build)
├── submissions/          # Merged community submissions (one JSON file per submission)
├── wiki/                 # Source files for the GitHub Wiki
├── CODE_OF_CONDUCT.md    # Contributor Covenant v2.1
├── CONTRIBUTING.md       # How to submit your results
├── LICENSE               # MIT
├── MAINTAINERS.md        # Governance and current maintainers
└── README.md             # This file
```

## What is in a submission?

Every submission JSON carries:

- **Identification** — `submission_id` (UUIDv4), `submitted_at`,
  `schema_version`, `puma_version`.
- **Submitter** — `name_or_alias`, optional `affiliation` / `contact`,
  three consent booleans, and the `CC-BY-4.0` license clause.
- **Run metadata** — `scenario` (one of `triage_jira`, `effort_tawos`,
  `prioritization_jira`), `model`, `strategy`, instance count, seed,
  temperature, Ollama version, timestamps, and latency percentiles.
- **Hardware profile** — canonical `profile_id` from the PUMA catalog
  plus CPU / RAM / GPU details.
- **Metrics** — at least one of `f1_macro`, `mae`, or `accuracy`, plus
  optional per-class breakdowns and a confusion matrix.
- **Sustainability** — CodeCarbon emissions and tracking mode.
- **Integrity** — `predictions_summary_hash`, a deterministic SHA-256
  over the canonical CSV of the run's predictions joined on instance
  IDs.

See the [Wiki Submission Format](../../wiki/Submission-Format) page for the
field-by-field tour.

## Documentation

- [Submission schema](schema/submission.v1.json) — JSON Schema v1.0.0
  (Draft 2020-12).
- [Contributing guide](CONTRIBUTING.md) — submission flow, manual path,
  acceptance criteria.
- [Maintainer guide](docs/maintainer-guide.md) — exclusion lists, schema
  upgrades, mirror activation, wiki sync, demo notebook regeneration.
- [Mirrors setup](docs/mirrors-setup.md) — Hugging Face, Zenodo, Kaggle.
- [Notifiers setup](docs/notifiers-setup.md) — Discord, Telegram.
- [Colab demo](docs/colab-demo.md) — browser-based walkthrough.
- [Wiki](../../wiki) — end-user documentation, FAQ, submission-format
  explainer.

## Related projects

- **[PUMA Benchmark Tool](https://github.com/pumacp/puma)** — the
  local-LLM evaluation engine that produces submissions for this hub.
- **[Hugging Face mirror](https://huggingface.co/datasets/pumaproject/puma-community-submissions)**
  — read-only mirror of merged submissions.
- **[Zenodo snapshots](https://zenodo.org/communities/pumacp)** — DOI-stamped
  quarterly archives.
- **[Kaggle mirror](https://www.kaggle.com/datasets/pumacp/puma-community-submissions)**
  — weekly mirror for the data-science community.

## License

PUMA Community is released under the MIT License. See [`LICENSE`](LICENSE)
for the full text. Submissions remain attributable to their contributors via
the `submitter.name_or_alias` field, and are accepted under the `CC-BY-4.0`
clause embedded in the submitter consent block of the schema.

## Code of Conduct

This project follows the [Contributor Covenant v2.1](CODE_OF_CONDUCT.md).
Conduct concerns can be reported privately to
`pumacapstoneproject@gmail.com`.
