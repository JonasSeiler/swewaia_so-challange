# 003 — Data Fetcher Tests

**Date**: 2026-03-23
**Tool**: VS Code GitHub Copilot Chat
**Model**: GPT-5.3-Codex
**Iterations**: 1

## Prompt

**2026-03-23 15:56**

Write pytest tests for `data_fetcher.py`. The module should:
- Fetch monthly SO question counts (2008-2024)
- Return a pandas DataFrame with columns: year_month, question_count
- Cache results locally as CSV
- Handle network errors gracefully

Write the tests BEFORE the implementation. Use unittest.mock to
mock API/network calls in tests. Include tests for:
- Successful data fetch returns correct DataFrame shape
- Cached data is returned without network call
- Network error triggers retry logic

Save the diary entry and commit everything with a proper commit
message describing what was added.
