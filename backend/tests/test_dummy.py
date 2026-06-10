"""Trivial backend test to verify pytest environment."""


def test_dummy(dummy_fixture: str) -> None:
    """Verify conftest loading and pytest runner."""
    assert dummy_fixture == "ok"
