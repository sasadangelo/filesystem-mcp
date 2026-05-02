"""Tests for write_file tool."""

import tempfile
from pathlib import Path

import pytest

from filesystem_mcp.server import write_file
import filesystem_mcp.server as server_module


@pytest.mark.asyncio
async def test_write_file_creates_new_file():
    """Test writing content to a new file."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir
        expected_content = "Hello, MCP Server!"

        # Act
        result = await write_file(path="test.txt", content=expected_content)

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Successfully wrote to" in result[0].text
        test_file = Path(tmpdir) / "test.txt"
        assert test_file.exists()
        assert test_file.read_text() == expected_content


@pytest.mark.asyncio
async def test_write_file_creates_parent_directories():
    """Test writing to a file creates parent directories if they don't exist."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir
        expected_content = "Nested content"

        # Act
        result = await write_file(path="subdir/nested.txt", content=expected_content)

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Successfully wrote to" in result[0].text
        nested_file = Path(tmpdir) / "subdir" / "nested.txt"
        assert nested_file.exists()
        assert nested_file.read_text() == expected_content
        assert nested_file.parent.exists()


@pytest.mark.asyncio
async def test_write_file_overwrites_existing_file():
    """Test writing to an existing file overwrites its content."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("Old content")
        new_content = "New content"

        # Act
        result = await write_file(path="test.txt", content=new_content)

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Successfully wrote to" in result[0].text
        assert test_file.read_text() == new_content
        assert test_file.read_text() != "Old content"


@pytest.mark.asyncio
async def test_write_file_with_empty_content():
    """Test writing empty content to a file."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir

        # Act
        result = await write_file(path="empty.txt", content="")

        # Assert
        assert len(result) == 1
        assert "Successfully wrote to" in result[0].text
        test_file = Path(tmpdir) / "empty.txt"
        assert test_file.exists()
        assert test_file.read_text() == ""


# Made with Bob
