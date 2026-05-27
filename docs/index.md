<p align="center">
  <img src="assets/img/PUMA.png" alt="PUMA logo" width="240">
</p>

<p align="center"><strong>Public submission hub for community-contributed local-LLM benchmark results in ICT Project Management.</strong></p>

<p align="center">
  <a href="https://github.com/pumacp/puma-community/actions/workflows/validate-submission.yml"><img src="https://github.com/pumacp/puma-community/actions/workflows/validate-submission.yml/badge.svg" alt="Validate submissions"></a>
  <a href="https://github.com/pumacp/puma-community/actions/workflows/docs.yml"><img src="https://github.com/pumacp/puma-community/actions/workflows/docs.yml/badge.svg?branch=main" alt="Docs CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-111111" alt="License: MIT">
  <img src="https://img.shields.io/badge/schema-v1.0.0-111111" alt="Schema v1.0.0">
  <br>
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pumacp/puma-community/main/badges/submission-count.json" alt="Submissions">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pumacp/puma-community/main/badges/models-count.json" alt="Models">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pumacp/puma-community/main/badges/scenarios-count.json" alt="Scenarios">
  <br>
  <a href="https://huggingface.co/datasets/pumaproject/puma-community-submissions"><img src="https://img.shields.io/badge/%F0%9F%A4%97-Dataset-111111" alt="Hugging Face dataset"></a>
  <a href="https://huggingface.co/spaces/pumaproject/puma-leaderboard"><img src="https://img.shields.io/badge/%F0%9F%A4%97-Leaderboard-111111" alt="Leaderboard"></a>
  <a href="https://zenodo.org/communities/pumacp"><img src="https://img.shields.io/badge/Zenodo-DOI-111111" alt="Zenodo"></a>
</p>

<!-- PUMA-ACROSTIC-BLOCK START — DO NOT MODIFY — IMMUTABLE -->
---
**F**ollowing empirical evidence, ICT project management faces triage, estimation, and learning inefficiencies.<br>
**O**bserved widely, these persist despite abundant historical data.<br>
**L**aying a rigorous foundation requires reproducible benchmarking.<br>
**L**everaging labeled datasets enables systematic evaluation of LLM performance.<br>
**O**utcomes are compared using quantitative metrics and statistical analysis.<br>
**W**ith an incremental design, a minimal viable benchmark is defined.<br>
**T**hrough open-source release, results become reproducible and verifiable.<br>
**H**ence, the framework supports extensibility across models and tasks.<br>
**E**ventually, it enables integration into real organizational settings.<br>
**W**ithin ICT environments, recurring inefficiencies hinder effective decision-making.<br>
**H**eterogeneous data sources complicate prioritization and estimation processes.<br>
**I**n response, this work builds a reproducible LLM-based benchmark.<br>
**T**he focus is on issue triage and story-point estimation tasks.<br>
**E**valuation follows controlled experiments with statistical validation.<br>
**P**rotocols ensure reproducibility through fixed parameters and configurations.<br>
**U**sing carbon tracking, the framework measures energy impact.<br>
**M**oreover, the MVP delivers a valid and original contribution.<br>
**A**ll artefacts are released as open source for replication and extension.<br>
---
<!-- PUMA-ACROSTIC-BLOCK END -->

<p align="center">
  <a href="#how-to-contribute"><strong>Submit your results</strong></a> ·
  <a href="https://huggingface.co/spaces/pumaproject/puma-leaderboard"><strong>Browse the leaderboard</strong></a> ·
  <a href="#submission-format"><strong>Read the schema</strong></a>
</p>

## What is PUMA Community?

PUMA Community is the **public, cryptographically-verifiable archive** of
community-contributed benchmark results produced by the
[PUMA benchmark tool](https://github.com/pumacp/puma). Anyone can run PUMA on
their own hardware, generate a submission, and publish it here for others to
discover, cite, and reproduce.

The hub is **serverless by design**: all of its infrastructure runs on free
services — GitHub Actions for validation and merge, Hugging Face Spaces for the
leaderboard and verifier, and Zenodo for DOI-backed archival. Submissions are
auto-validated against a JSON Schema, auto-merged when valid, and mirrored
outward to external archives so downstream researchers and tool builders can
find them where they already work.

## Why a public submission hub?

- **Cryptographic integrity** — every submission carries a deterministic SHA-256 hash over its predictions, recomputable and verifiable by anyone.
- **FAIR data** — findable (Hugging Face mirror), accessible (CC-BY-4.0), interoperable (JSON Schema), reusable (open, forever).
- **Citable** — DOI-backed Zenodo snapshots make every submission academically citable.
- **Reproducible** — each submission records seed, temperature, model version, hardware profile, and sustainability cost.
- **Open** — zero vendor lock-in, zero paid API dependencies, MIT-licensed.

## The submission pipeline

```text
puma share-results  →  PR (submissions/<id>.json)  →  validate-submission CI
        │                                                      │
        │                                              valid?  ├─ no → "invalid" label + comment
        ▼                                                      ▼ yes
  local JSON package                                    "valid" label
                                                               │
                                          auto-merge-valid  →  main  →  update-badges
                                                               │
                              mirrors (HF / Zenodo / Kaggle) ──┤── notifiers (Discord / Telegram)
                                                               │
                                              verify-submission → <id>.verified.json
```

1. Run `puma share-results --dry-run` locally — this generates the submission JSON.
2. Open a pull request adding `submissions/<id>.json`.
3. The **validate-submission** workflow checks schema, filename, and integrity hash.
4. Valid PRs receive the `valid` label.
5. The **auto-merge-valid** workflow squash-merges them into `main`.
6. The **update-badges** workflow refreshes the live counters.
7. **Mirror** workflows (when secrets are configured) propagate to Hugging Face, Zenodo, and Kaggle.
8. **Notify** workflows (when secrets are configured) announce to Discord and Telegram.
9. The **verify-submission** sidecar computes an independent verification badge.

## Submission format

Each submission is a single JSON document conforming to schema **v1.0.0**:

- **Identification** — `submission_id` (UUIDv4), `schema_version`, `puma_version`.
- **Submitter consent** — explicit CC-BY-4.0 release flags.
- **Run metadata** — scenario, model, strategy, seed, temperature.
- **Hardware profile** — a canonical `profile_id` from the PUMA catalog.
- **Metrics** — F1-macro, MAE, accuracy.
- **Sustainability** — CodeCarbon-measured emissions.
- **Integrity** — `predictions_summary_hash`.

See the [submission format guide](submission-format.md) for the full
field-by-field tour.

## Validation guarantees

!!! info "Every merged submission satisfies three guarantees"
    1. **Schema conformance** — validates against `schema/submission.v1.json` (JSON Schema Draft 2020-12).
    2. **Filename consistency** — the file name must match the `submission_id` field.
    3. **Integrity** — `predictions_summary_hash` is recomputed server-side and compared to the declared value.

PRs that fail any guarantee receive the `invalid` label with a sticky comment
summarizing the failure.

## The mirror network

| Channel | Target | Status |
|---|---|---|
| Hugging Face Datasets | `pumaproject/puma-community-submissions` | mirror active when `HF_TOKEN` is configured |
| Zenodo community | `pumacp` | sandbox validated; production pending the first DOI |
| Kaggle dataset | `pumacp/puma-community-submissions` | prepared, dormant — activated by trigger |

Each mirror has its own GitHub Actions workflow under `.github/workflows/`,
runs on its own schedule, and is gated by the secret it requires.

## The verifier pipeline

Verification is independent of the original submitter:

- The Hugging Face Space [`puma-verifier`](https://huggingface.co/spaces/pumaproject/puma-verifier) (private endpoint) replicates the **byte-identical** hashing algorithm from the PUMA client.
- The `verify-submission` workflow detects new submissions via `git diff` and invokes the verifier.
- Each submission gets a sidecar `<id>.verified.json` next to it.
- Verification status renders as a badge in the leaderboard.

**Trust model:** cryptographic hashing makes tampering detectable, and the
verifier is independent of the submitter — so a published result can be trusted
without trusting the person who submitted it.

## How to contribute

```bash
# 1. Run PUMA locally and generate a submission
puma run specs/runs/baseline_triage.yaml
puma share-results

# 2. Fork puma-community and create a branch
gh repo fork pumacp/puma-community
cd puma-community && git checkout -b my-submission

# 3. Add the submission JSON
cp ~/.puma/submissions/<id>.json submissions/<id>.json

# 4. Validate locally (optional but recommended)
python -m jsonschema -i submissions/<id>.json schema/submission.v1.json

# 5. Open the PR
git add submissions/<id>.json && git commit -m "Add submission <id>"
git push origin my-submission && gh pr create --fill
```

See the [contributing guide](contributing.md) for the long-form walkthrough.

## The community

- **Discord** — [discord.gg/fVhcpHREJv](https://discord.gg/fVhcpHREJv)
- **GitHub Discussions** — on this [repository](https://github.com/pumacp/puma-community/discussions).
- **Contribute** — start with the [contributing guide](contributing.md).
- **Report issues** — open an issue on the relevant repository.

## Trust model & Code of Conduct

- All submissions are released under **CC-BY-4.0** with attribution.
- The project enforces the **Contributor Covenant v2.1**.
- Personal-data scanning runs **client-side** in `puma share-results`, before a
  submission payload is ever constructed.
- The CI's defense-in-depth is intentionally narrow (schema + filename + hash),
  so the recommended client path remains the trusted source.

## Roadmap

The hub grows along trigger-based horizons rather than fixed dates:

| Horizon | Milestone | Trigger | Status |
|---|---|---|---|
| H1 | Hub live, CI green, docs published | Public launch | **complete** |
| H2 | First external community submissions | Outside contributors open PRs | pending external submissions |
| H3 | DOI-backed snapshots | First Zenodo production deposit | planned |
| H4 | Mirror activation (HF / Zenodo / Kaggle) | Secrets configured | designed |
| H5 | Notifications (Discord / Telegram) | Webhook/bot secrets configured | designed |
| H6 | Verifier at scale | Sustained submission volume | designed |

## Resources

### Code repositories
- **PUMA benchmark tool** — <https://github.com/pumacp/puma>
- **PUMA Community** — <https://github.com/pumacp/puma-community>
- **PUMA Vault** — <https://github.com/pumacp/puma-vault>

### Documentation sites
- **PUMA Community** — <https://pumacp.github.io/puma-community/>
- **PUMA docs** — <https://pumacp.github.io/puma/>
- **PUMA Vault** — <https://pumacp.github.io/puma-vault/>
- **Wiki (community)** — <https://github.com/pumacp/puma-community/wiki> · **Wiki (tool)** — <https://github.com/pumacp/puma/wiki>

### Hugging Face Hub
- **Organization** — <https://huggingface.co/pumaproject>
- **Dataset of submissions** — <https://huggingface.co/datasets/pumaproject/puma-community-submissions>
- **Leaderboard (Gradio Space)** — <https://huggingface.co/spaces/pumaproject/puma-leaderboard>
- **Verifier (private endpoint)** — <https://huggingface.co/spaces/pumaproject/puma-verifier>
- **Personal namespace** — <https://huggingface.co/pumacp>

### Persistent archives & catalogs
- **Zenodo community (production)** — <https://zenodo.org/communities/pumacp>
- **Zenodo community (sandbox)** — <https://sandbox.zenodo.org/communities/pumacp>
- **Source dataset (Jira Social Repository)** — <https://doi.org/10.5281/zenodo.5901893>
- **Kaggle dataset** — <https://www.kaggle.com/datasets/pumacp/puma-community-submissions>

### Knowledge management & research
- **Zotero library** — <https://www.zotero.org/pumacp/library>
- **Google Drive (PDF repository)** — <https://drive.google.com/drive/folders/1TKbYhYqLIrq7liAPISF7ztS2Bv0l7vZS?usp=sharing>
- **ResearchRabbit map 1** — <https://app.researchrabbit.ai/folder-shares/d8244f17-47f7-4f6c-a589-473876578b54>
- **ResearchRabbit map 2** — <https://app.researchrabbit.ai/folder-shares/b6c00471-2f28-4c66-85f5-ab5399470228>

### Conversation
- **Discord** — <https://discord.gg/fVhcpHREJv>
- **Contact** — pumacapstoneproject@gmail.com

## Citation

If you use PUMA Community submissions as a data source, please cite the archive:

```bibtex
@misc{puma_community,
  title        = {PUMA Community: a public archive of community-contributed LLM benchmark results for ICT Project Management},
  author       = {{The PUMA Project}},
  year         = {2026},
  howpublished = {\url{https://github.com/pumacp/puma-community}},
  note         = {Zenodo DOI forthcoming}
}
```

!!! note
    A Zenodo DOI is forthcoming and will be appended here after the first
    DOI-backed snapshot.

---

<!-- PUMA-ACROSTIC-BLOCK START — DO NOT MODIFY — IMMUTABLE -->
---
**F**ollowing empirical evidence, ICT project management faces triage, estimation, and learning inefficiencies.<br>
**O**bserved widely, these persist despite abundant historical data.<br>
**L**aying a rigorous foundation requires reproducible benchmarking.<br>
**L**everaging labeled datasets enables systematic evaluation of LLM performance.<br>
**O**utcomes are compared using quantitative metrics and statistical analysis.<br>
**W**ith an incremental design, a minimal viable benchmark is defined.<br>
**T**hrough open-source release, results become reproducible and verifiable.<br>
**H**ence, the framework supports extensibility across models and tasks.<br>
**E**ventually, it enables integration into real organizational settings.<br>
**W**ithin ICT environments, recurring inefficiencies hinder effective decision-making.<br>
**H**eterogeneous data sources complicate prioritization and estimation processes.<br>
**I**n response, this work builds a reproducible LLM-based benchmark.<br>
**T**he focus is on issue triage and story-point estimation tasks.<br>
**E**valuation follows controlled experiments with statistical validation.<br>
**P**rotocols ensure reproducibility through fixed parameters and configurations.<br>
**U**sing carbon tracking, the framework measures energy impact.<br>
**M**oreover, the MVP delivers a valid and original contribution.<br>
**A**ll artefacts are released as open source for replication and extension.<br>
---
<!-- PUMA-ACROSTIC-BLOCK END -->

PUMA Community is released under the **MIT License**. Built with
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/). See also the
[PUMA benchmark tool docs](https://pumacp.github.io/puma/).
