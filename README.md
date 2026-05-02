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
tests/unit/test_list_directory.py::test_list_directory_shows_files PASSED
tests/unit/test_list_directory.py::test_list_directory_shows_subdirectories PASSED
tests/unit/test_list_directory.py::test_list_directory_nonexistent_returns_error PASSED
tests/unit/test_list_directory.py::test_list_directory_nonexistent PASSED
tests/unit/test_list_directory.py::test_list_directory_file_returns_error PASSED
...
```

### Method 2: MCP Inspector (Recommended for Integration Testing)

MCP Inspector is a visual tool for testing MCP servers. It provides an interactive web interface to test your server's tools.

#### Starting the Inspector

Run the inspector with the provided shell script:

```bash
npx @modelcontextprotocol/inspector ./run_server.sh
```

This will:
1. Start MCP Inspector on `http://localhost:6274`
2. Automatically open your browser
3. Connect the server to the inspector with the correct environment variables

#### Using the Inspector

In the web interface you can:
- 📋 View all available tools
- 🧪 Test each tool interactively
- 📊 See requests and responses in real-time
- 🐛 Debug the MCP protocol

**Example tests in the Inspector:**

1. **List the sandbox directory:**
   - Select the `list_directory` tool
   - Enter `{"path": "sandbox"}` as arguments
   - Click "Run" to see the sample files

2. **Read a sample file:**
   - Select the `read_file` tool
   - Enter `{"path": "sandbox/test.txt"}` as arguments
   - Click "Run" to see the content

3. **Write a new file:**
   - Select the `write_file` tool
   - Enter `{"path": "sandbox/myfile.txt", "content": "Hello from MCP!"}` as arguments
   - Click "Run" to create the file

## 🔧 Configuration with Claude Desktop

To use this server with Claude Desktop, you need to configure it in Claude's configuration file.

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Quick Setup

1. Copy the example configuration:
   ```bash
   cp mcp-config.json.example mcp-config.json
   ```

2. The default configuration uses relative paths and should work out of the box:
   ```json
   {
     "mcpServers": {
       "filesystem": {
         "command": "uv",
         "args": [
           "run",
           "python",
           "-m",
           "filesystem_mcp.server",
           "sandbox"
         ]
       }
     }
   }
   ```

3. Add this configuration to Claude Desktop's config file

### Custom Configuration

If you need to customize paths, edit `mcp-config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "-m",
        "filesystem_mcp.server",
        "/absolute/path/to/your/sandbox"
      ],
      "cwd": "/absolute/path/to/filesystem-mcp"
    }
  }
}
```

**Important Configuration Notes:**
- The `sandbox` argument specifies which directory the server can access
- Use relative paths (like `sandbox`) for portability
- Use absolute paths if you need to access specific directories
- The server will **only** access files within the specified sandbox directory
- `mcp-config.json` is gitignored to avoid committing user-specific paths

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
│       └── server.py                    # Main MCP server with sandbox protection
├── tests/
│   └── unit/
│       ├── __init__.py
│       ├── test_read_file.py            # Tests for read_file tool
│       ├── test_write_file.py           # Tests for write_file tool
│       ├── test_list_directory.py       # Tests for list_directory tool
│       ├── test_validate_path.py        # Tests for path validation
│       └── test_sandbox_security.py     # Security tests
├── sandbox/                             # Default sandbox directory for testing
│   ├── test.txt                         # Sample text file
│   ├── notes.md                         # Sample markdown file
│   └── config.json                      # Sample JSON file
├── .vscode/
│   └── launch.json                      # VS Code debug configuration
├── run_server.sh                        # Shell script to run server with correct env
├── pyproject.toml                       # Project configuration
├── uv.lock                              # Dependencies lockfile
├── .gitignore                           # Git ignore rules
├── .flake8                              # Flake8 configuration
├── LICENSE                              # MIT License
└── README.md                            # This file
```

### Sandbox Directory

The `sandbox/` directory is provided as a **secure testing area** with sample files:
- `test.txt` - A simple text file
- `notes.md` - A markdown file with a list
- `config.json` - A JSON configuration file

**Important:** The server enforces that all operations stay within the configured sandbox directory. This prevents accidental or malicious access to files outside the sandbox.

## 🔒 Security

### ✅ Sandbox Protection (Implemented)

The server now includes **mandatory sandbox protection** that restricts all filesystem operations to a specified directory.

**How it works:**
- All file paths are validated before any operation
- Paths are resolved to absolute paths (handling `..` and symlinks)
- The server verifies that resolved paths remain within the sandbox
- Path traversal attacks (e.g., `../../../etc/passwd`) are automatically blocked

**Security Status:**
- ✅ **Path restrictions implemented** - All operations confined to sandbox directory
- ✅ **Path traversal protection** - Attempts to escape sandbox are blocked
- ✅ **Mandatory sandbox** - Server requires sandbox directory argument
- ❌ No operation logging (planned)
- ❌ No additional permission controls (planned)

**Usage:**
```bash
# Specify sandbox directory when starting server
uv run python -m filesystem_mcp.server /path/to/sandbox

# Or use default ./sandbox directory
uv run python -m filesystem_mcp.server sandbox
```

**Example - What's Protected:**
- ✅ `read_file("test.txt")` → Reads `sandbox/test.txt`
- ✅ `list_directory(".")` → Lists `sandbox/`
- ❌ `read_file("../../../etc/passwd")` → **BLOCKED** (outside sandbox)
- ❌ `read_file("/etc/passwd")` → **BLOCKED** (outside sandbox)

**Recommendations:**
- ✅ Always specify a dedicated sandbox directory
- ✅ Use a directory with only test/safe files
- ✅ Run with limited user permissions
- ✅ Never expose to untrusted users or networks
- ✅ Review operations in production environments

**The `sandbox/` directory in this repository contains sample files for safe testing.**

## 🛠️ Development

### Running the Server Manually

With default sandbox directory:
```bash
PYTHONPATH=src uv run python -m filesystem_mcp.server sandbox
```

With custom sandbox directory:
```bash
PYTHONPATH=src uv run python -m filesystem_mcp.server /path/to/your/sandbox
```

### Testing Sandbox Security

Run the sandbox validation test:
```bash
python test_sandbox.py
```

This test verifies that:
- Valid paths within sandbox are allowed
- Path traversal attempts are blocked
- The sandbox protection works correctly

### Running with the Shell Script

```bash
./run_server.sh
```

## 🚀 Next Steps

Ideas to evolve the server:

- [x] **Implement path restrictions (sandbox)** - ✅ Completed!
- [ ] Add operation logging and audit trails
- [ ] Add `delete_file` operation
- [ ] Add `create_directory` operation
- [ ] Implement file search with patterns
- [ ] Add support for binary files
- [ ] Support for recursive operations
- [ ] File metadata (size, modification date, permissions)
- [ ] Add HTTP transport support
- [ ] Add configurable file size limits
- [ ] Add rate limiting for operations

## 📝 License

MIT License © 2025 Salvatore D'Angelo

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

**Note**: This is an educational project to learn MCP. For production use, consider adding additional security controls and error handling.
