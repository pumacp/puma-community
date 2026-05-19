# Submission Format

Every submission is a JSON document conforming to
[`schema/submission.v1.json`](https://github.com/pumacp/puma-community/blob/main/schema/submission.v1.json)
(JSON Schema Draft 2020-12). The schema is the single source of truth; this
page is a human-friendly summary.

## Top-level fields

| Field             | Type          | Description                                                                 |
|-------------------|---------------|-----------------------------------------------------------------------------|
| `schema_version`  | string        | Always `"1.0.0"` for v1 submissions.                                        |
| `submission_id`   | string (UUID) | UUIDv4. The filename under `submissions/` must match: `<submission_id>.json`. |
| `submitted_at`    | datetime      | UTC timestamp the payload was assembled. Auto-set by `puma share-results`. |
| `puma_version`    | string        | SemVer of the PUMA tool that produced the submission.                       |
| `submitter`       | object        | Identity and consent block (see below).                                     |
| `run_metadata`    | object        | Scenario, model, strategy, timing, latency.                                 |
| `hardware_profile`| object        | Canonical hardware profile and detected specifications.                     |
| `metrics`         | object        | Scenario-specific quality metrics.                                          |
| `sustainability`  | object        | CodeCarbon emissions (CO₂, energy).                                         |
| `integrity`       | object        | Deterministic SHA-256 over the run's predictions.                           |
| `notes`           | string \| null| Optional free-text. PII is rejected client-side before submission.          |
| `raw_predictions_url` | string \| null | Optional pointer to the raw per-prediction archive.                  |

### `submitter`

- `name_or_alias` (string, 3-64 chars, `[A-Za-z0-9_\-\.]+`).
- `affiliation` (optional, max 128 chars).
- `contact` (optional, max 128 chars).
- `consent_public_release`, `consent_redistribution`, `consent_research_use`
  (all three must be `true`).
- `license` (`"CC-BY-4.0"`).

### `run_metadata`

- `scenario` — one of `triage_jira`, `effort_tawos`, `prioritization_jira`.
- `model` — Ollama tag (e.g. `qwen2.5:3b`).
- `strategy` — one of the canonical snake_case strategy values (see below).
- `n_instances` — number of evaluation instances (1-100000).
- `seed`, `temperature`, `ollama_version`.
- `started_at` / `completed_at` — UTC timestamps. `completed_at >= started_at`.
- `latency_ms_total`, `latency_ms_p50`, `latency_ms_p95` — must satisfy
  `p95 >= p50 >= 0`.

### `metrics`

At least one of `f1_macro`, `mae`, or `accuracy` must be present:

- `f1_macro`, `accuracy` — `[0.0, 1.0]`.
- `mae`, `mdae` — `>= 0.0`.
- `ece` — `[0.0, 1.0]`.
- `f1_per_class`, `confusion_matrix` — optional structured fields.

### `sustainability`

- `codecarbon_version`, `tracking_mode` (`"machine"` or `"process"`),
  `country_iso` (3-letter ISO 3166-1 alpha-3 uppercase).
- `co2_grams_total`, `energy_kwh_total` — non-negative floats.

### `integrity`

- `predictions_summary_hash` — lowercase 64-char hex SHA-256, computed by
  `puma share-results` over the canonical CSV of the run's predictions.
- `payload_signature` — optional, reserved for future signing schemes.
- `verification_status` — `"unverified"`, `"self-attested"`,
  `"community-verified"`. Defaults to `"self-attested"`.

## Hardware profiles

The schema validates `hardware_profile.profile_id` against the canonical
PUMA catalog at
[`config/profiles.yaml`](https://github.com/pumacp/puma/blob/main/config/profiles.yaml)
in the academic tool repository. The current catalog ships 15 profile IDs:
five baselines (`cpu-lite`, `cpu-standard`, `gpu-entry`, `gpu-mid`,
`gpu-high`) plus ten Apple-Silicon variants spanning the M3 / M4 / M5
generations (`apple-silicon-m3`, `apple-silicon-m3-pro`,
`apple-silicon-m3-max`, …, `apple-silicon-m5-ultra`).

## Scenarios

- `triage_jira` — issue classification using Jira issue text. Quality is
  measured with `f1_macro` and `accuracy`; the confusion matrix is the
  authoritative breakdown.
- `effort_tawos` — story-point estimation using the TAWOS dataset. Quality
  is measured with `mae` / `mdae`; large outliers dominate `mae`, so
  `mdae` is reported alongside.
- `prioritization_jira` — backlog prioritisation. Quality is measured with
  scenario-specific accuracy.

## Strategies

The schema accepts nine canonical strategies (snake_case): `zero_shot`,
`zero_shot_cot`, `few_shot_3`, `few_shot_6`, `cot_few_shot`, `rcoif`,
`contextual_anchoring`, `egi`, `self_consistency`. The PUMA tool's CLI
accepts kebab-case (e.g. `zero-shot`) and translates to snake_case at
submission time.

## Example (abridged)

```json
{
  "schema_version": "1.0.0",
  "submission_id": "4f2a8d1c-9b3e-4d8a-9b1c-aaaaaaaaaaaa",
  "submitted_at": "2026-05-18T10:00:00+00:00",
  "puma_version": "2.7.0",
  "submitter": { "name_or_alias": "alice_42", ... },
  "run_metadata": {
    "scenario": "triage_jira",
    "model": "qwen2.5:3b",
    "strategy": "zero_shot",
    "n_instances": 200,
    ...
  },
  "hardware_profile": { "profile_id": "gpu-entry", ... },
  "metrics": { "f1_macro": 0.5867, "accuracy": 0.62 },
  "sustainability": { "co2_grams_total": 12.5, ... },
  "integrity": { "predictions_summary_hash": "aaaa...64hex" }
}
```
