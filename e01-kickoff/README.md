# E1 — Kickoff + full environment setup

**Phase:** P1 (Jul–Aug) · **Est:** 3.5h · **Planned:** 2026-07-27 → 2026-07-30

> 🎯 Outcome: Environment 100% operational; you know your path and deadlines.

## Definition of done

- [ ] All 4 accounts created and verified (Anthropic, GitHub, Hugging Face, Microsoft Learn)
- [x] Claude Code installed and running
- [x] `ai-engineer-journey` repo created with README + schedule
- [x] Weekly study blocks on the calendar

## What was actually set up

| Item | Detail |
|---|---|
| Claude Code | Running on Windows 11, model Opus 5 |
| Git | 2.54.0.windows.1 |
| GitHub CLI | 2.97.0, installed via `winget install --id GitHub.cli` |
| GitHub auth | Device flow → token in Windows keyring; scopes `gist`, `read:org`, `repo` |
| Git identity | `Abderrahman Haouate <abderrahmanehaouate@gmail.com>` |
| Credential helper | `gh auth setup-git` — HTTPS push/pull works without prompts |
| Secret hygiene | `.gitignore` blocks `.env` from commit #1; `.env.example` is the template |

## Notes

The `.env` habit was built before there was anything to leak — that was the point of
doing it on day one rather than the first time an API key showed up.

Hugging Face and Microsoft Learn accounts are created. Microsoft Learn is smoke-tested —
first AI-900 module started, so the learning path shows progress against the account.

Remaining: the Hugging Face smoke test (log in, create one dummy Space or model repo),
then put the three weekly blocks on the calendar as recurring events.
