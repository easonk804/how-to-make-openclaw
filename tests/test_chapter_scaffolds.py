from pathlib import Path


def test_each_chapter_has_required_files() -> None:
    root = Path(__file__).resolve().parents[1] / "chapters"
    chapter_dirs = sorted([p for p in root.iterdir() if p.is_dir()])
    assert len(chapter_dirs) == 10

    for chapter in chapter_dirs:
        assert (chapter / "README.md").exists(), f"missing README.md in {chapter.name}"
        assert any(chapter.glob("v1_*.py")), f"missing v1_*.py in {chapter.name}"
        assert any(chapter.glob("v2_*.py")), f"missing v2_*.py in {chapter.name}"
        assert any(chapter.glob("v3_*.py")), f"missing v3_*.py in {chapter.name}"
        assert (chapter / "exercises.md").exists(), f"missing exercises.md in {chapter.name}"
        assert any(chapter.glob("test_chapter*.py")), f"missing chapter test in {chapter.name}"
