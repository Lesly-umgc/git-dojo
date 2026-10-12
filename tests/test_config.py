"""Smoke tests: the delivery contract CI enforces on every push and PR.

If any of these fail, the delivery is not shippable — no matter what
the commit messages claim.
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent


def test_threshold_in_valid_range():
    """The model threshold must be a real probability."""
    text = (ROOT / "config.yaml").read_text(encoding="utf-8")
    line = next(l for l in text.splitlines() if "threshold" in l)
    value = float(line.split(":")[1])
    assert 0.0 < value < 1.0, f"threshold out of range: {value}"


def test_no_merge_conflict_markers_shipped():
    """A pushed conflict marker in client config is a career-limiting move."""
    for name in ("config.yaml", "train.py"):
        content = (ROOT / name).read_text(encoding="utf-8")
        assert "<<<<<<" not in content, f"conflict marker left in {name}"
        assert ">>>>>>" not in content, f"conflict marker left in {name}"


def test_train_module_compiles():
    """train.py must at least parse — CI catches syntax breaks in seconds."""
    import py_compile

    py_compile.compile(str(ROOT / "train.py"), doraise=True)
