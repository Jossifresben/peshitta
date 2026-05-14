"""Shared pytest fixtures for the Peshitta Constellations test suite.

The Flask app is instantiated once per session (init_index is expensive — it
loads the corpus and builds the in-memory root index). All tests share that
single app via Flask's test_client.
"""
import os
import sys
import pytest

# Make the repo root importable so `from peshitta_roots.app import app` works
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture(scope="session")
def flask_app():
    """The Flask app, initialised once for the whole test session."""
    from peshitta_roots.app import app
    app.config["TESTING"] = True
    return app


@pytest.fixture()
def client(flask_app):
    """A fresh test client per test."""
    return flask_app.test_client()
