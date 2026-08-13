# AI Engineer Journey

My learning log for the **AI Engineers Track** — July 2026 → October 2026.

The goal: earn AI-900 and AB-620, ship a real internal agent to production (capstone),
and prep for AI-103. This repo is the portfolio artifact for that program.

---

## Accounts

No secrets live in this repo. Credentials go in a password manager; API keys go in
a local `.env` (see [`.env.example`](.env.example)), which is git-ignored.

| Service | Purpose | Status |
|---|---|---|
| Anthropic (Claude Code) | Primary coding agent | ✅ Active |
| GitHub | Source control, portfolio | ✅ Active — [@Abderrahmanehaouate](https://github.com/Abderrahmanehaouate) |
| Hugging Face | Agents course + certification (E8) | ✅ Active |
| Microsoft Learn | AI-900 / AB-620 / AI-103 paths | ✅ Active |

> Smoke-test rule: after creating each account, log in and create one dummy resource
> before moving on. An account that has never been used is not a verified account.

---

## Weekly schedule

Protected study blocks — ~7h/week, on the calendar as recurring events.

| Day | Time | Hours |
|---|---|---|
| Tuesday | 19:00 – 21:00 | 2h |
| Thursday | 19:00 – 21:00 | 2h |
| Saturday | 10:00 – 13:00 | 3h |
| **Total** | | **7h** |

---

## Program tasks

14 tasks across two phases. Source of truth is the Notion tracker; this table is the
public mirror. Status: ⬜ not started · 🔄 in progress · ✅ done.

### Phase 1 — Jul–Aug (foundations)

| ID | Task | Est. | Done |
|---|---|---|---|
| E1 | Kickoff + full environment setup | 3.5h | ✅ |
| E3 | Claude Code 101 | 3.5h | ✅ |
| E4 | Agentic fundamentals: LLM, RAG, tool use, MCP | 7h | 🔄 |
| E5 | Introduction to Model Context Protocol (MCP) | 7h | ⬜ |
| E6 | GitHub Copilot & GitHub at the state of the art | 3.5h | ⬜ |
| E7 | Claude Code in Action | 7h | ⬜ |
| E8 | Hugging Face AI Agents Course (+ certification) | 21h | ⬜ |
| E9 | Create agents in Microsoft Copilot Studio | 14h | ⬜ |
| E10 | Introduction to LangGraph | 10.5h | ⬜ |
| E11 | Evals & agent quality (promptfoo) | 7h | ⬜ |

### Phase 2 — Sep–Oct (certification + ship)

| ID | Task | Est. | Done |
|---|---|---|---|
| E12 | Certification AI-900 (Azure AI Fundamentals) | 7h | ⬜ |
| E13 | Certification AB-620 (AI Agent Builder Associate) | 7h | ⬜ |
| E14 | Ship an internal agent to production (capstone) | 35h | ⬜ |
| E15 | Azure AI Apps & Agents Developer Associate (AI-103) prep | 14h | ⬜ |

**Total estimated effort: 147h** — roughly 21 weeks at 7h/week.

---

## Known risks

**The end date and the effort estimate do not agree.** 147h at 7h/week is 21 weeks. E1
started 2026-07-27, so 21 weeks lands around **2026-12-20**, against a stated target of
end of October — a gap of roughly 50h. Measured generously from 2026-07-01, capacity to
2026-10-31 is ~122h against 147h needed, so the gap does not close on any reading.

Three ways out: extend the end date, raise the weekly hours, or cut scope. **The decision is
deliberately deferred to the Phase 1 → Phase 2 boundary (after E11)**, when the real per-task
velocity from Phase 1 is known and the estimates can be re-based on evidence rather than
guesswork.

Do not let it slip past that point. E14 (capstone, 35h) plus the three certifications
(E12, E13, E15 — 28h) are 63h of the total and all sit in Phase 2, so Phase 2 is where the
gap becomes unavoidable rather than theoretical.

---

## Repo conventions

- One directory per task, named by task ID: `e03-claude-code-101/`, `e08-hf-agents/`, …
- Each task directory gets its own `README.md` with what was built and what was learned.
- Secrets never leave `.env`. If a key is ever committed, rotate it — don't just delete the commit.
- Notes and course bookmarks live in Notion; code and artifacts live here.

## Layout

```
ai-engineer-journey/
├── README.md                   # this file
├── CLAUDE.md                   # working agreement for Claude Code in this repo
├── .env.example                # template for local secrets — copy to .env
├── .gitignore
├── .github/workflows/ci.yml    # ruff + mypy + pytest + journey status --strict
├── e01-kickoff/                # per-task directories, added as the program progresses
├── e03-claude-code-101/        # the `journey` status CLI lives here
└── e04-agentic-fundamentals/
```
