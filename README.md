# PUMA Community

![Submissions](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pumacp/puma-community/main/badges/submission-count.json)
![Schema](https://img.shields.io/badge/schema-v1.0.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Models](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pumacp/puma-community/main/badges/models-count.json)
![Scenarios](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pumacp/puma-community/main/badges/scenarios-count.json)
![Latest](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pumacp/puma-community/main/badges/latest-submission.json)

PUMA Community is a public submission hub for local-LLM benchmark results
produced by the open-source PUMA tool. Anyone can run a PUMA evaluation
locally and share their results with the community via a Pull Request to this
repository.

PUMA itself is a local, reproducible benchmarking framework for evaluating
open-weight language models on project-management tasks. Submissions in this
repository let researchers and practitioners compare model behaviour across
hardware profiles, tuning strategies, and scenarios without anyone needing to
re-run the underlying experiments.

---

## What is this repository?

This is a **data repository**: a curated, schema-validated archive of
community-contributed benchmark results.

- Each submission is a single JSON file under `submissions/`, keyed by a
  unique `submission_id`.
- Every file conforms to [`schema/submission.v1.json`](schema/submission.v1.json),
  a JSON Schema (Draft 2020-12) describing the canonical submission shape.
- Submissions are immutable once merged. Corrections are filed as new
  submissions that reference the older one (see
  [`submissions/README.md`](submissions/README.md)).

There is **no application code** in this repository. The benchmark tool that
produces these submissions lives in a separate project. Validation and
maintenance run entirely inside GitHub Actions on pull requests.

---

## How to submit your results

The recommended workflow uses the PUMA tool's built-in submission command:

```bash
# 1. Run a PUMA evaluation locally (see the PUMA tool docs).
# 2. Configure a GitHub Personal Access Token once:
puma auth login github

# 3. Preview the payload as a local file before opening a PR:
puma share-results --dry-run --run-id <run_id>

# 4. Open the PR on this repository:
puma share-results --run-id <run_id>
```

The tool builds the submission from your local SQLite results, validates it
against the schema, scans for personal data, signs an integrity hash over the
predictions, forks this repository on your behalf, creates a branch named
`submission/<submission_id>`, commits the JSON file, and opens a Pull
Request titled
`Submission <submission_id[:12]>: <scenario> / <model> / <strategy>`.

If you prefer to submit manually — for example, because you generated the
results with a different tool, or because you want to inspect every step —
see [`CONTRIBUTING.md`](CONTRIBUTING.md) for the manual path.

---

## How to browse submissions

All submissions live under [`submissions/`](submissions/). Each file is a
self-contained JSON document. The schema (see `schema/submission.v1.json`)
guarantees that every submission carries at least:

- **Identification:** `submission_id`, `submitted_at`, `schema_version`,
  `puma_version`.
- **Submitter:** `name_or_alias`, optional `affiliation` / `contact`, and the
  three consent fields (`consent_public_release`, `consent_redistribution`,
  `consent_research_use`).
- **Run metadata:** `scenario` (one of `triage_jira`, `effort_tawos`,
  `prioritization_jira`), `model`, `strategy`, instance count, seed,
  temperature, Ollama version, timestamps, and latency percentiles.
- **Hardware profile:** canonical `profile_id` plus CPU / RAM / GPU details.
- **Metrics:** scenario-specific quality metrics — at least one of
  `f1_macro`, `mae`, or `accuracy` is required, plus optional per-class
  breakdowns and a confusion matrix.
- **Sustainability:** CodeCarbon emissions (`co2_grams_total`,
  `energy_kwh_total`) and tracking mode.
- **Integrity:** `predictions_summary_hash` — a deterministic SHA-256 over
  the canonical CSV of the run's predictions, joined on instance IDs, that
  third parties can re-compute to verify the submission has not been
  tampered with after the fact.

Browse the directory in the GitHub web UI, clone the repository, or fetch
individual files via the raw URL — for example:

```
https://raw.githubusercontent.com/pumacp/puma-community/main/submissions/<submission_id>.json
```

---

## Validation policy

Every incoming Pull Request is processed automatically:

1. The `.github/workflows/validate-submission.yml` workflow checks each
   modified or added file under `submissions/`:
   - JSON Schema validation against `schema/submission.v1.json`.
   - Filename / `submission_id` field consistency.
   - A defence-in-depth scan for obvious personal data
     (email-shaped strings, phone-shaped strings, IPv4 addresses).
2. On success the PR receives the `valid` label and
   `.github/workflows/auto-merge-valid.yml` enables auto-merge with the
   squash strategy.
3. On failure the PR receives the `invalid` label and a sticky comment
   detailing the specific error.

The client-side `puma share-results` command runs a much richer set of
checks (full PII regex catalogue, integrity hash recomputation, model
exclusion list, anomaly heuristics on F1 and timestamps). The server-side
workflow is intentionally minimal — it acts as a safety net, not as the
primary gate.

See [`docs/maintainer-guide.md`](docs/maintainer-guide.md) for the
governance notes that complement this policy.

---

## What gets rejected

A submission will not be accepted if any of the following are detected:

- The JSON does not validate against `schema/submission.v1.json`.
- The filename does not match `submissions/<submission_id>.json`.
- The submission appears to contain personal data (email, phone, IP).
- The `submission_id` already exists in the repository (immutability).
- The model field references a model on the PUMA tool's exclusion list or
  pending-validation list (`puma share-results` refuses to build the
  payload in the first place).
- The `predictions_summary_hash` does not match the canonical computation
  the PUMA tool would produce for the same predictions.

If your PR is rejected, read the sticky comment, fix the issue locally, and
push a new commit; the workflow re-runs automatically.

---

## Governance

PUMA Community is maintained by volunteer contributors who keep the
validation workflows running, triage `governance` issues, and steward the
schema across versions. See [`MAINTAINERS.md`](MAINTAINERS.md) for the
current maintainer roster and the dispute-resolution process.

The design rationale behind this repository — separate-repo architecture,
dual-mode submission flow, defence-in-depth validation — is documented in
the PUMA tool's `docs/decisions/ADR-005-puma-community-architecture.md`.
That document is the authoritative reference for *why* this repository is
shaped the way it is.

---

## Schema reference

The canonical schema is [`schema/submission.v1.json`](schema/submission.v1.json).
It is generated from the Pydantic v2 models in the PUMA tool repository and
copied here byte-for-byte. The schema declares
`$schema = "https://json-schema.org/draft/2020-12/schema"` and
`$id = "https://pumacp.github.io/puma-community/schema/submission.v1.json"`.

Schema upgrades are versioned: future revisions land at `schema/submission.v2.json`,
`schema/submission.v3.json`, and so on. The v1 schema is preserved
indefinitely so that older submissions remain readable.

For end-user documentation, see the [PUMA Community Wiki](../../wiki).

---

## Code of conduct

This project follows the Contributor Covenant v2.1. See
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Conduct concerns can be
reported privately to `puma-community-conduct@pumacp.org`.

---

## License

PUMA Community is released under the MIT License — see
[`LICENSE`](LICENSE). Submissions are accepted under the
`CC-BY-4.0` clause embedded in the submitter consent block of the schema,
which permits redistribution and remix with attribution.
