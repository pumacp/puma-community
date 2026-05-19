# Colab demo

PUMA Community ships a Colab-ready demo notebook so prospective contributors
can preview a submission without installing PUMA locally. The notebook walks
through downloading the v1 schema, validating a sample submission, inspecting
metrics and sustainability data, and browsing the community archive via the
anonymous GitHub API.

## Run in Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pumacp/puma-community/blob/main/notebooks/puma_community_demo.ipynb)

Clicking the badge opens the notebook directly in Google Colab. The first
cell installs `jsonschema`; every subsequent cell uses only the Python
standard library.

## What the demo covers

- How a PUMA submission is structured (field-by-field tour).
- How to validate a submission against the v1 schema.
- How to inspect metrics and sustainability data.
- How to browse all community submissions via the anonymous GitHub API
  (subject to GitHub's 60-requests-per-hour anonymous rate limit).
- How to submit your own results via `puma share-results` or the manual
  Pull Request path.

## Requirements

A modern web browser is the only requirement. No PUMA installation, no
GitHub account, no API token. The notebook reads only from the public
repository.

## Run locally with Jupyter

If you'd rather run the notebook on your own machine:

```bash
pip install jupyter jsonschema==4.23.0
jupyter notebook notebooks/puma_community_demo.ipynb
```

## Regenerate the notebook

The notebook is built programmatically from
[`scripts/build_demo_notebook.py`](../scripts/build_demo_notebook.py). To
update its contents, edit the script and run:

```bash
python3 scripts/build_demo_notebook.py
```

Commit both the script change and the regenerated `.ipynb`.
