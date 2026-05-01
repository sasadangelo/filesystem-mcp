"""
Filesystem MCP Server
A simple MCP server that provides basic filesystem operations.
"""

from pathlib import Path
from typing import Any, Literal

from mcp.server import Server
from mcp.types import TextContent, Tool
from mcp.server.stdio import stdio_server


# Initialize the MCP server
app = Server(name="filesystem-mcp")


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
        target_path = Path(path).expanduser().resolve()

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

    except PermissionError:
        return [TextContent(type="text", text=f"Error: Permission denied: {path}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error listing directory: {str(e)}")]


async def read_file(path: str) -> list[TextContent]:
    """Read contents of a file."""
    try:
        target_path: Path = Path(path).expanduser().resolve()

        if not target_path.exists():
            return [TextContent(type="text", text=f"Error: File does not exist: {path}")]

        if not target_path.is_file():
            return [TextContent(type="text", text=f"Error: Path is not a file: {path}")]

        content = target_path.read_text(encoding="utf-8")
        return [TextContent(type="text", text=content)]

    except PermissionError:
        return [TextContent(type="text", text=f"Error: Permission denied: {path}")]
    except UnicodeDecodeError:
        return [TextContent(type="text", text=f"Error: File is not a text file: {path}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error reading file: {str(e)}")]


async def write_file(path: str, content: str) -> list[TextContent]:
    """Write content to a file."""
    try:
        target_path: Path = Path(path).expanduser().resolve()

        # Create parent directories if they don't exist
        target_path.parent.mkdir(parents=True, exist_ok=True)

        target_path.write_text(data=content, encoding="utf-8")
        return [TextContent(type="text", text=f"Successfully wrote to {path}")]

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
    import asyncio

    asyncio.run(main=main())
