# THIS CODE HAS BEEN ORGANIZED

"""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║ Documentation for test_importing_this_package.py
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Standard Library Imports
import importlib
from importlib.util import find_spec

# Third-Party Imports
import pytest


# Main Functions
def test_importing_this_package():
    spec = find_spec("dev_pytopia")
    assert spec is not None, "Package 'dev_pytopia' not found!"

    try:
        importlib.import_module("dev_pytopia")
    except ImportError as e:
        pytest.fail(f"Failed to import 'dev_pytopia' package: {e}")
