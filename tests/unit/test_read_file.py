"""Tests for read_file tool."""

import tempfile
from pathlib import Path

import pytest

from filesystem_mcp.server import read_file
import filesystem_mcp.server as server_module


@pytest.mark.asyncio
async def test_read_file_returns_content():
    """Test reading content from an existing file."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir
        test_file = Path(tmpdir) / "test.txt"
        expected_content = "Hello, MCP Server!"
        test_file.write_text(expected_content)

        # Act
        result = await read_file(path="test.txt")

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert result[0].text == expected_content


@pytest.mark.asyncio
async def test_read_file_nonexistent_returns_error():
    """Test reading a non-existent file returns an error."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir

        # Act
        result = await read_file(path="nonexistent.txt")

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: File does not exist" in result[0].text


@pytest.mark.asyncio
async def test_read_file_directory_returns_error():
    """Test reading a directory instead of a file returns an error."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir

        # Act
        result = await read_file(path=".")

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: Path is not a file" in result[0].text


@pytest.mark.asyncio
async def test_read_file_handles_unicode_decode_error():
    """Test that reading a binary file returns appropriate error."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        server_module.SANDBOX_ROOT = tmpdir
        binary_file = Path(tmpdir) / "binary.bin"
        # Write binary data that's not valid UTF-8
        binary_file.write_bytes(b"\x80\x81\x82\x83")

        # Act
        result = await read_file(path="binary.bin")

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: File is not a text file" in result[0].text


# Made with Bob
