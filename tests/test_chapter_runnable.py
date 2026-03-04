from pathlib import Path
import runpy


def test_all_chapter_versions_can_run() -> None:
    root = Path(__file__).resolve().parents[1]
    version_files = sorted(root.glob("chapters/*/v[123]_*.py"))
    assert len(version_files) == 30

    for file_path in version_files:
        runpy.run_path(str(file_path), run_name="__main__")
