from __future__ import annotations

from pathlib import Path

import pytest

from journey.cli import main


def test_status_prints_the_report(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["status", "--repo", str(repo)]) == 0
    assert "program status" in capsys.readouterr().out


def test_strict_succeeds_when_nothing_has_drifted(repo: Path) -> None:
    assert main(["status", "--repo", str(repo), "--strict"]) == 0


def test_strict_fails_when_the_root_readme_is_stale(repo: Path) -> None:
    readme = repo / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8").replace("| 3.5h | ✅ |", "| 3.5h | ⬜ |"),
                      encoding="utf-8")

    assert main(["status", "--repo", str(repo), "--strict"]) == 1


def test_drift_alone_does_not_fail_without_strict(repo: Path) -> None:
    readme = repo / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8").replace("| 3.5h | ✅ |", "| 3.5h | ⬜ |"),
                      encoding="utf-8")

    assert main(["status", "--repo", str(repo)]) == 0


def test_default_repo_is_found_from_the_working_directory(
    repo: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Without --repo the tool reads the repo enclosing the cwd, not its own source tree."""
    nested = repo / "e03-claude-code-101"
    monkeypatch.chdir(nested)

    assert main(["status"]) == 0
    assert "Kickoff + full environment setup" in capsys.readouterr().out


def test_default_repo_errors_outside_any_repo(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["status"]) == 2
    assert "repo root" in capsys.readouterr().err


def test_missing_repo_reports_an_error(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["status", "--repo", str(tmp_path)]) == 2
    assert "repo root" in capsys.readouterr().err


def test_bare_invocation_prints_help(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert "usage:" in capsys.readouterr().out
