# E3 — Claude Code 101

**Phase:** P1 (Jul–Aug) · **Est:** 3.5h · **Planned:** 2026-07-31 → 2026-08-04

> 🎯 Outcome: Install/configure Claude Code, use it on a real task, and write a `CLAUDE.md`.

**Course:** [Anthropic Academy — Claude Code 101](https://anthropic.skilljar.com/claude-code-101)

## Definition of done

- [x] Claude Code configured on a real repo
- [x] One real task done end-to-end (explore → plan → code → commit)
- [x] `CLAUDE.md` written and committed

## Practical project

Point Claude Code at this repo and have it scaffold a small Python CLI here, add
tests, and make a commit. Then write a `CLAUDE.md` at the repo root capturing the
stack, conventions, and do-not-touch areas.

## What was actually built

**`journey` — a status CLI for this repo.** Zero runtime dependencies, stdlib only.

```
journey status [--repo PATH] [--strict]
```

It reads two sources and compares them:

| Source | What it gives | Trustworthiness |
|---|---|---|
| Root `README.md` task tables | ID, name, estimate, ⬜/🔄/✅ glyph | *Mirrored* — a human has to remember to update it |
| Each `e*/README.md` "Definition of done" | Ticked / unticked checkboxes | *Observed* — moves when the work moves |

Observed status is derived: all boxes ticked → `DONE`, some → `DOING`, none or no
directory → `TODO`. Where mirrored disagrees with observed, the report prints **DRIFT**
and names both sides. `--strict` exits non-zero, so it can gate CI.

| Module | Lines | Role |
|---|---|---|
| `journey/parse.py` | 170 | Markdown → `Task` records; scopes checkboxes to the DoD section |
| `journey/report.py` | 85 | Text rendering and program totals |
| `journey/cli.py` | 57 | Argument handling and exit codes |
| `tests/` | 286 | 28 cases across parse / report / cli |

Gates: **28 pytest passing**, `ruff check` clean, `mypy --strict` clean.

Two decisions worth recording. Output is **ASCII only** — a Windows console codepage is
not always UTF-8, and a status tool that crashes printing its own status glyphs is worse
than no tool; there is a test asserting this. Markdown is read as **explicit UTF-8** for
the same reason, since these files contain `—`, `·`, `→`, and `✅`.

**It found a real error on first run:** the root README claimed 146.5h of total effort
while the task rows summed to 147h. That number had been wrong since E1. Fixed.

## Notes

The Explore → Plan → Code → Commit loop worked as advertised. Framing the task and
reviewing the diff is the job now; the typing is not the bottleneck. Planning the scope
before any code got written is what kept this from becoming a generic to-do-app exercise.

Picking a tool that reads *this* repo was the highest-value choice made here. It gave the
tests something real to assert against instead of `add(2, 2) == 4`, and it attacks a
problem the program actually has — status living in three places (Notion, root README,
task checkboxes) and drifting between them.

The quality gates earned their place: `ruff` caught a line-length violation that a human
review would have waved through, and `mypy --strict` passed only because the types were
written up front rather than retrofitted.

What went into `CLAUDE.md` as a result: the per-task directory and README structure, the
three-way status sync with Notion as source of truth, the branch-per-task PR workflow, and
the intended toolchain — the conventions that otherwise have to be re-derived by reading
several files. Treating it as living documentation is the single biggest quality lever, as
the course claimed.

> Personal course takeaways still to add here in your own words — this section records the
> execution, not what you learned watching the material.
