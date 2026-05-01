# 🗂️ Filesystem MCP Server

A simple MCP (Model Context Protocol) server for filesystem operations, built with Python and `uv`.

## 🎯 What is MCP?

MCP (Model Context Protocol) is a standard protocol for connecting AI assistants (like Claude) to external tools. This server allows Claude to interact with the filesystem in a safe and controlled manner.

## ✨ Features

The server provides three basic operations:

- **📂 list_directory**: Lists files and directories in a specified path
- **📖 read_file**: Reads the content of a text file
- **📝 write_file**: Writes content to a file (creates or overwrites)

## 🚀 Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-org/filesystem-mcp.git
cd filesystem-mcp
```

### 2️⃣ Install Dependencies

```bash
uv sync
```

This automatically creates a virtual environment and installs all necessary dependencies.

## 🧪 Testing

### Method 1: Unit Tests with pytest

Run the unit tests to verify that the core functions work correctly:

```bash
uv run pytest tests/unit/ -v
```

For more detailed output with coverage:

```bash
uv run pytest tests/unit/ -v --cov=src/filesystem_mcp --cov-report=term-missing
```

Expected output:
```
tests/unit/test_server.py::test_list_directory PASSED
tests/unit/test_server.py::test_read_file PASSED
tests/unit/test_server.py::test_write_file PASSED
tests/unit/test_server.py::test_list_directory_nonexistent PASSED
tests/unit/test_server.py::test_read_file_nonexistent PASSED
```

### Method 2: Manual Function Testing

Run a quick manual test to verify basic functionality:

```bash
PYTHONPATH=src uv run python test_server.py
```

### Method 3: MCP Inspector (Recommended for Integration Testing)

MCP Inspector is a visual tool for testing MCP servers. It provides an interactive web interface to test your server's tools.

#### Using the Configuration File

The easiest way to use MCP Inspector is with the provided configuration file:

```bash
npx @modelcontextprotocol/inspector mcp-inspector-config.json
```

This will:
1. Start MCP Inspector on `http://localhost:5173`
2. Automatically open your browser
3. Connect the server to the inspector

#### Manual Command

Alternatively, you can run it manually:

```bash
npx @modelcontextprotocol/inspector uv run python -m filesystem_mcp.server
```

#### Using the Inspector

In the web interface you can:
- 📋 View all available tools
- 🧪 Test each tool interactively
- 📊 See requests and responses in real-time
- 🐛 Debug the MCP protocol

**Example test in the Inspector:**
1. Select the `list_directory` tool
2. Enter `{"path": "."}` as arguments
3. Click "Run" to see the results

## 🔧 Configuration with Claude Desktop

To use this server with Claude Desktop, add the following configuration to Claude's configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "-m",
        "filesystem_mcp.server"
      ],
      "cwd": "/path/to/filesystem-mcp"
    }
  }
}
```

Replace `/path/to/filesystem-mcp` with the absolute path to the project directory.

## 📖 Usage

Once configured, you can ask Claude to:

- "List the files in the /Users/username/Documents directory"
- "Read the content of the config.json file"
- "Create a file called notes.txt with the content 'Hello World'"

## 🏗️ Project Structure

```
filesystem-mcp/
├── src/
│   └── filesystem_mcp/
│       ├── __init__.py
│       └── server.py              # Main MCP server
├── tests/
│   ├── test_hello.py              # Example test
│   └── unit/
│       ├── __init__.py
│       └── test_server.py         # Unit tests for server functions
├── .vscode/
│   └── launch.json                # VS Code debug configuration
├── test_server.py                 # Manual test script
├── mcp-config.json                # Example MCP configuration
├── mcp-inspector-config.json      # MCP Inspector configuration
├── inspector-config.json          # Alternative inspector config
├── run_server.sh                  # Shell script to run server
├── pyproject.toml                 # Project configuration
├── uv.lock                        # Dependencies lockfile
├── .gitignore                     # Git ignore rules
├── .flake8                        # Flake8 configuration
├── LICENSE                        # MIT License
└── README.md                      # This file
```

## 🔒 Security

⚠️ **Important**: This server has full access to the filesystem. Use it only in trusted environments and consider:

- Limiting access to specific directories
- Implementing permission controls
- Validating file paths
- Adding operation logging

## 🛠️ Development

### Running the Server Manually

```bash
PYTHONPATH=src uv run python -m filesystem_mcp.server
```

### Running with the Shell Script

```bash
./run_server.sh
```

## 🚀 Next Steps

Ideas to evolve the server:

- [ ] Implement path restrictions (sandbox)
- [ ] Add `delete_file` operation
- [ ] Add `create_directory` operation
- [ ] Implement file search with patterns
- [ ] Add support for binary files
- [ ] Add operation logging
- [ ] Support for recursive operations
- [ ] File metadata (size, modification date, permissions)

## 📝 License

MIT License © 2025 Salvatore D'Angelo

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

**Note**: This is an educational project to learn MCP. For production use, consider adding additional security controls and error handling.
