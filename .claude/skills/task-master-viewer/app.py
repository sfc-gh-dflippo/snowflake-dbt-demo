"""
Task Master Viewer
A Streamlit application for viewing and editing Task Master tasks.json files.
"""

import streamlit as st
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Task Master Viewer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF !important;
    }

    h1, h2, h3 {
        color: #1B4D84 !important;
    }

    .stButton > button {
        background-color: #29B5E8 !important;
        color: white !important;
        border: none !important;
        border-radius: 0.5rem !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        text-align: left !important;
        height: auto !important;
        min-height: 2.5rem !important;
        padding: 0.5rem 1rem !important;
        justify-content: flex-start !important;
        display: flex !important;
        align-items: center !important;
    }

    .stButton > button:hover {
        background-color: #1B4D84 !important;
    }

    .stButton > button[kind="secondary"] {
        background-color: #F8FCFF !important;
        color: #1B4D84 !important;
        border: 2px solid #29B5E8 !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background-color: #D4F1FA !important;
    }

    .stButton > button > div {
        text-align: left !important;
        justify-content: flex-start !important;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# DATA MANAGEMENT
# ============================================================================

class TaskMasterEditor:
    """Handler for Task Master JSON file operations."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load tasks from JSON file."""
        if not self.file_path.exists():
            return {"master": {"tasks": [], "metadata": {}}}
        
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        # Handle both formats for backward compatibility
        # New format: {"master": {...}}
        # Old format: {"tags": {"master": {...}}}
        if "tags" in data:
            # Convert old format to new format
            return data["tags"]
        elif "master" in data:
            return data
        else:
            return {"master": {"tasks": [], "metadata": {}}}

    def _save_data(self) -> bool:
        """Save tasks to JSON file. Normalizes IDs before saving."""
        try:
            # Normalize all task IDs before saving
            for tag_data in self.data.values():
                if isinstance(tag_data, dict) and "tasks" in tag_data:
                    tasks = tag_data.get("tasks", [])
                    self._normalize_ids(tasks)
            
            with open(self.file_path, 'w') as f:
                json.dump(self.data, f, indent=2)
            
            # Reload data to ensure cache is fresh
            self.data = self._load_data()
            return True
        except Exception as e:
            st.error(f"Error saving file: {str(e)}")
            return False

    def _normalize_ids(self, items: List[Dict]) -> None:
        """Renumber items sequentially (1, 2, 3, ...) to eliminate gaps."""
        sorted_items = sorted(items, key=lambda x: x.get("id", 0))
        for idx, item in enumerate(sorted_items, start=1):
            item["id"] = idx
            # Recursively normalize subtasks
            if "subtasks" in item and item["subtasks"]:
                self._normalize_ids(item["subtasks"])

    def get_tags(self) -> List[str]:
        """Get list of available tags."""
        return list(self.data.keys())
    
    def get_tasks(self, tag: str) -> List[Dict]:
        """Get tasks for a specific tag."""
        return self.data.get(tag, {}).get("tasks", [])

    def add_task(self, tag: str, task: Dict) -> bool:
        """Add a new task."""
        if tag not in self.data:
            self.data[tag] = {"tasks": [], "metadata": {}}
        
        tasks = self.data[tag]["tasks"]
        if "id" not in task:
            task["id"] = max([t.get("id", 0) for t in tasks], default=0) + 1
        
        tasks.append(task)
        tasks.sort(key=lambda x: x.get("id", 0))
        return self._save_data()

    def update_task(self, tag: str, task_id: int, updated_task: Dict) -> bool:
        """Update an existing task."""
        tasks = self.get_tasks(tag)
        for i, task in enumerate(tasks):
            if task.get("id") == task_id:
                tasks[i] = updated_task
                return self._save_data()
        return False

    def delete_task(self, tag: str, task_id: int) -> bool:
        """Delete a task."""
        tasks = self.get_tasks(tag)
        self.data[tag]["tasks"] = [t for t in tasks if t.get("id") != task_id]
        return self._save_data()


def get_editor(file_path: str) -> TaskMasterEditor:
    """Get or create editor for the file path."""
    if "editor" not in st.session_state or st.session_state.get("editor_path") != file_path:
        st.session_state["editor"] = TaskMasterEditor(file_path)
        st.session_state["editor_path"] = file_path
    return st.session_state["editor"]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_status_emoji(status: str) -> str:
    """Get emoji for task status."""
    return {
        "pending": "⏳",
        "in-progress": "🔄",
        "done": "✅",
        "blocked": "🚫",
        "cancelled": "❌",
        "deferred": "⏸️",
        "review": "👀"
    }.get(status.lower(), "⚪")


def parse_id_string(id_str: str) -> Optional[List[int]]:
    """Parse ID string like '1', '1.2', '1.2.3' into list of integers."""
    try:
        return [int(p) for p in id_str.strip().split(".")]
    except ValueError:
        return None


def shift_items(items: List[Dict], from_id: int) -> None:
    """Shift items with ID >= from_id by 1."""
    items_to_shift = [item for item in items if item.get("id", 0) >= from_id]
    for item in reversed(sorted(items_to_shift, key=lambda x: x.get("id", 0))):
        item["id"] = item["id"] + 1


def get_item_at_path(all_tasks: List[Dict], id_parts: List[int]) -> Optional[Tuple[Dict, List[Dict]]]:
    """
    Navigate to an item using ID path and return (item, parent_list).
    Examples: [1] -> task, [1,2] -> subtask, [1,2,3] -> nested subtask
    """
    if not id_parts:
        return None

    # Find task
    task = next((t for t in all_tasks if t.get("id") == id_parts[0]), None)
    if not task:
        return None

    if len(id_parts) == 1:
        return task, all_tasks

    # Find subtask
    subtasks = task.get("subtasks", [])
    subtask = next((s for s in subtasks if s.get("id") == id_parts[1]), None)
    if not subtask:
        return None

    if len(id_parts) == 2:
        return subtask, subtasks

    # Find nested subtask
    nested_subtasks = subtask.get("subtasks", [])
    nested = next((n for n in nested_subtasks if n.get("id") == id_parts[2]), None)
    if not nested:
        return None

    return nested, nested_subtasks


def calculate_statistics(all_tasks: List[Dict]) -> Dict[str, int]:
    """Calculate task completion statistics."""
    total_tasks = len(all_tasks)
    total_subtasks = sum(len(t.get("subtasks", [])) for t in all_tasks)
    total_nested = sum(
        sum(len(s.get("subtasks", [])) for s in t.get("subtasks", []))
        for t in all_tasks
    )

    done_tasks = sum(1 for t in all_tasks if t.get("status") == "done")
    done_subtasks = sum(
        sum(1 for s in t.get("subtasks", []) if s.get("status") == "done")
        for t in all_tasks
    )
    done_nested = sum(
        sum(
            sum(1 for n in s.get("subtasks", []) if n.get("status") == "done")
            for s in t.get("subtasks", [])
        )
        for t in all_tasks
    )

    return {
        "total_tasks": total_tasks,
        "done_tasks": done_tasks,
        "total_subtasks": total_subtasks,
        "done_subtasks": done_subtasks,
        "total_nested": total_nested,
        "done_nested": done_nested
    }


# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_tree_item(task_id: str, title: str, status: str, item_key: str,
                     is_selected: bool, indent: int = 0) -> bool:
    """Render a tree item (task or subtask) and return True if clicked."""
    emoji = get_status_emoji(status)
    indent_spaces = "  " * indent
    label = f"{indent_spaces}{'↳ ' if indent > 0 else ''}{emoji} {task_id}: {title}"

    return st.button(
        label,
        key=item_key,
        use_container_width=True,
        type="primary" if is_selected else "secondary"
    )


def render_form_fields(item: Dict, all_tasks: List[Dict],
                       current_id: Optional[str] = None) -> Dict[str, Any]:
    """Render common form fields and return their values."""
    title = st.text_input("Title*", value=item.get("title", ""), 
                         help="Brief name for this task")
    description = st.text_area("Description", value=item.get("description", ""), height=150,
                               help="Summary of what this task involves")
    details = st.text_area("Implementation Details", value=item.get("details", ""), height=200,
                          help="Step-by-step implementation notes and progress logs")
    test_strategy = st.text_area("Test Strategy", value=item.get("testStrategy", ""), height=150,
                                 help="How to verify this task is complete")

    col1, col2 = st.columns(2)
    with col1:
        statuses = ["pending", "in-progress", "done", "blocked", "cancelled", "deferred", "review"]
        current_status = item.get("status", "pending")
        status = st.selectbox("Status", statuses,
                             index=statuses.index(current_status) if current_status in statuses else 0)
    with col2:
        priorities = ["low", "medium", "high"]
        current_priority = item.get("priority", "medium")
        priority = st.selectbox("Priority", priorities,
                               index=priorities.index(current_priority) if current_priority in priorities else 1)

    # Only top-level tasks can be dependencies
    available_deps = [t.get("id") for t in all_tasks]
    if current_id:
        # Remove current item from dependencies
        current_task_id = int(current_id.split(".")[0]) if "." in current_id else int(current_id)
        if current_task_id in available_deps:
            available_deps.remove(current_task_id)

    current_deps = item.get("dependencies", [])
    dependencies = st.multiselect("Dependencies", options=available_deps,
                                  default=[d for d in current_deps if d in available_deps],
                                  help="Select task IDs that must be completed before this task")

    return {
        "title": title,
        "description": description,
        "details": details,
        "testStrategy": test_strategy,
        "status": status,
        "priority": priority,
        "dependencies": dependencies
    }


# ============================================================================
# ITEM MANIPULATION
# ============================================================================

def create_item(editor: TaskMasterEditor, selected_tag: str, id_str: str,
                fields: Dict[str, Any], all_tasks: List[Dict]) -> None:
    """Create a new item (task/subtask/nested) based on ID format."""
    id_parts = parse_id_string(id_str)

    if not id_parts:
        st.error("Invalid ID format. Use numbers like: 1, 2.1, or 3.1.1")
        return

    if len(id_parts) == 1:
        # Create task
        task_id = id_parts[0]
        if any(t.get("id") == task_id for t in all_tasks):
            shift_items(all_tasks, task_id)
            for t in all_tasks:
                editor.update_task(selected_tag, t["id"] - 1, t)

        new_task = {**fields, "id": task_id, "subtasks": []}
        editor.add_task(selected_tag, new_task)
        st.success(f"✅ Task created!")

    elif len(id_parts) == 2:
        # Create subtask
        parent_id, subtask_id = id_parts
        result = get_item_at_path(all_tasks, [parent_id])
        if not result:
            st.error(f"Parent task {parent_id} not found!")
            return

        parent_task, _ = result
        subtasks = parent_task.get("subtasks", [])
        if any(s.get("id") == subtask_id for s in subtasks):
            shift_items(subtasks, subtask_id)

        new_subtask = {**fields, "id": subtask_id, "parentTaskId": parent_id}
        subtasks.append(new_subtask)
        subtasks.sort(key=lambda x: x.get("id", 0))
        parent_task["subtasks"] = subtasks
        editor.update_task(selected_tag, parent_id, parent_task)
        st.success(f"✅ Subtask created!")

    elif len(id_parts) == 3:
        # Create nested subtask
        parent_task_id, parent_subtask_id, nested_id = id_parts
        parent_task_result = get_item_at_path(all_tasks, [parent_task_id])
        if not parent_task_result:
            st.error(f"Parent task {parent_task_id} not found!")
            return

        parent_task, _ = parent_task_result
        parent_subtask_result = get_item_at_path(all_tasks, [parent_task_id, parent_subtask_id])
        if not parent_subtask_result:
            st.error(f"Parent subtask {parent_task_id}.{parent_subtask_id} not found!")
            return

        parent_subtask, _ = parent_subtask_result
        if "subtasks" not in parent_subtask:
            parent_subtask["subtasks"] = []

        nested_subtasks = parent_subtask["subtasks"]
        if any(n.get("id") == nested_id for n in nested_subtasks):
            shift_items(nested_subtasks, nested_id)

        new_nested = {**fields, "id": nested_id}
        nested_subtasks.append(new_nested)
        nested_subtasks.sort(key=lambda x: x.get("id", 0))
        parent_subtask["subtasks"] = nested_subtasks
        editor.update_task(selected_tag, parent_task_id, parent_task)
        st.success(f"✅ Nested subtask created!")

    st.session_state["selected_tree_item"] = None
    st.rerun()


def update_item(editor: TaskMasterEditor, selected_tag: str, current_id: str,
                new_id_str: str, fields: Dict[str, Any], all_tasks: List[Dict],
                current_item: Dict) -> None:
    """Update an item, handling ID changes and hierarchy conversions."""
    new_id_parts = parse_id_string(new_id_str)
    current_id_parts = parse_id_string(current_id)

    if not new_id_parts or not current_id_parts:
        st.error("Invalid ID format. Use numbers like: 1, 2.1, or 3.1.1")
        return

    # If ID unchanged at same level, just update in place
    if new_id_parts == current_id_parts:
        if len(current_id_parts) == 1:
            updated = {**fields, "id": current_id_parts[0],
                      "subtasks": current_item.get("subtasks", [])}
            editor.update_task(selected_tag, current_id_parts[0], updated)
            st.success("✅ Task updated!")
        elif len(current_id_parts) == 2:
            parent_task, _ = get_item_at_path(all_tasks, [current_id_parts[0]])
            updated = {**fields, "id": current_id_parts[1],
                      "parentTaskId": current_id_parts[0],
                      "subtasks": current_item.get("subtasks", [])}
            subtasks = parent_task.get("subtasks", [])
            for i, s in enumerate(subtasks):
                if s.get("id") == current_id_parts[1]:
                    subtasks[i] = updated
                    break
            editor.update_task(selected_tag, current_id_parts[0], parent_task)
            st.success("✅ Subtask updated!")
        else:
            parent_task, _ = get_item_at_path(all_tasks, [current_id_parts[0]])
            parent_subtask, _ = get_item_at_path(all_tasks, current_id_parts[:2])
            updated = {**fields, "id": current_id_parts[2]}
            nested = parent_subtask.get("subtasks", [])
            for i, n in enumerate(nested):
                if n.get("id") == current_id_parts[2]:
                    nested[i] = updated
                    break
            editor.update_task(selected_tag, current_id_parts[0], parent_task)
            st.success("✅ Nested subtask updated!")
        st.rerun()
        return

    # Otherwise, remove from current location and create at new location
    remove_item_at_path(editor, selected_tag, current_id_parts, all_tasks)
    create_item(editor, selected_tag, new_id_str, fields, all_tasks)


def remove_item_at_path(editor: TaskMasterEditor, selected_tag: str,
                       id_parts: List[int], all_tasks: List[Dict]) -> None:
    """Remove an item from its current location."""
    if len(id_parts) == 1:
        editor.delete_task(selected_tag, id_parts[0])
    elif len(id_parts) == 2:
        parent_task, _ = get_item_at_path(all_tasks, [id_parts[0]])
        parent_task["subtasks"] = [s for s in parent_task.get("subtasks", [])
                                    if s.get("id") != id_parts[1]]
        editor.update_task(selected_tag, id_parts[0], parent_task)
    else:
        parent_task, _ = get_item_at_path(all_tasks, [id_parts[0]])
        parent_subtask, _ = get_item_at_path(all_tasks, id_parts[:2])
        parent_subtask["subtasks"] = [n for n in parent_subtask.get("subtasks", [])
                                       if n.get("id") != id_parts[2]]
        editor.update_task(selected_tag, id_parts[0], parent_task)


# ============================================================================
# FORM RENDERING
# ============================================================================

def render_edit_form(editor: TaskMasterEditor, selected_tag: str,
                    selected_item: str, all_tasks: List[Dict]) -> None:
    """Render the appropriate edit form based on selected item."""

    if selected_item == "new_task":
        render_new_form(editor, selected_tag, all_tasks)
        return

    # Parse selected item
    if selected_item.startswith("task_"):
        current_id = selected_item.replace("task_", "")
    elif selected_item.startswith("subtask_"):
        parts = selected_item.replace("subtask_", "").split("_")
        current_id = f"{parts[0]}.{parts[1]}"
    elif selected_item.startswith("nested_"):
        parts = selected_item.replace("nested_", "").split("_")
        current_id = f"{parts[0]}.{parts[1]}.{parts[2]}"
    else:
        return

    id_parts = parse_id_string(current_id)
    if not id_parts:
        return

    result = get_item_at_path(all_tasks, id_parts)
    if not result:
        st.error("Item not found!")
        return

    item, parent_list = result

    # Render form
    st.markdown(f"### ✏️ Edit {current_id}")

    with st.form(key=f"form_{selected_item}"):
        col1, col2 = st.columns([1, 3])
        with col1:
            new_id_str = st.text_input("ID", value=current_id, 
                                       help="Change hierarchy: 1=task, 1.1=subtask, 1.1.1=nested. Items shift automatically.")

        st.divider()

        fields = render_form_fields(item, all_tasks, current_id)

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("💾 Save Changes", use_container_width=True):
                update_item(editor, selected_tag, current_id, new_id_str,
                           fields, all_tasks, item)
        with col2:
            if st.form_submit_button("🗑️ Delete", use_container_width=True):
                remove_item_at_path(editor, selected_tag, id_parts, all_tasks)
                st.success("Item deleted!")
                st.session_state["selected_tree_item"] = None
                st.rerun()


def render_new_form(editor: TaskMasterEditor, selected_tag: str,
                   all_tasks: List[Dict]) -> None:
    """Render form for creating a new item."""
    st.markdown("### ➕ Create New Item")

    with st.form(key="form_new_item"):
        default_id = max([t.get("id", 0) for t in all_tasks], default=0) + 1

        col1, col2 = st.columns([1, 3])
        with col1:
            new_id_str = st.text_input("ID", value=str(default_id),
                                       help="Choose position: 1=task, 2.1=subtask under task 2, 1.1.1=nested under subtask 1.1")

        st.divider()

        fields = render_form_fields({}, all_tasks)

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("✨ Create", use_container_width=True):
                if not fields["title"]:
                    st.error("Title is required!")
                else:
                    create_item(editor, selected_tag, new_id_str, fields, all_tasks)
        with col2:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.session_state["selected_tree_item"] = None
                st.rerun()


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application."""
    st.title("📋 Task Master Editor")
    
    # Help Section
    with st.expander("ℹ️ How to Use This Editor", expanded=False):
        st.markdown("""
        ### Quick Start
        1. **Select a task** in the tree view (left panel) to edit it
        2. **Edit fields** in the form (right panel)
        3. **Change the ID** to move or reorganize:
           - `1` = Task (top level)
           - `1.1` = Subtask (under task 1)
           - `1.1.1` = Nested subtask (under subtask 1.1)
        4. **Click Save** - All changes save immediately to tasks.json
        
        ### Features
        - **Tree View**: Click any task/subtask to edit
        - **Status Indicators**: ✅ done, 🔄 in-progress, ⏳ pending, 🚫 blocked
        - **Automatic Renumbering**: IDs clean up automatically (no gaps)
        - **Add Tasks**: Click ➕ button to create new items
        - **Delete**: Use 🗑️ button in edit form
        - **Switch Tags**: Use sidebar to change task context
        
        ### ID-Based Hierarchy
        Change an item's ID to reorganize it:
        - Task 5 → Subtask 2.3: Change `5` to `2.3`
        - Subtask 1.2 → Task 7: Change `1.2` to `7`
        - Create subtask: Use `2.1` format when adding new item
        
        💡 **Tip**: If you change to an existing ID, that item shifts down automatically.
        """)

    # Sidebar - Settings
    with st.sidebar:
        st.header("📊 Task Statistics")

        # File selection
        with st.expander("⚙️ Settings", expanded=False):
            # Walk up directory tree to find .taskmaster folder
            def find_taskmaster_dir():
                current = Path.cwd()
                for _ in range(10):  # Limit search depth
                    taskmaster_path = current / ".taskmaster" / "tasks" / "tasks.json"
                    if taskmaster_path.exists():
                        return taskmaster_path
                    if current.parent == current:  # Reached root
                        break
                    current = current.parent
                # Default fallback
                return Path.cwd() / ".taskmaster" / "tasks" / "tasks.json"
            
            default_path = find_taskmaster_dir()
            tasks_file = st.text_input(
                "Tasks File Path",
                value=str(default_path),
                help="Change this if your tasks.json is in a different location"
            )

        # Check file exists
        if not Path(tasks_file).exists():
            st.error(f"❌ Tasks file not found: {tasks_file}")
            return

        # Initialize editor
        editor = get_editor(tasks_file)

        # Force reload if file changed
        if st.button("🔄 Reload File", help="Reload tasks from file"):
            editor.data = editor._load_data()
            st.rerun()

        # Tag selection
        available_tags = editor.get_tags()
        if not available_tags:
            st.error("No tags found in tasks file.")
            return

        selected_tag = st.selectbox(
            "📑 Select Tag",
            available_tags,
            index=0 if "master" not in available_tags else available_tags.index("master")
        )

        # Get tasks
        all_tasks = editor.get_tasks(selected_tag)
        if all_tasks:
            stats = calculate_statistics(all_tasks)
            st.metric("Total Tasks Completed", f"{stats['done_tasks']}/{stats['total_tasks']}")
            if stats['total_subtasks'] > 0:
                st.metric("Total Subtasks Completed", f"{stats['done_subtasks']}/{stats['total_subtasks']}")
            if stats['total_nested'] > 0:
                st.metric("Total Nested Completed", f"{stats['done_nested']}/{stats['total_nested']}")

    # Main content
    st.subheader("Tasks")

    if not all_tasks:
        st.info("No tasks available. Create your first task!")
        return

    # Initialize selection state
    if "selected_tree_item" not in st.session_state:
        st.session_state["selected_tree_item"] = None

    # Two column layout
    tree_col, form_col = st.columns([1, 2])

    # Tree view
    with tree_col:
        st.markdown('<div style="font-size: 0.9em; max-height: 700px; overflow-y: auto;">',
                   unsafe_allow_html=True)

        for task in all_tasks:
            task_id = task.get("id")
            is_selected = st.session_state["selected_tree_item"] == f"task_{task_id}"
            if render_tree_item(str(task_id), task.get("title", "Untitled"),
                               task.get("status", "pending"), f"tree_task_{task_id}",
                               is_selected):
                st.session_state["selected_tree_item"] = f"task_{task_id}"
                st.rerun()

            # Render subtasks
            for subtask in task.get("subtasks", []):
                subtask_id = subtask.get("id")
                full_id = f"{task_id}.{subtask_id}"
                is_selected = st.session_state["selected_tree_item"] == f"subtask_{task_id}_{subtask_id}"
                if render_tree_item(full_id, subtask.get("title", "Untitled"),
                                   subtask.get("status", "pending"),
                                   f"tree_subtask_{task_id}_{subtask_id}",
                                   is_selected, indent=1):
                    st.session_state["selected_tree_item"] = f"subtask_{task_id}_{subtask_id}"
                    st.rerun()

                # Render nested subtasks
                for nested in subtask.get("subtasks", []):
                    nested_id = nested.get("id")
                    full_nested_id = f"{task_id}.{subtask_id}.{nested_id}"
                    is_selected = st.session_state["selected_tree_item"] == f"nested_{task_id}_{subtask_id}_{nested_id}"
                    if render_tree_item(full_nested_id, nested.get("title", "Untitled"),
                                       nested.get("status", "pending"),
                                       f"tree_nested_{task_id}_{subtask_id}_{nested_id}",
                                       is_selected, indent=2):
                        st.session_state["selected_tree_item"] = f"nested_{task_id}_{subtask_id}_{nested_id}"
                        st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # Form view
    with form_col:
        if st.button("➕ Add New Task", use_container_width=True, type="primary"):
            st.session_state["selected_tree_item"] = "new_task"
            st.rerun()

        st.markdown("---")

        selected_item = st.session_state.get("selected_tree_item")
        if selected_item:
            render_edit_form(editor, selected_tag, selected_item, all_tasks)
        else:
            st.info("👈 Select a task or subtask from the tree to edit it, or click '➕ Add New Task' above.")


if __name__ == "__main__":
    main()
