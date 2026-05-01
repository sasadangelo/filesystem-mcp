#!/bin/bash
cd /Users/sasadangelo/github.com/sasadangelo/filesystem-mcp
export PYTHONPATH=src
exec uv run python -m filesystem_mcp.server

# Made with Bob
