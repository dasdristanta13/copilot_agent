"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def dummy_fixture() -> str:
    """Provide a simple dummy fixture."""
    return "ok"
