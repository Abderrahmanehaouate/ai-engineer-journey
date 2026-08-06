"""A miniature journey repo, shaped like the real one but small enough to assert on."""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT_README = """\
# AI Engineer Journey

| Service | Purpose | Status |
|---|---|---|
| GitHub | Source control, portfolio | Active |

| Day | Time | Hours |
|---|---|---|
| Tuesday | 19:00 - 21:00 | 2h |
| **Total** | | **7h** |

### Phase 1

| ID | Task | Est. | Done |
|---|---|---|---|
| E1 | Kickoff + full environment setup | 3.5h | ✅ |
| E3 | Claude Code 101 | 3.5h | \U0001f504 |
| E4 | Agentic fundamentals | 7h | ⬜ |

### Phase 2

| ID | Task | Est. | Done |
|---|---|---|---|
| E12 | Certification AI-900 | 7h | ⬜ |
"""

E01_README = """\
# E1 - Kickoff

## Definition of done

- [x] Accounts created
- [x] Claude Code installed

## Notes

Everything shipped.
"""

E03_README = """\
# E3 - Claude Code 101

## Definition of done

- [x] Claude Code configured on a real repo
- [ ] One real task done end-to-end
- [ ] CLAUDE.md written and committed

## What was actually built

_To fill in._
"""


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """E1 fully ticked, E3 partly ticked, E4 and E12 not yet scaffolded."""
    (tmp_path / "README.md").write_text(ROOT_README, encoding="utf-8")

    kickoff = tmp_path / "e01-kickoff"
    kickoff.mkdir()
    (kickoff / "README.md").write_text(E01_README, encoding="utf-8")

    claude_code = tmp_path / "e03-claude-code-101"
    claude_code.mkdir()
    (claude_code / "README.md").write_text(E03_README, encoding="utf-8")

    return tmp_path
