"""Tests for list_directory tool."""

import tempfile
from pathlib import Path

import pytest

from filesystem_mcp.server import list_directory
import filesystem_mcp.server as server_module


@pytest.mark.asyncio
async def test_list_directory_shows_files():
    """Test listing directory contents."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("content")

        # Act
        result = await list_directory(path=".")

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Contents of" in result[0].text
        assert "test.txt" in result[0].text
        assert "📄" in result[0].text


@pytest.mark.asyncio
async def test_list_directory_shows_subdirectories():
    """Test listing directory with subdirectories."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir
        subdir = Path(tmpdir) / "subdir"
        subdir.mkdir()

        # Act
        result = await list_directory(path=".")

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "subdir" in result[0].text
        assert "📁" in result[0].text


@pytest.mark.asyncio
async def test_list_directory_nonexistent_returns_error():
    """Test listing a non-existent directory returns an error."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir

        # Act
        result = await list_directory(path="nonexistent")

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: Path does not exist" in result[0].text


@pytest.mark.asyncio
async def test_list_directory_file_returns_error():
    """Test listing a file instead of a directory returns an error."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("content")

        # Act
        result = await list_directory(path="test.txt")

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: Path is not a directory" in result[0].text


@pytest.mark.asyncio
async def test_list_directory_empty_directory():
    """Test listing an empty directory."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir

        # Act
        result = await list_directory(path=".")

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Contents of" in result[0].text


# Made with Bob
