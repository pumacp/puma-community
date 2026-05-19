# Maintainers

The maintainer team is responsible for keeping the validation workflows
healthy, triaging governance issues, and stewarding the submission schema
across versions.

## Current maintainers

| Name   | GitHub handle | Areas                           |
|--------|---------------|---------------------------------|
| Daniel | _TBD_         | schema, workflows, governance   |

The handle column will be filled in when the repository is first published.
Additional maintainers may be added by consensus of the current team and
will be appended above with the same row format.

## Proposing changes

- **Governance and policy questions** — open an issue labelled
  `governance`. Examples: dispute over a rejected submission, proposal to
  change the validation policy, request to add a new maintainer.
- **Schema updates** — see
  [`docs/maintainer-guide.md`](docs/maintainer-guide.md). Schema upgrades
  are coordinated with the PUMA tool repository, since the canonical
  schema is generated there from Pydantic models.
- **Exclusion-list updates** — see
  [`docs/maintainer-guide.md`](docs/maintainer-guide.md). The exclusion
  list lives in the PUMA tool repository; this repository does not
  duplicate it.

## Dispute resolution

Validation disputes are handled in three steps:

1. The submitter opens an issue labelled `governance` referencing the
   rejected PR.
2. A maintainer triages within seven days, either re-running validation,
   explaining the rejection, or escalating to the full team.
3. The full team decides by simple majority; tie-breaks favour rejection
   (defence-in-depth bias on a public submission repository).

The complete operational procedure — adding models to the exclusion list,
flagging models as pending validation, bumping the schema — lives in
[`docs/maintainer-guide.md`](docs/maintainer-guide.md).
