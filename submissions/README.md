# Submissions

This directory holds one JSON file per accepted submission. Every file
conforms to [`../schema/submission.v1.json`](../schema/submission.v1.json).

## Filename convention

```
submissions/<submission_id>.json
```

The `<submission_id>` is a UUIDv4 (or, in future schema revisions, a
content-addressed hash). The validation workflow rejects any PR where the
filename does not match the `submission_id` field inside the JSON document.

## Immutability

Files in this directory are **immutable once merged**. Maintainers will not
edit a merged submission to apply corrections, redactions, or stylistic
changes. To correct a previously submitted result, file a **new** submission
with a fresh `submission_id`.

A future schema revision will introduce a `supersedes` field so a corrected
submission can point at the older `submission_id` it replaces. v1 documents
do not carry this field; the convention is forward-compatible and will be
back-fillable without breaking older readers.

## Sort order

Files are listed lexically by `submission_id`. Tooling that consumes the
directory should sort the same way for reproducible output.

## Browsing

To read a submission directly without cloning, fetch the raw URL:

```
https://raw.githubusercontent.com/pumacp/puma-community/main/submissions/<submission_id>.json
```
