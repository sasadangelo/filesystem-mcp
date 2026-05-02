"""
Filesystem MCP Server
A simple MCP server that provides basic filesystem operations.
"""

import os
import sys
from pathlib import Path
from typing import Any, Literal
import asyncio

from mcp.server import Server
from mcp.types import TextContent, Tool
from mcp.server.stdio import stdio_server


# Global variable for sandbox root directory (initialized in main)
SANDBOX_ROOT = ""


# Initialize the MCP server
app = Server(name="filesystem-mcp")


def validate_path(requested_path: str) -> Path:
    """
    Validate that the requested path is within the sandbox directory.

    This function:
    1. Combines the sandbox root with the requested path
    2. Resolves the absolute path (handling .. and symlinks)
    3. Verifies the resolved path is still within the sandbox

    Args:
        requested_path: The path requested by the user (relative to sandbox)

    Returns:
        Path: The validated absolute path

    Raises:
        ValueError: If the path attempts to escape the sandbox
    """
    # Get absolute sandbox path
    abs_sandbox: str = os.path.abspath(SANDBOX_ROOT)

    # Combine sandbox root with requested path
    full_path: str = os.path.join(abs_sandbox, requested_path)

    # Resolve to absolute path (handles .. and symlinks)
    abs_requested: str = os.path.abspath(full_path)

    # Verify the resolved path is still within sandbox
    if not abs_requested.startswith(abs_sandbox + os.sep) and abs_requested != abs_sandbox:
        raise ValueError(f"Access denied: path outside sandbox (requested: {requested_path})")

    return Path(abs_requested)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available filesystem tools."""
    return [
        Tool(
            name="list_directory",
            description="List files and directories in a given path",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The directory path to list (relative or absolute)",
                    }
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="read_file",
            description="Read the contents of a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The file path to read (relative or absolute)",
                    }
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="write_file",
            description="Write content to a file (creates or overwrites)",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The file path to write to (relative or absolute)",
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file",
                    },
                },
                "required": ["path", "content"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls for filesystem operations."""

    if name == "list_directory":
        return await list_directory(path=arguments["path"])
    elif name == "read_file":
        return await read_file(path=arguments["path"])
    elif name == "write_file":
        return await write_file(path=arguments["path"], content=arguments["content"])
    else:
        raise ValueError(f"Unknown tool: {name}")


async def list_directory(path: str) -> list[TextContent]:
    """List contents of a directory."""
    try:
        target_path = validate_path(path)

        if not target_path.exists():
            return [TextContent(type="text", text=f"Error: Path does not exist: {path}")]

        if not target_path.is_dir():
            return [TextContent(type="text", text=f"Error: Path is not a directory: {path}")]

        items: list[Any] = []
        for item in sorted(target_path.iterdir()):
            item_type: Literal["📁", "📄"] = "📁" if item.is_dir() else "📄"
            items.append(f"{item_type} {item.name}")

        result = f"Contents of {path}:\n" + "\n".join(items)
        return [TextContent(type="text", text=result)]

    except ValueError as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    except PermissionError:
        return [TextContent(type="text", text=f"Error: Permission denied: {path}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error listing directory: {str(e)}")]


async def read_file(path: str) -> list[TextContent]:
    """Read contents of a file."""
    try:
        target_path: Path = validate_path(requested_path=path)

        if not target_path.exists():
            return [TextContent(type="text", text=f"Error: File does not exist: {path}")]

        if not target_path.is_file():
            return [TextContent(type="text", text=f"Error: Path is not a file: {path}")]

        content = target_path.read_text(encoding="utf-8")
        return [TextContent(type="text", text=content)]

    except UnicodeDecodeError:
        return [TextContent(type="text", text=f"Error: File is not a text file: {path}")]
    except ValueError as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    except PermissionError:
        return [TextContent(type="text", text=f"Error: Permission denied: {path}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error reading file: {str(e)}")]


async def write_file(path: str, content: str) -> list[TextContent]:
    """Write content to a file."""
    try:
        target_path: Path = validate_path(requested_path=path)

        # Create parent directories if they don't exist
        target_path.parent.mkdir(parents=True, exist_ok=True)

        target_path.write_text(data=content, encoding="utf-8")
        return [TextContent(type="text", text=f"Successfully wrote to {path}")]

    except ValueError as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    except PermissionError:
        return [TextContent(type="text", text=f"Error: Permission denied: {path}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error writing file: {str(e)}")]


async def main() -> None:
    """Run the MCP server."""

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream=read_stream,
            write_stream=write_stream,
            initialization_options=app.create_initialization_options(),
        )


if __name__ == "__main__":
    # Parse command line arguments for sandbox directory
    if len(sys.argv) > 1:
        sandbox_path = sys.argv[1]
    else:
        # Default to ./sandbox directory
        sandbox_path = os.path.join(os.getcwd(), "sandbox")

    # Set global SANDBOX_ROOT
    globals()["SANDBOX_ROOT"] = sandbox_path

    # Verify sandbox directory exists
    if not os.path.isdir(sandbox_path):
        print(f"Error: Sandbox directory does not exist: {sandbox_path}", file=sys.stderr)
        print(f"Usage: {sys.argv[0]} [sandbox_directory]", file=sys.stderr)
        sys.exit(1)

    # Log sandbox configuration to stderr (won't interfere with MCP protocol on stdout)
    print(f"Filesystem MCP Server starting with sandbox: {os.path.abspath(sandbox_path)}", file=sys.stderr)

    asyncio.run(main=main())
