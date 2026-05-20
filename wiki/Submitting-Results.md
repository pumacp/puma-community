# Submitting Your Results

This page walks through the full submission flow: prerequisites, creating a
GitHub Personal Access Token, authenticating the local PUMA client,
dry-running the submission, and publishing.

## Prerequisites

- PUMA installed locally (see [Running a Benchmark](Running-A-Benchmark)) and
  at least one completed run.
- A GitHub account.
- A GitHub Personal Access Token (PAT) — instructions below.

## Create your PAT

1. Go to `https://github.com/settings/tokens?type=beta` and click
   **Generate new token (fine-grained)**.
2. **Repository access**: select only `pumacp/puma-community`. Do not give
   the token access to your other repositories.
3. **Permissions**:
   - `Contents`: Read and write
   - `Pull requests`: Read and write
   - `Metadata`: Read (this is automatic and required)
4. **Token name** and **expiration**: pick whatever you like. A 90-day
   expiration is a sensible default.
5. Click **Generate token** and copy it once. The token starts with
   `github_pat_`. You will not see it again, so paste it into the next step
   immediately.

## Authenticate the local client

```bash
docker compose run --rm puma_runner puma auth login
```

Paste the PAT when prompted. The token is stored at
`~/.puma/credentials.toml` with file mode `0600`, so only your user can read
it. To check the stored credentials:

```bash
docker compose run --rm puma_runner puma auth whoami
```

## Dry-run first

Always dry-run before publishing. The dry-run builds the full submission
JSON, runs the PII scanner, and saves the artifact under
`data/community/submissions/` without opening a PR:

```bash
docker compose run --rm puma_runner puma share-results \
  --dry-run --run-id <your_run_id> --yes
```

Inspect the generated JSON. Confirm:

- The metrics are what you expect.
- Your submitter alias is what you want shown publicly.
- No unexpected fields contain anything sensitive (the PII scanner blocks
  this automatically, but a visual check is cheap).

## Publish

```bash
docker compose run --rm puma_runner puma share-results \
  --run-id <your_run_id> --yes
```

This creates a Pull Request on `https://github.com/pumacp/puma-community`
from your fork. The PR description includes the submission summary, the
integrity hash, and a link to the schema version it conforms to.

## What you'll see

- The PR URL is printed once the command succeeds.
- A green check appears under the PR once schema validation and integrity
  verification finish (usually within a minute).
- A "merged" label appears within a few minutes once auto-merge runs.
- Your submission count contributes to the badges on the repository README
  on the next badge refresh.

## If validation fails

Click **Details** on the failed check to see the validation error. The most
common causes are:

- A schema field is out of its allowed range (for example, a probability
  outside `[0, 1]` or a count below 1).
- The integrity hash does not match the predictions — usually a sign that
  the submission JSON was edited by hand after generation.
- The model tag is not in the curated catalog and the submission was not
  marked as experimental.

Fix the issue locally and re-run `share-results`. A new PR will be opened
(or the existing one updated, if your branch is still active).
