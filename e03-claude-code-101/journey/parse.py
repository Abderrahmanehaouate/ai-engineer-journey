"""Parse the repo's markdown into structured task records.

Two sources feed a status report, and they disagree often enough that detecting
the disagreement is the point of this tool:

- The root ``README.md`` task tables: every task, its estimate, and a *mirrored*
  status glyph that a human has to remember to update.
- Each ``e*/README.md`` "Definition of done" section: checkboxes that get ticked
  as the work actually happens. This is the observed truth.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

#: A task row in one of the root README program tables:
#: ``| E1 | Kickoff + full environment setup | 3.5h | * |``
TABLE_ROW = re.compile(r"^\|\s*(E\d+)\s*\|\s*(.+?)\s*\|\s*([\d.]+)\s*h\s*\|\s*(\S+)?\s*\|$")

#: A markdown task-list checkbox, ticked or not.
CHECKBOX = re.compile(r"^-\s*\[([ xX])\]\s*(.+?)\s*$")

DOD_HEADING = re.compile(r"^##\s+definition of done\s*$", re.IGNORECASE)
ANY_HEADING = re.compile(r"^#{1,6}\s")
TASK_DIR = re.compile(r"^e(\d+)-")

#: Root README legend: not started / in progress / done.
STATUS_BY_GLYPH = {"⬜": "todo", "\U0001f504": "doing", "✅": "done"}

TODO, DOING, DONE, UNKNOWN = "todo", "doing", "done", "unknown"


@dataclass(frozen=True)
class DoDItem:
    """One acceptance-criteria checkbox from a task README."""

    text: str
    checked: bool


@dataclass
class Task:
    """A program task, joined across the root README and its own directory."""

    id: str
    name: str
    est_hours: float
    mirrored: str
    directory: Path | None = None
    dod: list[DoDItem] = field(default_factory=list)

    @property
    def number(self) -> int:
        return int(self.id[1:])

    @property
    def dod_done(self) -> int:
        return sum(1 for item in self.dod if item.checked)

    @property
    def dod_total(self) -> int:
        return len(self.dod)

    @property
    def observed(self) -> str:
        """Status implied by the checkboxes, regardless of what the mirror claims.

        A task with no directory or no checkboxes has nothing to observe, so it
        reads as not started.
        """
        if not self.dod:
            return TODO
        if all(item.checked for item in self.dod):
            return DONE
        if any(item.checked for item in self.dod):
            return DOING
        return TODO

    @property
    def drifted(self) -> bool:
        return self.mirrored != self.observed


def read_text(path: Path) -> str:
    """Read markdown as UTF-8 regardless of the console's codepage."""
    return path.read_text(encoding="utf-8")


def parse_program_table(text: str) -> list[Task]:
    """Pull task rows out of the root README, ignoring its other tables.

    The accounts and schedule tables have a different column count and no ``E``
    prefixed first cell, so the row pattern skips them. A task listed twice keeps
    its first appearance.
    """
    tasks: list[Task] = []
    seen: set[str] = set()
    for raw in text.splitlines():
        match = TABLE_ROW.match(raw.strip())
        if not match:
            continue
        task_id, name, hours, glyph = match.groups()
        if task_id in seen:
            continue
        seen.add(task_id)
        tasks.append(
            Task(
                id=task_id,
                name=name,
                est_hours=float(hours),
                mirrored=STATUS_BY_GLYPH.get(glyph or "", UNKNOWN),
            )
        )
    return sorted(tasks, key=lambda task: task.number)


def parse_dod(text: str) -> list[DoDItem]:
    """Collect checkboxes from the "Definition of done" section only.

    Task READMEs carry checkboxes elsewhere over time; stopping at the next
    heading keeps those out of the acceptance criteria.
    """
    items: list[DoDItem] = []
    in_section = False
    for raw in text.splitlines():
        line = raw.strip()
        if DOD_HEADING.match(line):
            in_section = True
            continue
        if not in_section:
            continue
        if ANY_HEADING.match(line):
            break
        match = CHECKBOX.match(line)
        if match:
            items.append(DoDItem(text=match.group(2), checked=match.group(1).lower() == "x"))
    return items


def task_directories(repo_root: Path) -> dict[int, Path]:
    """Map task number to its directory, for the ones scaffolded so far."""
    found: dict[int, Path] = {}
    for entry in sorted(repo_root.iterdir()):
        if not entry.is_dir():
            continue
        match = TASK_DIR.match(entry.name)
        if match:
            found[int(match.group(1))] = entry
    return found


def load_program(repo_root: Path) -> list[Task]:
    """Join the root README task list with whatever task directories exist."""
    root_readme = repo_root / "README.md"
    if not root_readme.is_file():
        raise FileNotFoundError(f"no README.md at {repo_root} - is that the repo root?")

    tasks = parse_program_table(read_text(root_readme))
    directories = task_directories(repo_root)
    for task in tasks:
        directory = directories.get(task.number)
        if directory is None:
            continue
        task.directory = directory
        readme = directory / "README.md"
        if readme.is_file():
            task.dod = parse_dod(read_text(readme))
    return tasks
