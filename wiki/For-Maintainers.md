# For Maintainers

This page is for people who hold write access to `pumacp/puma-community` and
operate the validation pipeline. It documents schema versioning, workflow
control, mirror activation, and the operational procedures for handling
edge cases.

## Schema versioning

The canonical submission schema lives at `schema/submission.v1.json`
(Draft 2020-12). Any non-additive change is a **breaking change** and
requires a new major version (e.g., `submission.v2.json`) plus a documented
migration path for existing submitters.

Additive, non-breaking changes (new optional fields, widened enum values)
can stay on `v1.json` but must be reviewed for downstream consumer impact
before merging.

## Releasing a schema update

1. Edit `schema/submission.v1.json` (or create `submission.v2.json` for
   breaking changes).
2. Recompute the SHA-256 of the file:
   ```bash
   sha256sum schema/submission.v1.json
   ```
3. Update the byte-identical copy bundled in the PUMA tool at
   `src/puma/community/schema_data/submission.v1.json` in the
   `pumacp/puma` repository.
4. Bump the `SCHEMA_VERSION` constant in both repositories so the local
   validator and the CI validator agree.
5. Tag a new PUMA Community release and add a CHANGELOG entry.

## Disabling a misbehaving workflow

In the GitHub Actions UI: select the workflow, click the **⋯** menu, and
choose **Disable workflow**. This is reversible from the same menu. Use
this when an upstream dependency (action, secret rotation) is causing a
flood of failed runs.

## Activating mirrors

Add the following secrets via **Settings → Secrets and variables → Actions**:

- `HF_TOKEN` — Hugging Face access token with `write` scope on
  `pumaproject/puma-community-submissions`.
- `ZENODO_TOKEN` — Zenodo personal access token with `deposit:write`.
- `KAGGLE_USERNAME` and `KAGGLE_KEY` — Kaggle credentials with dataset
  write access.

The mirror workflows detect the secrets at run time and become active on
the next push.

## Activating notifications

Same UI:

- `DISCORD_WEBHOOK_URL` — webhook for the Discord channel that should
  receive merge notifications.
- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` — Telegram bot credentials
  for the broadcast channel.

## Removing a submission

If a submitter requests withdrawal:

1. Confirm the request comes from the submitter (check the alias against
   any side channel they used to contact you).
2. Open a removal PR that deletes the relevant file under `submissions/`.
3. Label the PR `removal` so the badge job knows to decrement counts.
4. Merge.

The next push to `main` triggers `update-badges`, which refreshes the
counts to match the new archive state.

## Contact

For governance questions, schema policy decisions, or contested
submissions, write to `pumacapstoneproject@gmail.com`.
