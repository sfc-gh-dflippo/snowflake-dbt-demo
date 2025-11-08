# Contributing to Skills MCP Server

Thank you for your interest in contributing to the Skills MCP Server!

## Development Setup

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager
- Git

### Setup Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/skills-mcp-server.git
   cd skills-mcp-server
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov  # For testing
   ```

4. **Install in development mode:**
   ```bash
   pip install -e .
   ```

## Running Tests

### Basic Functionality Test

```bash
python test_basic.py
```

### Full Test Suite

```bash
pytest tests/ -v
```

### With Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

## Code Style

### Python Code Standards

- Follow PEP 8 style guide
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Docstrings

Use Google-style docstrings:

```python
def function_name(arg1: str, arg2: int) -> bool:
    """
    Short description of function.
    
    Longer description with more details if needed.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: Description of when this is raised
    """
    pass
```

## Project Structure

```
skills-mcp-server/
├── src/                    # Source code
│   ├── __init__.py        # Package initialization
│   ├── __main__.py        # Entry point for module execution
│   ├── server.py          # FastMCP server implementation
│   ├── skill_manager.py   # Skill discovery and management
│   └── git_sync.py        # Repository synchronization
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_git_sync.py
│   ├── test_skill_manager.py
│   └── test_server.py
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
├── README.md              # User documentation
├── CONTRIBUTING.md        # This file
└── LICENSE                # MIT License
```

## Making Changes

### Branching Strategy

- `main` - Stable, production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical production fixes

### Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write code
   - Add/update tests
   - Update documentation

3. **Run tests:**
   ```bash
   python test_basic.py
   pytest tests/
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: Add new feature description"
   ```

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**

### Commit Message Format

Follow Conventional Commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `chore:` - Build/tool changes

Examples:
```
feat: Add support for GitLab repositories
fix: Handle missing skill resources gracefully
docs: Update configuration examples in README
test: Add integration tests for git_sync module
```

## Adding Features

### Adding a New MCP Tool

1. **Update server.py:**
   ```python
   @server.list_tools()
   async def list_tools() -> list[Tool]:
       return [
           # ... existing tools ...
           Tool(
               name="your_tool_name",
               description="Description of your tool",
               inputSchema={
                   "type": "object",
                   "properties": {
                       # Define parameters
                   }
               }
           )
       ]
   
   @server.call_tool()
   async def call_tool(name: str, arguments: dict) -> list[TextContent]:
       if name == "your_tool_name":
           # Implement tool logic
           pass
   ```

2. **Add tests:**
   Create test file in `tests/test_your_feature.py`

3. **Update documentation:**
   Add tool to README.md MCP Interface section

### Adding Support for New Git Providers

1. **Update git_sync.py:**
   - Add URL detection for new provider
   - Implement ZIP download URL construction
   - Handle provider-specific quirks

2. **Add tests:**
   Add test cases for new provider URLs

3. **Update README.md:**
   Document new provider support

## Testing

### Unit Tests

Test individual functions and classes:

```python
def test_function_name():
    """Test description."""
    result = function_to_test(input_value)
    assert result == expected_value
```

### Integration Tests

Test interactions between modules:

```python
def test_skill_discovery_flow():
    """Test complete skill discovery flow."""
    # Setup
    config = create_test_config()
    
    # Execute
    repos = sync_repositories(config)
    skills = discover_skills(repos)
    
    # Verify
    assert len(skills) > 0
```

### Manual Testing

Test the MCP server integration:

1. Update `.cursor/mcp.json` with local development path
2. Restart Cursor
3. Verify skills catalog appears
4. Test loading skills
5. Test MCP tools

## Documentation

### README Updates

Update README.md for:
- New features
- Configuration changes
- API changes
- Usage examples

### PRD Updates

Update `.taskmaster/docs/skills-mcp-server-prd.md` for:
- Scope changes
- New requirements
- Architecture changes

### Code Comments

Add comments for:
- Complex logic
- Non-obvious decisions
- Performance considerations
- Security checks

## Security

### Security Best Practices

- Never commit credentials or tokens
- Validate all user inputs
- Sanitize file paths (prevent directory traversal)
- Handle errors gracefully (don't expose internals)
- Log security-relevant events

### Reporting Security Issues

Email security@your-org.com with:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

Do not create public issues for security vulnerabilities.

## Review Process

### Pull Request Checklist

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Commit messages follow format
- [ ] No merge conflicts
- [ ] Changelog updated (if applicable)

### Review Criteria

Reviewers will check:
- Code quality and style
- Test coverage
- Documentation completeness
- Performance implications
- Security considerations
- Backward compatibility

## Getting Help

- **Questions:** Open a GitHub Discussion
- **Bugs:** Create a GitHub Issue
- **Feature Requests:** Create a GitHub Issue with "enhancement" label
- **Chat:** Join our Discord/Slack (if available)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing!


