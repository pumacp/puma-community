# Contributing to PUMA Community

Thanks for sharing your benchmark results. This document covers the two
supported submission paths — the **recommended** path that uses the PUMA
tool's built-in command, and the **manual** path for advanced users who want
full control of every step.

Before you start, please read [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
By submitting a Pull Request you agree to the licensing terms in
[`LICENSE`](LICENSE) and to the consent fields encoded in your submission
payload (public release, redistribution, research use).

---

## Recommended: submit via `puma share-results`

The PUMA tool is the easiest and safest way to file a submission. It builds
the payload from your local SQLite results, validates the schema, scans for
personal data, computes the integrity hash, forks this repository, creates
the branch, commits the JSON file, and opens the Pull Request — all in one
command.

```bash
# 1. Store a GitHub Personal Access Token (PAT) once.
#    Required scopes: public_repo (or repo if you want to use a private fork).
puma auth login github

# 2. Preview the payload locally before touching GitHub. The file lands in
#    data/community/submissions/<submission_id>.json by default.
puma share-results --dry-run --run-id <your_run_id>

# 3. Once you are happy with the preview, open the PR.
puma share-results --run-id <your_run_id>
```

The tool prints the PR URL on success. If anything goes wrong (rate-limit
exhausted, GitHub API error, conflict on an existing branch), re-run with
`--dry-run` and inspect the saved payload before retrying.

Optional flags worth knowing about:

- `--submitter-alias <alias>` — override the default alias. Defaults to a
  slug of your GitHub login in publish mode and `anonymous-<hex8>` in
  dry-run mode.
- `--yes` / `-y` — skip the interactive consent prompt. Use only when you
  have already reviewed the payload via `--dry-run`.
- `PUMA_SUBMITTER_ALIAS` — environment-variable equivalent of
  `--submitter-alias`.

---

## Manual submission (advanced users)

If you generated the results with a different tool, or you want to inspect
every step of the submission yourself, you can craft and submit the payload
by hand.

### 1. File naming

Save your JSON file as `submissions/<submission_id>.json` where
`<submission_id>` is a UUIDv4 string. The validation workflow rejects
PRs where the filename does not match the `submission_id` field inside the
JSON.

### 2. Schema validation

Validate locally before opening the PR. The same schema runs in CI:

```bash
pip install jsonschema==4.23.0
python -m jsonschema -i submission.json schema/submission.v1.json
```

If the command exits silently, your submission is well-formed.

### 3. Pull Request title

Use the canonical title format so reviewers can scan the PR list at a
glance:

```
Submission <submission_id[:12]>: <scenario> / <model> / <strategy>
```

For example:
`Submission 4f2a8d1c9b3e: triage_jira / qwen2.5:3b / zero_shot`.

### 4. Pull Request body

Fill in the template at `.github/PULL_REQUEST_TEMPLATE.md`. The required
fields are the submission ID, the run summary (scenario / model / strategy),
the tool that generated the payload, and the three confirmation checkboxes.

### 5. Push and open the PR

Fork this repository, push your branch named `submission/<submission_id>`
to your fork, and open the PR against `main`. The validation workflow runs
automatically; expect a comment within a minute.

---

## What gets rejected

A submission is rejected when **any** of the following holds:

- The JSON does not validate against `schema/submission.v1.json`.
- The filename does not match `submissions/<submission_id>.json`.
- The submission contains personal data — email-shaped strings,
  phone-shaped strings, or IP addresses are flagged in CI. The PUMA tool's
  client-side scan is stricter; running `puma share-results --dry-run`
  first is the safest way to catch this before the PR opens.
- The `submission_id` already exists in the repository. Submissions are
  immutable; corrections must use a fresh `submission_id`.
- The `predictions_summary_hash` cannot be reproduced from the predictions
  the submitter claims to have run. The PUMA tool computes this hash
  deterministically; tampering with the JSON after the fact is detectable.
- The model is on the PUMA tool's exclusion list or pending-validation
  list. See `docs/maintainer-guide.md` for the canonical list location.

If your PR is rejected, fix the issue locally and push a new commit; the
workflow re-runs and the labels update automatically.

---

## Code of conduct

All interactions on this repository — issues, pull requests, discussions —
are governed by the [Contributor Covenant v2.1](CODE_OF_CONDUCT.md).
Concerns can be reported privately to
`pumacapstoneproject@gmail.com`.
