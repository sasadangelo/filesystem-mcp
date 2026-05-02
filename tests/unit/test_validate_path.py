"""Tests for validate_path security function."""

import tempfile
from pathlib import Path

import pytest

from filesystem_mcp.server import validate_path
import filesystem_mcp.server as server_module


@pytest.mark.asyncio
async def test_validate_path_with_empty_string():
    """Test validate_path with empty string."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir

        # Act
        result = validate_path("")

        # Assert - empty string should resolve to sandbox root
        assert str(result) == tmpdir


@pytest.mark.asyncio
async def test_validate_path_with_dot():
    """Test validate_path with current directory."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir

        # Act
        result = validate_path(".")

        # Assert
        assert str(result) == tmpdir


@pytest.mark.asyncio
async def test_validate_path_with_subdirectory():
    """Test validate_path with subdirectory path."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir
        subdir = Path(tmpdir) / "subdir"
        subdir.mkdir()

        # Act
        result = validate_path("subdir")

        # Assert
        assert result == subdir


# Made with Bob
