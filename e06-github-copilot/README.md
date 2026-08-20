# E6 — GitHub Copilot & GitHub at the state of the art

**Phase:** P1 (Jul–Aug) · **Est:** 3.5h · **Planned:** 2026-08-19 → 2026-08-22

> 🎯 Outcome: Use Copilot in the IDE; open a PR with Actions (CI) on a practice repo.

**Course:** [GitHub Skills — getting-started-with-github-copilot](https://skills.github.com/)

## Scope

Git and GitHub are already familiar, so the hours go to the two things that are new:
Copilot chat in the IDE, and a CI workflow that actually runs on GitHub. The practice
repo is this one — no throwaway sandbox.

**Starting position:** `.github/workflows/ci.yml` was written during E3 (commit `99ed152`)
but never pushed, so Actions has never run here. Landing it through a real PR is what
closes two of the three boxes below.

## Definition of done

- [ ] Copilot used in-IDE on real code
- [x] A PR opened with CI (Actions) passing
- [x] A working `ci.yml` committed

## Practical project

Write a function with Copilot's help on the `journey` CLI, add a test for it, push this
branch, open a PR, and watch the Actions run go green before merging.

## Study blocks

| Block | Hours |
|---|---|
| Thu 2026-08-20, 19:00–21:00 | 2h |
| Sat 2026-08-22, 10:00–11:30 | 1.5h |
| **Total** | **3.5h** |

The 3.5h total matches the plan's 0.5-day estimate. The dates are self-imposed — the
program plan carries durations and phases only, no calendar.

## What was actually built

**CI, finally running.** `.github/workflows/ci.yml` was written during E3 (commit `99ed152`)
and had sat local ever since. The push was refused every time:

```
! [remote rejected] refusing to allow an OAuth App to create or update
  workflow `.github/workflows/ci.yml` without `workflow` scope
```

The `gh` token carried `gist, read:org, repo` — GitHub blocks any push touching
`.github/workflows/` without `workflow` on top. So 18 commits stayed on the laptop and
Actions had never run on this repo. `gh auth refresh -h github.com -s workflow` fixed it.

The lesson is the failure mode, not the fix: the workflow was correct for two weeks and the
repo still had no CI, because a *push* was rejected rather than a *build*. Nothing in the
local tooling flags that — `journey status` was happily green the whole time.

[PR #3](https://github.com/Abderrahmanehaouate/ai-engineer-journey/pull/3) landed it. First
run passed green: `e03 - journey CLI` (ruff → mypy → pytest) plus the repo-wide
`journey status --strict` drift gate.

**Still open:** `actions/checkout@v4` and `actions/setup-python@v5` target Node.js 20, now
deprecated and force-run on Node 24. Bump to `checkout@v5` / `setup-python@v6`.

## Notes

_To fill in — where Copilot helped, where it hallucinated, and how it compares to reaching
for Claude Code instead._
