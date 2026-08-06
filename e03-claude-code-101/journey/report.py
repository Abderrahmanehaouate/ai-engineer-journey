"""Render parsed tasks as a plain-text report.

Output stays ASCII: this runs in a Windows console whose codepage is not always
UTF-8, and a status tool that crashes on its own status glyphs is not useful.
"""

from __future__ import annotations

from dataclasses import dataclass

from .parse import DONE, Task

LABELS = {"todo": "TODO", "doing": "DOING", "done": "DONE", "unknown": "?"}

NAME_WIDTH = 44


@dataclass(frozen=True)
class Summary:
    """Program totals derived from observed status, not the mirrored glyphs."""

    tasks_total: int
    tasks_done: int
    hours_total: float
    hours_done: float
    drifted: list[Task]

    @property
    def percent(self) -> float:
        if not self.hours_total:
            return 0.0
        return self.hours_done / self.hours_total * 100


def summarize(tasks: list[Task]) -> Summary:
    return Summary(
        tasks_total=len(tasks),
        tasks_done=sum(1 for task in tasks if task.observed == DONE),
        hours_total=sum(task.est_hours for task in tasks),
        hours_done=sum(task.est_hours for task in tasks if task.observed == DONE),
        drifted=[task for task in tasks if task.drifted],
    )


def _truncate(text: str, width: int) -> str:
    if len(text) <= width:
        return text
    return text[: width - 3] + "..."


def _dod_cell(task: Task) -> str:
    if not task.dod:
        return "-"
    return f"{task.dod_done}/{task.dod_total}"


def render(tasks: list[Task]) -> str:
    """Build the full report: one row per task, then totals and any drift."""
    summary = summarize(tasks)
    header = f"  {'ID':<4} {'Task':<{NAME_WIDTH}} {'Est':>6}  {'DoD':>5}  Status"
    lines = ["AI Engineer Journey - program status", "", header, "  " + "-" * (len(header) - 2)]

    for task in tasks:
        lines.append(
            f"  {task.id:<4} {_truncate(task.name, NAME_WIDTH):<{NAME_WIDTH}} "
            f"{task.est_hours:>5.1f}h  {_dod_cell(task):>5}  {LABELS[task.observed]}"
        )

    lines += [
        "",
        f"  {summary.hours_done:.1f}h of {summary.hours_total:.1f}h complete "
        f"({summary.percent:.1f}%) - {summary.tasks_done} of {summary.tasks_total} tasks",
    ]

    if summary.drifted:
        lines += ["", f"  DRIFT ({len(summary.drifted)}) - root README disagrees with checkboxes:"]
        for task in summary.drifted:
            lines.append(
                f"    {task.id:<4} root README says {LABELS[task.mirrored]}, "
                f"checkboxes say {LABELS[task.observed]}"
            )
    else:
        lines += ["", "  No drift: root README matches every task's checkboxes."]

    return "\n".join(lines)
