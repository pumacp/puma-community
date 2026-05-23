---
license: cc-by-4.0
language:
  - en
tags:
  - benchmark
  - llm-evaluation
  - project-management
  - local-llm
  - sustainability
  - issue-triage
  - effort-estimation
size_categories:
  - n<1K
pretty_name: PUMA Community Submissions
viewer: true
---

# PUMA Community Submissions

Community-contributed benchmark results from [PUMA](https://github.com/pumacp/puma) — an empirical evaluation platform for **local LLM agents on Project Management Office (PMO) tasks**.

## What you'll find here

Each submission is a JSON file under `submissions/` containing the result of a PUMA benchmark run on one of the supported scenarios:

- **triage_jira** — issue triage on the Jira Social Repository ([Zenodo DOI](https://doi.org/10.5281/zenodo.5901893)), reported as F1-macro
- **effort_tawos** — story point effort estimation on TAWOS, reported as MAE in story points
- **prioritization_jira** — issue prioritization, reported as nDCG@10 *(community-eval, optional)*

Each submission includes:

- Run metadata (model, prompting strategy, scenario, seed, temperature)
- Hardware profile (CPU-only / GPU / Apple Silicon variant)
- Metrics with bootstrap confidence intervals
- Sustainability data (kWh consumed, gCO₂eq via CodeCarbon)
- Optional `raw_predictions_url` for integrity verification

## Live leaderboard

Interactive view with filters, scatter plots, and verified badges:

👉 [pumaproject/puma-leaderboard](https://huggingface.co/spaces/pumaproject/puma-leaderboard)

## Schema

The canonical JSON Schema lives in the governance repo:

[`schema/submission.v1.json`](https://github.com/pumacp/puma-community/blob/main/schema/submission.v1.json)

Minimal example:

```json
{
  "schema_version": "1.0.0",
  "submission_id": "sub_2026_001",
  "submitter": {
    "github_handle": "pumacp",
    "affiliation": "UOC"
  },
  "run_metadata": {
    "scenario": "triage_jira",
    "model": "qwen2.5:3b",
    "prompting": "few_shot_3",
    "seed": 42,
    "temperature": 0.0
  },
  "hardware_profile": {
    "type": "cpu_only",
    "ram_gb": 16
  },
  "metrics": {
    "f1_macro": 0.5867,
    "ci_lower": 0.5612,
    "ci_upper": 0.6122
  },
  "sustainability": {
    "kwh": 0.0074,
    "co2_g": 3.075
  },
  "raw_predictions_url": "https://github.com/pumacp/puma-community/raw/main/raw/sub_2026_001.jsonl",
  "predictions_summary_hash": "sha256:..."
}
```

## How submissions get here

1. A community member runs `puma share-results --run-id <id>` locally
2. PUMA opens a pull request on [pumacp/puma-community](https://github.com/pumacp/puma-community)
3. Automated validation checks schema, hash integrity, and reproducibility metadata
4. Once merged, a GitHub Action mirrors the file to this dataset automatically
5. The leaderboard Space refreshes within ~5 minutes

## Trust model

This dataset is built on a **transparency, not gatekeeping** principle:

- Every submission carries enough metadata to reproduce the run locally
- An optional `raw_predictions_url` allows the [verifier Space](https://huggingface.co/spaces/pumaproject/puma-verifier) to recompute the SHA-256 over the predictions and emit a `verified: true` sidecar in GitHub
- Verification is **integrity-only** — it does not re-execute the model
- Unverified submissions remain visible but are flagged in the leaderboard

## Canonical sources

| Resource | Location |
|---|---|
| Source code | [github.com/pumacp/puma](https://github.com/pumacp/puma) |
| Governance & PR flow | [github.com/pumacp/puma-community](https://github.com/pumacp/puma-community) |
| Live leaderboard | [pumaproject/puma-leaderboard](https://huggingface.co/spaces/pumaproject/puma-leaderboard) |
| Citable snapshots (quarterly) | Zenodo DOI *(to be published in Q3 2026)* |

## Citation

```bibtex
@misc{puma2026,
  title  = {PUMA: Project Understanding and Management with Agents},
  author = {{PUMA Project Contributors}},
  year   = {2026},
  url    = {https://github.com/pumacp/puma}
}
```

## License

- **Submission data**: [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)
- **PUMA source code**: [MIT](https://github.com/pumacp/puma/blob/main/LICENSE)
