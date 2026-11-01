# Mirrors setup

PUMA Community supports three optional outward mirrors: Hugging Face Dataset,
Zenodo DOI snapshot, and Kaggle Dataset. All three are **disabled by default**:
each workflow runs only on a manual `workflow_dispatch` trigger and skips
cleanly if its required secrets are absent.

To enable a mirror, configure the secrets listed below in the repository
settings (**Settings → Secrets and variables → Actions → New repository
secret**) and then trigger the workflow manually from the **Actions** tab.
Once you've confirmed it works end-to-end, you can opt into the recommended
schedule by uncommenting the `schedule:` block at the top of the workflow
YAML.

---

## Hugging Face Dataset

Workflow file: `.github/workflows/mirror-huggingface.yml`.

**Required secret:** `HF_TOKEN`.

1. Generate a Hugging Face access token with **write** scope on the
   `pumacp` namespace at
   <https://huggingface.co/settings/tokens>.
2. Add it to the repository as a secret named `HF_TOKEN`.
3. Trigger manually: **Actions → mirror-huggingface → Run workflow**.

The workflow uses the `huggingface_hub` Python API to create-or-update the
dataset `pumaproject/puma-community-submissions` and upload the contents of
`submissions/` into it. The commit message records the source SHA for
traceability.

---

## Zenodo DOI snapshot

Workflow file: `.github/workflows/mirror-zenodo.yml`
(helper script: `scripts/mirror_zenodo.py`).

**Required secret:** `ZENODO_TOKEN`.

1. Generate a Zenodo personal access token at
   <https://zenodo.org/account/settings/applications/>. Grant the
   `deposit:write` and `deposit:actions` scopes.
2. Add it to the repository as a secret named `ZENODO_TOKEN`.
3. Optionally set the repository variable `ZENODO_BASE_URL` to
   `https://sandbox.zenodo.org/api` while you're testing — the Zenodo
   Sandbox issues fake DOIs that don't pollute the production index. Leave
   it unset (or set it to `https://zenodo.org/api`) for real publications.
4. Trigger manually: **Actions → mirror-zenodo → Run workflow**.

The workflow builds a zip archive of `submissions/`, `schema/`, the README,
and the LICENSE, then publishes a new Zenodo deposition. Each run mints a
new DOI; previous snapshots stay available indefinitely on Zenodo.

---

## Kaggle Dataset

Workflow file: `.github/workflows/mirror-kaggle.yml`.

**Required secrets:** `KAGGLE_USERNAME` and `KAGGLE_KEY`.

1. Sign in to Kaggle and visit <https://www.kaggle.com/settings>.
2. Under the **API** section, click **Create new token**. Your browser will
   download a `kaggle.json` file containing two fields: `username` and
   `key`.
3. Add `KAGGLE_USERNAME` and `KAGGLE_KEY` to the repository secrets,
   matching the values from `kaggle.json` byte-for-byte.
4. Trigger manually: **Actions → mirror-kaggle → Run workflow**.

The workflow uses the official `kaggle` CLI to either create the dataset
`pumacp/puma-community-submissions` on the first run, or push a new version
on subsequent runs.

---

## Trust model

These mirrors push data **outward only**. They do not modify the canonical
repository state, do not interact with the validation workflow, and never
read secrets back out of the runner environment. If a mirror is
misconfigured or the target service is unavailable, the workflow exits with
a clear error message and the canonical repository remains untouched —
submissions accumulate in `submissions/` exactly as before.

All three workflows are gated on their respective secrets. A workflow with
missing secrets prints a "Skipping: …" message and exits 0 without making
any external request, so accidentally clicking **Run workflow** on a
freshly-cloned fork is harmless.

---

## Schedule activation

Once you've verified a mirror manually, opt into the recommended schedule
by uncommenting the `schedule:` block at the top of its YAML file:

- `mirror-huggingface.yml` — daily at 03:00 UTC.
- `mirror-zenodo.yml` — quarterly at 04:00 UTC on the 1st of Jan / Apr /
  Jul / Oct.
- `mirror-kaggle.yml` — weekly on Sundays at 05:00 UTC.

These cadences are starting points; adjust to suit your community's load
and your service quotas.
