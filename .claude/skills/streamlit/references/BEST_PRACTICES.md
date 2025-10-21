# Streamlit Best Practices

Comprehensive guide to building production-ready Streamlit apps for Snowflake.

---

## Code Organization

### 1. Separate Data Access from UI

**✅ DO: Modular data access**
```python
# utils/data_loader.py
class DataQueries:
    def __init__(self, session):
        self.session = session
    
    def get_sales(self, start_date, end_date):
        return self.session.sql(f"""
            SELECT * FROM sales 
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
        """).to_pandas()
    
    def get_customers(self, region=None):
        query = "SELECT * FROM customers"
        if region:
            query += f" WHERE region = '{region}'"
        return self.session.sql(query).to_pandas()

# app.py
from utils.data_loader import DataQueries

session = get_snowpark_session()
queries = DataQueries(session)
df = queries.get_sales('2024-01-01', '2024-12-31')
st.dataframe(df)
```

**❌ DON'T: Mix SQL with UI code**
```python
# app.py - BAD
df = session.sql("SELECT * FROM sales WHERE...").to_pandas()
st.dataframe(df)
```

---

### 2. Cache Snowpark Session

**Always cache your session** to avoid reconnection overhead:

```python
@st.cache_resource
def get_snowpark_session():
    """Get or create Snowpark session (cached)"""
    try:
        return get_active_session()  # When running in Snowflake
    except:
        from snowflake.snowpark import Session
        return Session.builder.config('connection_name', 'default').create()
```

---

### 3. Use Forms for Multi-Field Input

**✅ DO: Group inputs in forms**
```python
with st.form("customer_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    
    if st.form_submit_button("Save"):
        save_customer(name, email, phone)
        st.success("Customer saved!")
```

**❌ DON'T: Trigger rerun on every input**
```python
# BAD - causes rerun on every keystroke
name = st.text_input("Name")
email = st.text_input("Email")
if st.button("Save"):
    save_customer(name, email)
```

---

### 4. Handle Errors Gracefully

**Provide helpful feedback:**

```python
try:
    save_customer(name, email)
    st.success("✅ Customer saved successfully!")
except ValueError as e:
    st.error(f"❌ Invalid input: {e}")
    st.info("💡 Tip: Check that email format is correct")
except Exception as e:
    st.error(f"❌ Unexpected error: {e}")
    st.info("💡 Please contact support if this persists")
```

---

### 5. Limit Column Nesting (Max 2 Levels)

**✅ DO: 2 levels maximum**
```python
col1, col2 = st.columns(2)
with col1:
    label_col, input_col = st.columns([1, 3])
    with label_col:
        st.markdown("**Name:**")
    with input_col:
        name = st.text_input("Name", label_visibility="collapsed")
```

**❌ DON'T: 3+ levels of nested columns**
```python
# BAD - causes Streamlit errors
col1, col2 = st.columns(2)
with col1:
    sub1, sub2 = st.columns(2)
    with sub1:
        deep1, deep2 = st.columns(2)  # Too deep!
```

---

## Performance Optimization

### 1. Cache Data Queries

```python
@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_sales_data(start_date, end_date):
    return session.sql(f"""
        SELECT * FROM sales 
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
    """).to_pandas()
```

### 2. Use Session State

```python
# Initialize state
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# Access throughout app
df = st.session_state.data
```

### 3. Lazy Load Heavy Computations

```python
if st.button("Run Analysis"):
    with st.spinner("Analyzing..."):
        result = expensive_computation()
        st.session_state.result = result

if 'result' in st.session_state:
    st.write(st.session_state.result)
```

---

## Snowflake-Specific Considerations

### 1. API Limitations

Some Streamlit features don't work in Snowflake:

| Feature | Status | Alternative |
|---------|--------|-------------|
| `st.dialog()` | ❌ Not supported | Use `st.expander()` or modals |
| `st.toggle()` | ❌ Not supported | Use `st.checkbox()` |
| `st.rerun()` | ⚠️ Older versions only | Use `st.experimental_rerun()` |
| `st.connection()` | ❌ Not supported | Use `get_active_session()` |

### 2. Package Availability

**Only Snowflake Anaconda packages available:**

```yaml
# environment.yml
name: streamlit_env
channels:
  - snowflake
dependencies:
  - pandas
  - plotly
  # ❌ DON'T include:
  # - streamlit  (already provided)
  # - snowflake-snowpark-python  (already provided)
```

**Check package availability:** https://repo.anaconda.com/pkgs/snowflake/

### 3. Python Version Support

**Don't specify Python version** - Snowflake controls this:

```yaml
# ❌ DON'T DO THIS
dependencies:
  - python=3.11  # Wrong!

# ✅ DO THIS
dependencies:
  - pandas
  - plotly
```

---

## Common Pitfalls

### DuplicateWidgetID Error

**Problem:** Two widgets with same implicit key

**Solution:** Add explicit keys
```python
st.text_input("Name", key="customer_name")
st.text_input("Name", key="product_name")
```

### IndentationError

**Check before deploying:**
```bash
python -c "import ast; ast.parse(open('streamlit_app/app.py').read())"
```

### Session Not Found (Local Development)

**Ensure proper fallback:**
```python
def get_snowpark_session():
    try:
        return get_active_session()  # Snowflake
    except:
        from snowflake.snowpark import Session
        return Session.builder.config('connection_name', 'default').create()
```

### Form Parameter Errors

**Some parameters not supported in Snowflake:**
- ❌ `border=False` in `st.form()`
- ❌ `border=True` in `st.container()`
- ❌ `hide_index=True` in `st.dataframe()` (older versions)

---

## Testing Strategy

### 1. Unit Tests (Pytest)

```python
# tests/test_data_loader.py
from utils.data_loader import DataQueries

def test_get_sales(mock_session):
    queries = DataQueries(mock_session)
    df = queries.get_sales('2024-01-01', '2024-01-31')
    assert not df.empty
```

### 2. Visual Testing (Browser Tool/Playwright MCP)

**Use for:**
- Form submission workflows
- Navigation testing
- Data display validation
- Responsive design checks
- Accessibility validation

**See:** [playwright-mcp skill](../../playwright-mcp/SKILL.md) for browser automation

### 3. Integration Tests

```python
# tests/test_integration.py
def test_app_loads(app_runner):
    """Test app loads without errors"""
    app_runner.run()
    assert not app_runner.exception
```

---

## Pre-Deployment Checklist

### Before Deploying:

- [ ] ✅ Fix all indentation errors
- [ ] ✅ Run unit tests: `pytest streamlit_app/tests/ -v`
- [ ] ✅ Test locally: `streamlit run streamlit_app/app.py`
- [ ] ✅ Verify forms and navigation with browser testing
- [ ] ✅ Check `environment.yml` only has non-default packages
- [ ] ✅ Remove development dependencies
- [ ] ✅ Test with different user roles/permissions
- [ ] ✅ Verify data access controls

### Deployment Commands:

```bash
# Method 1: Snowflake CLI (Recommended)
snow streamlit deploy --replace --connection default

# Method 2: Schemachange
schemachange deploy --config-folder . --connection-name default
```

### Post-Deployment:

- [ ] ✅ Verify app appears in Snowflake: Data → Databases → Schema → Streamlit
- [ ] ✅ Test all features in Snowflake UI
- [ ] ✅ Check permissions for different roles
- [ ] ✅ Monitor for errors in Streamlit logs

---

## Security Best Practices

### 1. Never Hardcode Credentials

**✅ DO:**
```python
session = get_active_session()  # Uses Snowflake auth
```

**❌ DON'T:**
```python
password = "secret123"  # Never do this!
```

### 2. Use Role-Based Access Control

```python
# Check user role
current_role = session.sql("SELECT CURRENT_ROLE()").collect()[0][0]

if current_role == "ADMIN":
    st.write("Admin features visible")
else:
    st.info("Admin access required")
```

### 3. Validate User Inputs

```python
def save_customer(name, email):
    if not name or len(name) < 2:
        raise ValueError("Name must be at least 2 characters")
    if "@" not in email:
        raise ValueError("Invalid email format")
    
    # Proceed with save
    ...
```

---

## Quick Reference

### Session Pattern
```python
@st.cache_resource
def get_snowpark_session():
    try:
        return get_active_session()
    except:
        return Session.builder.config('connection_name', 'default').create()
```

### Form Pattern
```python
with st.form("my_form"):
    field1 = st.text_input("Field 1")
    field2 = st.text_input("Field 2")
    if st.form_submit_button("Submit"):
        process(field1, field2)
```

### Error Handling Pattern
```python
try:
    result = process_data()
    st.success("✅ Success!")
except Exception as e:
    st.error(f"❌ Error: {e}")
```

### Caching Pattern
```python
@st.cache_data(ttl=600)
def load_data():
    return session.sql("SELECT * FROM table").to_pandas()
```

---

**Related Documentation:**
- `AUTHENTICATION.md` - Authentication methods
- `CONNECTION_CONFIG.md` - Connection configuration
- [playwright-mcp skill](../../playwright-mcp/SKILL.md) - Browser testing automation


