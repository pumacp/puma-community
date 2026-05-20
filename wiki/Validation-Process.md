# What Happens After You Submit

When you publish a submission, several automated steps run before it lands
on `main`. The whole pipeline finishes in a few minutes for typical
submissions.

## Step 1 — Pull Request creation

Your local PUMA client opens a Pull Request from your fork (or from a
branch on `pumacp/puma-community` if you have write access) targeting
`main`. The PR title is `submission: <model> · <scenario> · <profile>`.
The PR description embeds a human-readable summary of the submission and a
link to the integrity hash.

## Step 2 — Schema validation

The `validate-submission` workflow runs `jsonschema` against
`schema/submission.v1.json` (Draft 2020-12). It checks:

- Every required field is present.
- Every field is of the declared type.
- Every numeric field is inside its declared range.
- The submitter alias is non-empty and ASCII-printable.
- The PUMA version matches the supported range.

Typical duration: ~30 seconds.

## Step 3 — Integrity verification

The same workflow recomputes the SHA-256 hash over the submission's
predictions summary and compares it to the declared hash. If they differ,
the submission is rejected — this catches both accidental file corruption
and any deliberate edit to the metrics after generation.

## Step 4 — Auto-merge

If schema validation and integrity verification both pass, the
`auto-merge-valid` workflow merges the PR automatically. There is no human
gate in the path because the validation is fully deterministic — the same
input always produces the same accept/reject decision.

## Step 5 — Badge update

The `update-badges` workflow refreshes the four badges that appear at the
top of the repository README:

- **Submissions** — total accepted submission count.
- **Models** — number of distinct model tags represented.
- **Scenarios** — number of distinct scenarios represented (currently 3).
- **Latest submission** — date of the most recent accepted submission.

The badges are committed back to `main` by the workflow and are typically
visible within a minute of the merge.

## Optional mirrors

If the maintainers have configured the optional Hugging Face, Zenodo, or
Kaggle secrets, the submission is mirrored to those archives via additional
workflows. The status of each mirror is tracked in
[Mirror Locations](Mirror-Locations).
