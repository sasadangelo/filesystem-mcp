"""
Unit tests for filesystem MCP server operations.
Tests follow the AAA (Arrange-Act-Assert) pattern.
"""

import tempfile
from pathlib import Path

import pytest

from filesystem_mcp.server import list_directory, read_file, write_file


@pytest.mark.asyncio
async def test_write_file_creates_new_file():
    """Test writing content to a new file."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        expected_content = "Hello, MCP Server!"

        # Act
        result = await write_file(path=str(test_file), content=expected_content)

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Successfully wrote to" in result[0].text
        assert test_file.exists()
        assert test_file.read_text() == expected_content


@pytest.mark.asyncio
async def test_read_file_returns_content():
    """Test reading content from an existing file."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        expected_content = "Hello, MCP Server!"
        test_file.write_text(expected_content)

        # Act
        result = await read_file(path=str(test_file))

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert result[0].text == expected_content


@pytest.mark.asyncio
async def test_read_file_nonexistent_returns_error():
    """Test reading a non-existent file returns an error."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        nonexistent_file = Path(tmpdir) / "nonexistent.txt"

        # Act
        result = await read_file(path=str(nonexistent_file))

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: File does not exist" in result[0].text


@pytest.mark.asyncio
async def test_read_file_directory_returns_error():
    """Test reading a directory instead of a file returns an error."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)

        # Act
        result = await read_file(path=str(test_dir))

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: Path is not a file" in result[0].text


@pytest.mark.asyncio
async def test_list_directory_shows_files():
    """Test listing directory contents."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        test_file = test_dir / "test.txt"
        test_file.write_text("content")

        # Act
        result = await list_directory(path=str(test_dir))

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
        test_dir = Path(tmpdir)
        subdir = test_dir / "subdir"
        subdir.mkdir()

        # Act
        result = await list_directory(path=str(test_dir))

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
        nonexistent_dir = Path(tmpdir) / "nonexistent"

        # Act
        result = await list_directory(path=str(nonexistent_dir))

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: Path does not exist" in result[0].text


@pytest.mark.asyncio
async def test_list_directory_file_returns_error():
    """Test listing a file instead of a directory returns an error."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("content")

        # Act
        result = await list_directory(path=str(test_file))

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error: Path is not a directory" in result[0].text


@pytest.mark.asyncio
async def test_write_file_creates_parent_directories():
    """Test writing to a file creates parent directories if they don't exist."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        nested_file = Path(tmpdir) / "subdir" / "nested.txt"
        expected_content = "Nested content"

        # Act
        result = await write_file(path=str(nested_file), content=expected_content)

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Successfully wrote to" in result[0].text
        assert nested_file.exists()
        assert nested_file.read_text() == expected_content
        assert nested_file.parent.exists()


@pytest.mark.asyncio
async def test_write_file_overwrites_existing_file():
    """Test writing to an existing file overwrites its content."""
    # Arrange
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("Old content")
        new_content = "New content"

        # Act
        result = await write_file(path=str(test_file), content=new_content)

        # Assert
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Successfully wrote to" in result[0].text
        assert test_file.read_text() == new_content
        assert test_file.read_text() != "Old content"


# Made with Bob
