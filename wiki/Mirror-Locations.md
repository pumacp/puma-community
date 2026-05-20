# Mirror Locations

PUMA Community submissions can optionally be mirrored to external archives
for long-term accessibility, citation, and easy programmatic discovery. The
canonical source is always this GitHub repository; mirrors are downstream
copies refreshed automatically by GitHub Actions when the corresponding
secrets are configured.

## Planned mirrors

- **Hugging Face Datasets** at `pumacp/puma-community-submissions`. Each
  accepted submission becomes a row in a Parquet-backed dataset. Use case:
  programmatic discovery, filtering, and analytical queries via the
  `datasets` library.
- **Zenodo community `pumacp`**. Monthly DOI-backed snapshots of the
  full archive, suitable for academic citation.
- **Kaggle dataset** at `pumacp/puma-community-submissions`. Mirror in the
  Kaggle dataset catalog so that Kaggle Notebooks can attach the archive
  directly.

## Status

Mirrors are infrastructure-ready but **not yet populated**. Each mirror has
its own GitHub Actions workflow under `.github/workflows/` (`mirror-huggingface.yml`,
`mirror-zenodo.yml`, `mirror-kaggle.yml`), each gated on a repository secret
that the project maintainers have not yet provided. Until activation, the
GitHub repository remains the canonical and only source.

## How to query the mirrors once active

Once Hugging Face is populated:

```python
from datasets import load_dataset
ds = load_dataset("pumacp/puma-community-submissions", split="train")
```

Once Kaggle is populated:

```bash
kaggle datasets download pumacp/puma-community-submissions
```

For Zenodo, browse the community at `https://zenodo.org/communities/pumacp`
(once activated) and download the most recent snapshot directly from there.
Each snapshot has a stable DOI suitable for citation.
