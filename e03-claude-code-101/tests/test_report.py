from __future__ import annotations

from pathlib import Path

from journey.parse import DoDItem, Task, load_program
from journey.report import render, summarize


def test_summary_counts_only_fully_ticked_tasks(repo: Path) -> None:
    summary = summarize(load_program(repo))

    assert summary.tasks_total == 4
    assert summary.tasks_done == 1, "E3 is partly done and must not count"
    assert summary.hours_total == 21.0
    assert summary.hours_done == 3.5


def test_summary_percent_is_hours_not_task_count(repo: Path) -> None:
    assert summarize(load_program(repo)).percent == 3.5 / 21.0 * 100


def test_summary_percent_handles_an_empty_program() -> None:
    assert summarize([]).percent == 0.0


def test_render_lists_every_task_with_its_checkbox_tally(repo: Path) -> None:
    output = render(load_program(repo))

    assert "E1" in output and "2/2" in output
    assert "E3" in output and "1/3" in output
    assert "DOING" in output
    assert "3.5h of 21.0h complete" in output


def test_render_shows_a_dash_when_there_are_no_checkboxes(repo: Path) -> None:
    line = next(row for row in render(load_program(repo)).splitlines() if row.startswith("  E4"))
    assert line.endswith("TODO")
    assert "-" in line


def test_render_reports_no_drift_for_a_consistent_repo(repo: Path) -> None:
    assert "No drift" in render(load_program(repo))


def test_render_names_the_drifted_tasks(repo: Path) -> None:
    tasks = load_program(repo)
    stale = next(task for task in tasks if task.id == "E3")
    stale.mirrored = "todo"

    output = render(tasks)

    assert "DRIFT (1)" in output
    assert "E3   root README says TODO, checkboxes say DOING" in output


def test_render_output_is_ascii_safe() -> None:
    tasks = [Task(id="E1", name="x", est_hours=1.0, mirrored="done", dod=[DoDItem("a", True)])]
    render(tasks).encode("ascii")
