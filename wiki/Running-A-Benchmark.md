# Running a Benchmark

This page is a short overview of running PUMA locally so you have a result
worth submitting. For the complete reference, see the
[PUMA Wiki](https://github.com/pumacp/puma/wiki).

## Install

```bash
git clone https://github.com/pumacp/puma.git
cd puma
docker compose up -d
```

## Pull a model

```bash
docker compose exec puma_ollama ollama pull qwen2.5:3b
```

You can swap `qwen2.5:3b` for any Ollama tag. The curated catalog is listed
under `puma models`; off-catalog models are accepted but flagged as
"experimental" when submitted.

## Run a benchmark

```bash
docker compose run --rm puma_runner puma run \
  --scenario triage_jira \
  --model qwen2.5:3b \
  --strategy zero_shot \
  --instances 10
```

The run writes its predictions and metrics to the local SQLite database and
prints a final summary. Make a note of the **run ID** in the output; you'll
need it when submitting.

## Configuration options that matter for sharing

- **`--scenario`** must be one of the catalog values: `triage_jira`,
  `effort_tawos`, `prioritization_jira`. Off-catalog scenarios cannot be
  submitted.
- **`--model`** should ideally be from the curated PUMA catalog. Off-catalog
  models are accepted but marked `experimental: true` in the submission
  metadata so other users know the model's provenance hasn't been vetted by
  the project.
- **`--strategy`** must be one of the supported strategies: `zero_shot`,
  `few_shot_3`, `few_shot_6`, `chain_of_thought`, `rcoif`,
  `contextual_anchoring`.
- **`--instances`** should be **at least 10** for a publishable result.
  Smaller runs are accepted but flagged in the submission metadata so
  readers know the metrics come from a small sample.

## Next

Continue with [Submitting Results](Submitting-Results) to publish what you
just ran.
