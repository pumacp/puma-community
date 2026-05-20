# Security Policy

## Reporting a Vulnerability

If you believe you have found a security vulnerability in the PUMA
Community submission infrastructure, please **do not** open a public
GitHub Issue. Instead, report it privately by email to:

**pumacapstoneproject@gmail.com**

Include in your report:

- A description of the vulnerability and its potential impact.
- Steps to reproduce, or a minimal proof-of-concept.
- Any suggested mitigation, if applicable.

We will acknowledge receipt within 7 days and aim to provide a
remediation plan within 30 days for confirmed vulnerabilities.

## Scope

In scope:

- The submission JSON Schema (`schema/submission.v1.json`) and the
  validation workflows in `.github/workflows/`.
- The auto-merge logic (`auto-merge-valid.yml`).
- The mirror and notification workflows (when activated).
- The badge generation scripts in `scripts/`.

Out of scope (use a regular GitHub Issue instead):

- Disputes about the scientific validity of a specific submission.
  Submissions are accepted in good faith; correctness of the
  underlying experiment is the submitter's responsibility.
- Requests to remove a submission. Open a regular Issue labelled
  `removal`.

## Trust model

PUMA Community operates under a good-faith collaborative model:

- Schema validation enforces the structure of submissions but does
  not verify the truthfulness of the metrics. A determined actor
  could submit fabricated results that pass schema validation.
- Cryptographic integrity (SHA-256 over the predictions summary)
  detects accidental corruption and post-submission tampering but
  does not certify that the metrics correspond to a real run.
- The PII scanner in the local client (`puma share-results`)
  reduces but does not eliminate the risk of accidental PII
  inclusion. Submitters remain responsible for verifying their
  submissions before publishing.

Future versions may introduce signed submissions with public-key
identity. For v1 the model is explicitly "good-faith collaboration".

## Auto-merge safety

The auto-merge workflow applies a path filter: only Pull Requests that
modify exclusively files under `submissions/` are eligible for
automatic merge. Any PR touching `.github/`, `schema/`, `scripts/`,
`docs/`, or any other path requires manual review by a maintainer.

## Disclosure timeline

We follow a coordinated disclosure approach: once a fix is published,
we wait at least 14 days before publishing the full vulnerability
details.
