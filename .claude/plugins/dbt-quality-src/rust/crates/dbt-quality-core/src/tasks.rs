//! Editor tasks: adds the dbt-quality lint tasks to `.vscode/tasks.json`.

use std::path::Path;

use serde_json::{json, Value};

pub const TASK_LABELS: &[&str] = &["dbt: quality suggestions", "dbt: quality suggestions (watch, every 5 min)"];

/// The lint command the tasks run. `DBT_QUALITY_BIN` overrides the binary;
/// the plugin launcher sets it so tasks keep working across upgrades.
fn lint_binary() -> String {
    std::env::var("DBT_QUALITY_BIN")
        .ok()
        .or_else(|| std::env::current_exe().ok().map(|p| p.to_string_lossy().to_string()))
        .unwrap_or_else(|| "dbt-quality".into())
}

pub fn new_tasks() -> Vec<Value> {
    tasks_for(&lint_binary(), cfg!(windows))
}

fn tasks_for(bin: &str, windows: bool) -> Vec<Value> {
    let invoke = if windows {
        format!("& '{}' lint .", bin.replace('\'', "''"))
    } else {
        format!("'{}' lint .", bin.replace('\'', "'\\''"))
    };
    let (watch_command, watch_args) = if windows {
        ("powershell.exe", vec!["-NoProfile".to_string(), "-Command".to_string(), format!("while ($true) {{ Write-Output '>>> dbt-quality lint start'; {invoke}; Write-Output '>>> dbt-quality lint done'; Start-Sleep -Seconds 300 }}")])
    } else {
        ("sh", vec!["-c".to_string(), format!("while true; do printf '%s\\n' '>>> dbt-quality lint start'; {invoke}; printf '%s\\n' '>>> dbt-quality lint done'; sleep 300; done")])
    };
    let matcher = json!({
        "owner": "dbt-quality",
        "source": "dbt-quality",
        "fileLocation": ["relative", "${workspaceFolder}"],
        "pattern": {
            "regexp": r"^(.+?):(\d+):(\d+):(\d+):(\d+):\s+(error|warning|info):\s+\[(SSC-(?:EWI|FDM|PRF)-DBT[A-Z]{3}\d{4})\]\s+(.*)$",
            "file": 1, "line": 2, "column": 3, "endLine": 4, "endColumn": 5, "severity": 6, "code": 7, "message": 8,
        },
    });
    let mut watch = matcher.clone();
    watch["background"] = json!({
        "activeOnStart": true,
        "beginsPattern": "^>>> dbt-quality lint start$",
        "endsPattern": "^>>> dbt-quality lint done$",
    });
    vec![
        json!({
            "label": TASK_LABELS[0],
            "detail": "All dbt quality suggestions for the workspace, into the Problems panel.",
            "type": "process",
            "command": bin,
            "args": ["lint", "."],
            "options": {"cwd": "${workspaceFolder}"},
            "presentation": {"reveal": "silent", "panel": "dedicated", "clear": true},
            "problemMatcher": matcher,
            "group": "test",
        }),
        json!({
            "label": TASK_LABELS[1],
            "detail": "Auto-starts on folder open; re-runs the lint every 5 minutes for as long as this task keeps running, refreshing the Problems panel.",
            "type": "process",
            "command": watch_command,
            "args": watch_args,
            "options": {"cwd": "${workspaceFolder}"},
            "isBackground": true,
            "presentation": {"reveal": "silent", "panel": "dedicated", "clear": false},
            "problemMatcher": watch,
            "runOptions": {"runOn": "folderOpen"},
        }),
    ]
}

/// Add only the missing tasks, keeping every other task unchanged.
pub fn setup_tasks(path: &Path) -> Result<String, String> {
    let start = std::fs::canonicalize(path).unwrap_or_else(|_| path.to_path_buf());
    let root = start
        .ancestors()
        .find(|p| p.join("dbt_project.yml").is_file())
        .ok_or_else(|| format!("No dbt_project.yml found at or above {}.", start.display()))?;
    let tasks_path = root.join(".vscode/tasks.json");
    let config = if tasks_path.is_file() {
        let text = std::fs::read_to_string(&tasks_path).map_err(|e| e.to_string())?;
        let mut config: Value =
            serde_json::from_str(&text).map_err(|_| format!("{} is not valid JSON; add the tasks by hand.", tasks_path.display()))?;
        let existing: Vec<String> =
            config["tasks"].as_array().into_iter().flatten().filter_map(|t| t["label"].as_str().map(String::from)).collect();
        let missing: Vec<Value> = new_tasks().into_iter().filter(|t| !existing.iter().any(|e| t["label"] == e.as_str())).collect();
        if missing.is_empty() {
            return Ok(format!("dbt-quality tasks are already in {}.", tasks_path.display()));
        }
        if !config["tasks"].is_array() {
            config["tasks"] = json!([]);
        }
        config["tasks"].as_array_mut().unwrap().extend(missing);
        config
    } else {
        json!({"version": "2.0.0", "tasks": new_tasks()})
    };
    std::fs::create_dir_all(tasks_path.parent().unwrap()).map_err(|e| e.to_string())?;
    std::fs::write(&tasks_path, serde_json::to_string_pretty(&config).unwrap() + "\n").map_err(|e| e.to_string())?;
    Ok(format!(
        "Added the dbt-quality tasks to {}. Reload the window, or run \"dbt: quality suggestions (watch, every 5 min)\", to start the watcher.",
        tasks_path.display()
    ))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn process_task_preserves_executable_path() {
        let bin = r"C:\Program Files\dbt-quality\dbt-quality.exe";
        let tasks = tasks_for(bin, true);
        assert_eq!(tasks[0]["type"], "process");
        assert_eq!(tasks[0]["command"], bin);
        assert_eq!(tasks[0]["args"], json!(["lint", "."]));
        assert_eq!(tasks[1]["command"], "powershell.exe");
        assert!(tasks[1]["args"][2].as_str().unwrap().contains("Start-Sleep -Seconds 300"));
    }

    #[test]
    fn watch_paths_are_quoted_for_each_shell() {
        let unix = tasks_for("/opt/owner's tools/dbt-quality", false);
        assert!(unix[1]["args"][1].as_str().unwrap().contains("owner'\\''s tools"));
        let windows = tasks_for("C:/owner's tools/dbt-quality.exe", true);
        assert!(windows[1]["args"][2].as_str().unwrap().contains("owner''s tools"));
    }
}
