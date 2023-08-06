import pytest
import flyinthejungle


def test_project_defines_author_and_version():
    assert hasattr(flyinthejungle, '__author__')
    assert hasattr(flyinthejungle, '__version__')
