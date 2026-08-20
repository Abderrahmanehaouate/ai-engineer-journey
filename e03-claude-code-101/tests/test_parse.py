from __future__ import annotations

from pathlib import Path

from journey.parse import (
    DoDItem,
    Task,
    find_repo_root,
    is_repo_root,
    load_program,
    parse_dod,
    parse_program_table,
    task_directories,
)

from .conftest import ROOT_README


def test_program_table_reads_every_task_across_both_phases() -> None:
    tasks = parse_program_table(ROOT_README)
    assert [task.id for task in tasks] == ["E1", "E3", "E4", "E12"]


def test_program_table_sorts_numerically_not_lexically() -> None:
    tasks = parse_program_table(ROOT_README)
    assert tasks[-1].id == "E12", "E12 must sort after E4, not between E1 and E3"


def test_program_table_ignores_the_accounts_and_schedule_tables() -> None:
    names = {task.name for task in parse_program_table(ROOT_README)}
    assert "Source control, portfolio" not in names
    assert not any(name.startswith("19:00") for name in names)


def test_program_table_reads_hours_and_status_glyphs() -> None:
    by_id = {task.id: task for task in parse_program_table(ROOT_README)}
    assert by_id["E1"].est_hours == 3.5
    assert by_id["E12"].est_hours == 7.0
    assert by_id["E1"].mirrored == "done"
    assert by_id["E3"].mirrored == "doing"
    assert by_id["E4"].mirrored == "todo"


def test_dod_stops_at_the_next_heading() -> None:
    items = parse_dod(
        "## Definition of done\n\n- [x] counted\n\n## Notes\n\n- [x] not counted\n"
    )
    assert items == [DoDItem(text="counted", checked=True)]


def test_dod_ignores_checkboxes_before_the_section() -> None:
    items = parse_dod("# Title\n\n- [x] stray\n\n## Definition of done\n\n- [ ] real\n")
    assert items == [DoDItem(text="real", checked=False)]


def test_dod_accepts_uppercase_x() -> None:
    assert parse_dod("## Definition of done\n\n- [X] done\n")[0].checked is True


def test_dod_is_empty_when_the_section_is_missing() -> None:
    assert parse_dod("# Title\n\nNo criteria here.\n") == []


def test_observed_status_follows_the_checkboxes() -> None:
    def task(*checked: bool) -> Task:
        dod = [DoDItem(text=str(i), checked=c) for i, c in enumerate(checked)]
        return Task(id="E9", name="x", est_hours=1.0, mirrored="todo", dod=dod)

    assert task(True, True).observed == "done"
    assert task(True, False).observed == "doing"
    assert task(False, False).observed == "doing", (
        "criteria written but unticked means the task is underway, not untouched"
    )
    assert task().observed == "todo", "no directory and no criteria reads as not started"


def test_drift_compares_mirror_against_observation() -> None:
    done = [DoDItem(text="a", checked=True)]
    assert Task(id="E1", name="x", est_hours=1.0, mirrored="done", dod=done).drifted is False
    assert Task(id="E1", name="x", est_hours=1.0, mirrored="todo", dod=done).drifted is True


def test_task_directories_finds_scaffolded_tasks_only(repo: Path) -> None:
    assert sorted(task_directories(repo)) == [1, 3]


def test_load_program_joins_tables_with_task_directories(repo: Path) -> None:
    by_id = {task.id: task for task in load_program(repo)}

    assert by_id["E1"].dod_done == 2
    assert by_id["E1"].observed == "done"

    assert (by_id["E3"].dod_done, by_id["E3"].dod_total) == (1, 3)
    assert by_id["E3"].observed == "doing"

    assert by_id["E4"].directory is None
    assert by_id["E4"].dod == []


def test_load_program_survives_a_directory_with_no_readme(repo: Path) -> None:
    (repo / "e04-agentic-fundamentals").mkdir()
    by_id = {task.id: task for task in load_program(repo)}
    assert by_id["E4"].directory is not None
    assert by_id["E4"].observed == "unknown", "a directory with no criteria cannot be judged"


def test_a_scaffolded_task_with_no_ticks_yet_reads_as_in_progress(repo: Path) -> None:
    """The E4 case: branch checked out, README written, not one box ticked."""
    scaffold = repo / "e04-agentic-fundamentals"
    scaffold.mkdir()
    (scaffold / "README.md").write_text(
        "# E4\n\n## Definition of done\n\n- [ ] one\n- [ ] two\n", encoding="utf-8"
    )

    by_id = {task.id: task for task in load_program(repo)}
    assert by_id["E4"].observed == "doing"
    assert by_id["E4"].drifted is True, "root README still says not-started and must be called out"


def test_not_started_is_distinguishable_from_started_without_criteria(repo: Path) -> None:
    by_id = {task.id: task for task in load_program(repo)}
    assert by_id["E12"].observed == "todo", "E12 has no directory at all"

    (repo / "e12-cert-ai-900").mkdir()
    by_id = {task.id: task for task in load_program(repo)}
    assert by_id["E12"].observed == "unknown", "scaffolded but unreadable is not the same thing"


def test_is_repo_root_needs_both_a_readme_and_a_task_directory(tmp_path: Path, repo: Path) -> None:
    assert is_repo_root(repo) is True

    readme_only = tmp_path / "readme-only"
    readme_only.mkdir()
    (readme_only / "README.md").write_text("# Not the journey repo\n", encoding="utf-8")
    assert is_repo_root(readme_only) is False, "a stray README is not the repo root"


def test_find_repo_root_searches_upward_from_a_nested_directory(repo: Path) -> None:
    nested = repo / "e03-claude-code-101" / "journey"
    nested.mkdir(parents=True, exist_ok=True)
    assert find_repo_root(nested) == repo.resolve()


def test_find_repo_root_falls_back_to_the_starting_point(tmp_path: Path) -> None:
    assert find_repo_root(tmp_path) == tmp_path.resolve()


def test_load_program_rejects_a_path_that_is_not_the_repo_root(tmp_path: Path) -> None:
    try:
        load_program(tmp_path)
    except FileNotFoundError as exc:
        assert "repo root" in str(exc)
    else:
        raise AssertionError("expected FileNotFoundError")
