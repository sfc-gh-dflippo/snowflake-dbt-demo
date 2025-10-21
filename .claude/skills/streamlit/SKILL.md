---
name: Streamlit Development
description: Develop, test, and deploy Streamlit data applications on Snowflake. Use this skill when you're building interactive data apps, setting up local development environments, testing with pytest or Playwright, or deploying apps to Snowflake using Streamlit in Snowflake.
---

# Streamlit Development

Build interactive data applications using Streamlit, test them locally, and deploy to Snowflake's native Streamlit environment.

## Quick Start

**Execution Modes:**

- **Local Development** - PyPI packages, full environment
- **Snowflake Deployment** - Snowflake Anaconda packages, managed environment

## Connection Pattern

**Critical:** Support both local development and Snowflake deployment:

```python
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session

@st.cache_resource
def get_snowpark_session():
    try:
        return get_active_session()  # Snowflake
    except:
        return Session.builder.config('connection_name', 'default').create()  # Local
```

## Local Development

### Setup
```bash
# Install dependencies (pin Streamlit version to match Snowflake)
uv pip install --system -r requirements.txt

# Example requirements.txt
streamlit==1.46.0  # Must match Snowflake version
snowflake-snowpark-python
pandas
```

### Run Locally
```bash
streamlit run app.py
# Or with environment overrides
SNOWFLAKE_DATABASE=MY_DB streamlit run app.py
```

### Configuration
Create `~/.snowflake/connections.toml` for credentials.

## Testing

### Unit/Integration Tests
```bash
pytest streamlit_app/tests/ -v
```

### Browser Testing
Use Playwright MCP for interactive testing:
- Verify pages load without errors
- Test forms and navigation
- Check responsive design

See `TESTING_GUIDE.md` for patterns.

## Deployment

### Option 1: Snowflake CLI (Recommended)
```bash
snow streamlit deploy --replace -c default
```

### Option 2: Schemachange
Include Streamlit deployment in migration scripts.

## Key Patterns

- Separate data access from UI logic
- Cache Snowpark sessions
- Use forms for multi-field input
- Handle errors gracefully
- Limit column nesting (max 2 levels)

See `TROUBLESHOOTING.md` for common issues.

## Related Skills

**Complementary Testing:**
- **[playwright-mcp](../playwright-mcp/SKILL.md)** - Automate browser testing for Streamlit apps

Use playwright-mcp for visual testing, form validation, responsive design testing, and accessibility checks of your Streamlit applications.

---

## Resources

- `scripts/CONNECTION_PATTERN.py` - Required session pattern for local/Snowflake compatibility
- `references/AUTHENTICATION.md` - All authentication methods (SSO, key pair, OAuth)
- `references/CONNECTION_CONFIG.md` - Connection configuration and environment overrides
- `references/BEST_PRACTICES.md` - Performance optimization and code organization patterns
