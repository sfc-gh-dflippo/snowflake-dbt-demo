# Testing the Skills MCP Server

## Quick Start

```bash
npm test  # Runs all 34 tests (~3 seconds)
```

## Test Structure

Three test suites cover different aspects:

### 1. TypeScript Server Tests (`tests/test-server.ts`)

Tests the MCP server implementation - 16 tests covering:
- Resource listing (3 resources)
- Resource metadata and content
- Prompts (2 prompts)
- Tools (1 tool)
- Server capabilities

```bash
npm run test:server
```

### 2. TypeScript Script Tests (`tests/test-sync-script.ts`)

Tests the TypeScript sync script - 11 tests covering:
- Script syntax and compilation
- Required functions and imports
- Configuration constants
- Error handling
- JavaScript output validation

```bash
npm run test:ts-script
```

### 3. Python Script Tests (`tests/test_sync_script.py`)

Tests the Python sync script - 7 tests covering:
- Script syntax validation
- Required functions and imports
- Shebang and structure
- Script compilation

```bash
npm run test:py-script
```

## Development Testing

### FastMCP Dev Mode (Recommended)

Interactive CLI for quick testing:

```bash
npm run dev
```

Features:
- List resources interactively
- Read resource content
- Test prompts and tools
- See immediate feedback

### MCP Inspector

Visual web UI for testing:

```bash
npm run inspect
```

Opens `http://localhost:6274` with:
- Server info and capabilities
- Resource browser
- Interactive resource reading
- Prompt and tool testing

## Expected Server State

### Resources (3)

- `script://sync-skills.py` - Python sync script (~10KB)
- `script://sync-skills.ts` - TypeScript sync script (~11KB)
- `doc://manage-repositories` - Repository management docs

### Prompts (2)

- `sync-skills` - Step-by-step sync instructions
- `manage-repositories` - How to add/remove repositories

### Tools (1)

- `get_sync_instructions` - Returns sync instructions

## Python Test Setup

First-time setup for Python tests:

```bash
python3 -m venv .venv-test
source .venv-test/bin/activate
pip install -r tests/requirements.txt
```

The `npm run test:py-script` command handles activation automatically.

## Test Principles

All tests follow these principles:

1. **Fast** - Complete in < 1 second per test
2. **Deterministic** - Same result every time
3. **Self-Contained** - No shared state between tests
4. **Clear** - Name and assertions explain what's tested
5. **Current** - Tests match actual implementation

## Continuous Integration

All tests run on every build:

```bash
npm run build && npm test
```

Exit code 0 = all tests pass
Exit code 1 = at least one test failed

## Adding New Tests

### For Server Changes

Add tests to `tests/test-server.ts`:
- New resources → Add to resource listing tests
- New prompts → Add to prompts tests
- New tools → Add to tools tests

### For Script Changes

- TypeScript changes → Update `tests/test-sync-script.ts`
- Python changes → Update `tests/test_sync_script.py`

## Troubleshooting

### "Module not found" errors

```bash
npm run build  # Rebuild the dist/ directory
```

### Python tests fail

```bash
# Recreate Python virtual environment
rm -rf .venv-test
python3 -m venv .venv-test
source .venv-test/bin/activate
pip install -r tests/requirements.txt
```

### MCP Inspector won't start

```bash
# Ensure server is built
npm run build

# Try with npx to ensure latest inspector
npx @modelcontextprotocol/inspector node dist/index.js
```

## Test Coverage

Current test coverage:

- **Server Resources** - ✅ 100%
- **Server Prompts** - ✅ 100%
- **Server Tools** - ✅ 100%
- **Script Structure** - ✅ 100%
- **Script Syntax** - ✅ 100%
- **Script Compilation** - ✅ 100%

Total: **34 tests, all passing**
