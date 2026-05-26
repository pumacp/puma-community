# Maintainer guide

Operational reference for maintainers. This file describes how to perform
the recurring tasks the community repository requires; the policy rationale
sits in `MAINTAINERS.md` and the user-facing rules in `CONTRIBUTING.md`.

## Adding a model to the exclusion list

The canonical exclusion list lives in the PUMA tool repository at
`src/puma/community/builder.py`, in the `_HARD_EXCLUDED_MODELS`
`frozenset`. This community repository deliberately does **not** duplicate
that list, so we cannot drift from the tool over time.

To add a model:

1. Open a PR on the PUMA tool repository that adds the Ollama tag to
   `_HARD_EXCLUDED_MODELS`, with a rationale in the commit body.
2. Once that PR lands, open an issue here labelled `governance` summarising
   the exclusion. Include a link to the upstream commit.
3. Existing submissions referencing the excluded model are **not**
   retroactively removed. New submissions for that model will be rejected
   client-side by `puma share-results` before they can even reach this
   repository.

## Pending-validation models

A model is "pending validation" when its `notes` field in the PUMA tool's
`config/models_catalog.yaml` contains the exact substring:

```
Empirical validation status: pending
```

The PUMA tool's builder scans for this marker and refuses to construct a
submission for any pending model. As with exclusions, this repository does
not duplicate the list. To flag or unflag a model, edit the catalog in the
PUMA tool repository and open an informational issue here labelled
`governance`.

## Updating the schema

The schema in `schema/submission.v1.json` is **generated** from the
Pydantic v2 models in the PUMA tool repository. Do not hand-edit it.

To publish a schema upgrade:

1. In the PUMA tool repository, modify the Pydantic models under
   `src/puma/community/schema.py`.
2. Run `scripts/regenerate_submission_schema.py` to regenerate the JSON
   Schema artifact and refresh the on-disk copy.
3. Copy the regenerated file here as `schema/submission.v2.json` (or the
   next major version). Do **not** overwrite `submission.v1.json`; the v1
   schema is preserved indefinitely so older submissions remain readable.
4. Open a PR with a migration note: which fields changed, whether the
   change is backward-compatible, and whether the validation workflow
   needs to dispatch on `schema_version`.

## Validation policy and PII handling

The CI workflow `validate-submission.yml` performs only:

- JSON Schema validation against `schema/submission.v1.json`.
- A filename-matches-`submission_id` check.

It does **not** scan for personally identifiable information server-side.
The canonical PII scan runs **client-side** inside `puma share-results`,
before the submission payload is ever constructed: the tool inspects
`notes`, `submitter.affiliation`, and `submitter.contact` against a rich
catalogue of patterns and refuses to build the payload if any match.

This is a defence-in-depth gap accepted for v1 simplicity. v2 will add a
server-side PII scan that mirrors the client-side patterns; until then,
the recommended submission path (`puma share-results`) is the only
trusted source of PII filtering.

## Validation workflow trust model

`validate-submission.yml` labels each PR `valid` or `invalid` based on the
schema-validation outcome. `auto-merge-valid.yml` triggers on the `valid`
label and enables GitHub's native auto-merge with the squash strategy.

**v1 limitation:** any actor with write access to this repository can
also add the `valid` label manually. Auto-merge will trigger regardless
of which actor added the label. Maintainers are trusted not to bypass the
validation workflow.

**v2 plan:** restrict the `auto-merge-valid.yml` trigger to label events
whose `sender.type == "Bot"` and whose `sender.login` matches the GitHub
App identity that owns `validate-submission.yml`. This requires
provisioning a dedicated GitHub App for the repository, which is out of
scope for v1.

## Badge refresh

`update-badges.yml` runs on every push to `main` that touches
`submissions/*.json`. It rewrites `badges/submission-count.json` in the
shields.io endpoint schema and commits the result back to `main` as
`puma-community-bot <pumacapstoneproject@gmail.com>`. If the badge content does not
change, the workflow exits without committing.

## Releasing the repository

The community repository does not cut versioned releases. The schema
version (`schema/submission.v1.json`) is the only versioned artifact;
schema upgrades follow the procedure above.

## Mirrors

PUMA Community supports three optional outward mirrors:

- **Hugging Face Dataset** (`mirror-huggingface.yml`)
- **Zenodo DOI snapshot** (`mirror-zenodo.yml`)
- **Kaggle Dataset** (`mirror-kaggle.yml`)

All three are disabled by default. They run only on manual `workflow_dispatch`
and skip if their required secrets are absent. See
[`docs/mirrors-setup.md`](mirrors-setup.md) for setup instructions and the
trust model.

## Notifiers

PUMA Community supports two optional outward notifiers that announce new
submissions to project channels:

- **Discord webhook** (`notify-discord.yml`)
- **Telegram bot** (`notify-telegram.yml`)

Both are disabled by default. They run only on manual `workflow_dispatch`
and skip if their required secrets are absent. See
[`docs/notifiers-setup.md`](notifiers-setup.md) for setup instructions and
the trust model.

## Dynamic badges

PUMA Community displays four dynamic badges in the README, sourced from
`badges/*.json` in this repository:

- **submissions** — total count of merged submissions.
- **models** — distinct models covered.
- **scenarios** — distinct scenarios covered.
- **latest** — date of the most recent submission.

The badges are regenerated automatically by the `update-badges` workflow on
every push to `main` that touches `submissions/*.json`. The workflow calls
`scripts/generate_badges.py`, which can also be run locally to inspect the
output.

## Wiki

The Wiki content is version-controlled under `wiki/` in this repository. To
publish a change:

1. Edit the relevant page under `wiki/` and open a PR (same workflow as any
   other file).
2. After the PR is merged to `main`, manually trigger the `wiki-sync`
   workflow from the Actions tab (Actions → wiki-sync → Run workflow).
3. The workflow clones the GitHub Wiki repo, rsyncs `wiki/` into it,
   commits, and pushes.

**Pre-condition**: the repository's Wikis feature must be enabled in
Settings → Features → Wikis. The Wiki must have at least one page (any
content) before the first sync; create a stub page via the GitHub web UI
if needed.

## Demo notebook

The Colab demo notebook lives at `notebooks/puma_community_demo.ipynb` and
is generated from `scripts/build_demo_notebook.py`. To update it:

1. Edit `scripts/build_demo_notebook.py` (cells are constructed
   programmatically).
2. Run the generator: `python3 scripts/build_demo_notebook.py`.
3. Commit both the script change and the regenerated `.ipynb`.

The sample submission used by the notebook lives at
`notebooks/sample_submission.json`. It must remain valid against
`schema/submission.v1.json`. If the schema changes in a way that breaks the
sample, update the sample and re-validate locally with `python3 -c "import
json, jsonschema;
jsonschema.validate(json.load(open('notebooks/sample_submission.json')),
json.load(open('schema/submission.v1.json')))"` before committing.

## Oracle Cloud auxiliary deployment (v2)

PUMA Community v1 is fully serverless. A future v2 may add an optional
always-on auxiliary service hosted on Oracle Cloud Always Free, providing
a read-only HTTP API and a static leaderboard. The design proposal lives
at [`docs/oracle-cloud-deployment.md`](https://github.com/pumacp/puma-community/blob/main/docs/oracle-cloud-deployment.md). It is
NOT implemented as of v1.0.0; the design is captured so a future
maintainer can pick it up.
