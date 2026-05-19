# PUMA Community Wiki

Welcome to the PUMA Community Wiki. This is the end-user-facing reference for
contributors who want to submit local-LLM benchmark results to the public
submission hub, and for readers who want to interpret the JSON documents
under `submissions/`. Maintainer-facing operational notes live in
`docs/maintainer-guide.md` in the main repository.

PUMA itself is a local, reproducible benchmarking framework for evaluating
open-weight language models on project-management tasks. PUMA Community is
the public archive of evaluation runs that PUMA users have chosen to share.

## Pages

- [Submission Format](Submission-Format) — what's inside a submission JSON,
  what every field means, and which values are accepted.
- [FAQ](FAQ) — answers to the most common questions about validation,
  immutability, supported hardware, model exclusions, integrity hashes, and
  the optional outward mirrors.

## Quick links

- **Submit your results:** see
  [`CONTRIBUTING.md`](https://github.com/pumacp/puma-community/blob/main/CONTRIBUTING.md)
  for the recommended `puma share-results` workflow and the manual path.
- **Browse submissions:** the canonical archive lives under
  [`submissions/`](https://github.com/pumacp/puma-community/tree/main/submissions)
  on the main branch.
- **Schema:** the canonical JSON Schema is
  [`schema/submission.v1.json`](https://github.com/pumacp/puma-community/blob/main/schema/submission.v1.json).
- **Project README:** see the
  [main README](https://github.com/pumacp/puma-community/blob/main/README.md)
  for the high-level overview and badges.

## Reporting problems

Open an issue in the
[main repository](https://github.com/pumacp/puma-community/issues). Use the
`governance` label for disputes over rejected submissions, model exclusions,
or schema policy. Use the default label for everything else (typo reports,
documentation gaps, workflow bugs).
