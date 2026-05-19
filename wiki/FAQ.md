# FAQ

Frequently asked questions about contributing to PUMA Community. For the
operational view (workflows, schema upgrades, exclusion list management),
see `docs/maintainer-guide.md` in the main repository.

## How is my submission validated?

Every Pull Request that adds or modifies a file under `submissions/`
triggers the `validate-submission` GitHub Actions workflow. The workflow
checks two things:

1. The JSON validates against
   [`schema/submission.v1.json`](https://github.com/pumacp/puma-community/blob/main/schema/submission.v1.json).
2. The filename matches the `submission_id` field
   (`submissions/<submission_id>.json`).

If both checks pass, the workflow adds the `valid` label and the
`auto-merge-valid` workflow enables GitHub's native auto-merge with the
squash strategy. If either fails, the workflow adds the `invalid` label and
posts a sticky PR comment with the error details. Fix the issue locally,
push a new commit, and the workflow re-runs automatically.

Note that the canonical PII scan runs **client-side** in
`puma share-results`, not in the CI workflow. The CI step is intentionally
narrow: schema validity plus filename consistency.

## Can I update or correct my submission later?

Merged submissions are **immutable**. The validation workflow refuses
modifications to existing files for the same reason — historical results
must remain stable so that downstream analyses, leaderboards, and DOIs stay
trustworthy.

To publish a correction, open a new submission with a fresh
`submission_id`. A future schema revision (v2) will add a `supersedes`
field so a corrected submission can point at the older one it replaces;
v1 documents do not carry this field but the convention is
forward-compatible and back-fillable without breaking existing readers.

## What hardware profiles are supported?

The schema validates `hardware_profile.profile_id` against the canonical
PUMA catalog at
[`config/profiles.yaml`](https://github.com/pumacp/puma/blob/main/config/profiles.yaml).
The current catalog ships 15 profile IDs: five baselines (`cpu-lite`,
`cpu-standard`, `gpu-entry`, `gpu-mid`, `gpu-high`) plus ten Apple Silicon
variants covering the M3, M4, and M5 generations (`apple-silicon-m3`,
`apple-silicon-m3-pro`, `apple-silicon-m3-max`, …,
`apple-silicon-m5-ultra`).

See the [Submission Format](Submission-Format#hardware-profiles) page for
the full list.

## Why was my model rejected?

The PUMA tool maintains two lists in its `builder.py`:

- A **hard exclusion list** — models that the project has decided not to
  accept submissions for (typically because of unresolved reproducibility
  concerns).
- A **pending-validation list** — models that are catalogued but have not
  yet been empirically validated on PUMA's reference hardware. These are
  detected via the sentinel text `"Empirical validation status: pending"`
  in the model's `notes` field of
  [`config/models_catalog.yaml`](https://github.com/pumacp/puma/blob/main/config/models_catalog.yaml).

If `puma share-results` refused to build a submission for your model, one
of those two lists was the cause. To request a re-evaluation, open an
issue with the `governance` label in the main repository and link to the
upstream catalog entry.

## How is the integrity hash computed?

`integrity.predictions_summary_hash` is a SHA-256 over the canonical CSV
serialisation of the run's predictions, joined to the corresponding
instances and sorted by `instance_id` ascending. The same predictions
always produce the same hash regardless of insertion order, machine, or
Python version.

The hash protects against accidental tampering: if a maintainer (or anyone
else) edits a merged submission after the fact, the hash will no longer
match a re-computation, and anyone verifying the submission can detect
the change.

## Where else can I find PUMA Community data?

Three optional outward mirrors push merged submissions to:

- **Hugging Face Datasets** — `pumacp/puma-community-submissions`.
- **Zenodo** — versioned DOI snapshots.
- **Kaggle** — `pumacp/puma-community-submissions`.

All three are disabled by default and run only on manual
`workflow_dispatch`. See
[`docs/mirrors-setup.md`](https://github.com/pumacp/puma-community/blob/main/docs/mirrors-setup.md)
for setup instructions and the trust model.
