# VisionGuard.ai — Minimal Test Suite (tesing)

This folder contains lightweight `unittest` smoke tests for the backend.

## Run

From the repository root:

- `python -m unittest -v tesing.test_backend_smoke`

## Outputs

Test outputs should be stored in `tesing/results/`.

## Notes

- These tests do **not** require a running database.
- The tests add `backend-visionguard-ai/` to `sys.path` at runtime to import backend modules as `app.*`.
