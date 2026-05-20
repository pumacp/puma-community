# Why PUMA Community?

## The reproducibility problem

Local LLM benchmarks are intrinsically tied to the hardware they ran on. The
same model on different machines produces slightly different latency,
different energy figures, and occasionally different outputs if randomness is
not fully controlled. Public leaderboards rarely capture the consumer-hardware
profiles that matter most for practitioners — a $400 GPU, a five-year-old
laptop, an Apple Silicon Mac mini — and even when they do, the results are
not independently verifiable. Without a place to publish and verify
hardware-stratified benchmarks, the local-LLM ecosystem fragments into
isolated reports that nobody can compare directly.

## What PUMA Community offers

- **A public archive of verified submissions** across the full
  model × scenario × hardware-profile matrix. Each submission is a JSON
  document committed to the repository with a stable, citable URL.
- **Cryptographic integrity.** Every submission carries a SHA-256 hash over
  a deterministic summary of its predictions. The validation pipeline
  recomputes the hash before accepting the PR, so metrics cannot be silently
  altered from the predictions they claim to describe.
- **Schema-validated structure.** The submission JSON is validated against
  `schema/submission.v1.json` (Draft 2020-12). Every field is typed, every
  numeric range is bounded, and unknown fields are rejected — there is no
  free-form bag for ad-hoc metadata.
- **Anonymous by default.** The submitter alias is a free-form string of
  your choice. Your GitHub username, IP address, hostname, and file system
  paths are all omitted by the local validator before the submission is
  signed.
- **Zero centralized infrastructure.** The archive lives in this Git
  repository. Validation runs in GitHub Actions. There is no separate
  database, no server, no API key beyond your GitHub PAT.

## Why your contribution matters

Each submission adds a data point to a dataset that benefits everyone
evaluating local LLMs for ICT project management tasks. **Hardware diversity
is especially valuable**: a result from a `cpu-lite` profile is as
scientifically meaningful as one from `gpu-pro`, and exactly that diversity
is what's missing from existing benchmarks. **Reproducibility verification
emerges naturally**: when two independent submitters report matching metrics
for the same configuration, that pairing is empirical evidence that PUMA's
determinism guarantees hold on real hardware in the wild.

## How collaboration works

The flow is intentionally simple: you submit a Pull Request from your local
client, the validation workflows run, and on success the PR auto-merges.
A badge-update job refreshes the submission count, model count, and
scenario count on the repository README. The full mechanics are described in
[Submitting Results](Submitting-Results) and [Validation Process](Validation-Process).
