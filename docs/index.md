# PUMA Community

PUMA Community is the public archive of community-contributed benchmark results
for the [PUMA](https://github.com/pumacp/puma) project — a curated, verifiable
record of how local, open-weight LLMs perform on ICT Project Management tasks.

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

## Quick start

To contribute a result, follow the [Submitting results](contributing.md) guide —
it walks through generating a submission with the upstream
[PUMA benchmark tool](https://github.com/pumacp/puma) and opening a pull request.
Every submission is validated against the schema before it is merged and mirrored.

## Documentation map

- [Submitting results](contributing.md) — how to contribute a benchmark result.
- [Submission format](submission-format.md) — field-by-field tour of the schema.
- [Mirrors setup](mirrors-setup.md) — Hugging Face, Zenodo, and Kaggle mirrors.
- [Notifiers setup](notifiers-setup.md) — Discord and Telegram notifications.
- [Maintainer guide](maintainer-guide.md) — operating the hub.
- [Colab demo](colab-demo.md) — try the flow in a notebook.

### Related repositories

- [PUMA benchmark tool](https://github.com/pumacp/puma) · [docs](https://pumacp.github.io/puma/)
- [PUMA Vault](https://github.com/pumacp/puma-vault) · [docs](https://pumacp.github.io/puma-vault/)

---

This site is built with MkDocs Material and deployed automatically via GitHub
Actions on every push to `main`.
