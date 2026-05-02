"""Tests for sandbox security."""

import tempfile

import pytest

from filesystem_mcp.server import read_file
import filesystem_mcp.server as server_module


@pytest.mark.asyncio
async def test_sandbox_blocks_path_traversal_attack():
    """Test that path traversal attacks are blocked."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir

        # Act
        result = await read_file(path="../../../etc/passwd")

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: Access denied" in result[0].text or "outside sandbox" in result[0].text


@pytest.mark.asyncio
async def test_sandbox_blocks_absolute_path_outside():
    """Test that absolute paths outside sandbox are blocked."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir

        # Act
        result = await read_file(path="/etc/passwd")

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: Access denied" in result[0].text or "outside sandbox" in result[0].text


# Made with Bob
