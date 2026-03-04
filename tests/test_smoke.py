from pathlib import Path


def test_project_core_paths_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (root / "chapters").exists()
    assert (root / "final").exists()
    assert (root / "docs").exists()
    assert (root / "README.md").exists()
