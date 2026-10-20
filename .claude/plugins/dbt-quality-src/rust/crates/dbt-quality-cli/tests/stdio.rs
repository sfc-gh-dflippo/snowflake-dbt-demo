//! Run `dbt-quality mcp` over stdio against a temporary git project.

use std::io::{BufRead, BufReader, Write};
use std::path::Path;
use std::process::{Command, Stdio};

use dbt_quality_core::testing::TempProject;
use serde_json::{json, Value};

fn git(root: &Path, args: &[&str]) {
    let ok = Command::new("git")
        .arg("-C")
        .arg(root)
        .args(["-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"])
        .args(args)
        .status()
        .unwrap()
        .success();
    assert!(ok, "git {args:?}");
}

#[test]
fn stdio_agent_loop() {
    let t = TempProject::new(&[("models/a.sql", "select a.x\nfrom a, b\nwhere a.id = b.id\n")]);
    git(t.path(), &["init", "-q"]);
    git(t.path(), &["add", "-A"]);
    git(t.path(), &["commit", "-q", "-m", "x"]);
    let root = t.path().to_string_lossy().to_string();

    let mut child = Command::new(env!("CARGO_BIN_EXE_dbt-quality"))
        .arg("mcp")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .unwrap();
    let mut stdin = child.stdin.take().unwrap();
    let mut stdout = BufReader::new(child.stdout.take().unwrap());
    let mut id = 0;
    let mut rpc = |method: &str, params: Value| -> Value {
        id += 1;
        writeln!(stdin, "{}", json!({"jsonrpc": "2.0", "id": id, "method": method, "params": params})).unwrap();
        let mut line = String::new();
        stdout.read_line(&mut line).unwrap();
        let v: Value = serde_json::from_str(&line).unwrap();
        assert_eq!(v["id"], id, "{v}");
        v["result"].clone()
    };
    let call = |rpc: &mut dyn FnMut(&str, Value) -> Value, name: &str, args: Value| -> Value {
        let r = rpc("tools/call", json!({"name": name, "arguments": args}));
        assert_eq!(r["isError"], false, "{name}: {r}");
        r["structuredContent"].clone()
    };

    let init = rpc("initialize", json!({"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t", "version": "0"}}));
    assert_eq!(init["serverInfo"]["name"], "dbt-quality");
    let names: Vec<String> = rpc("tools/list", json!({}))["tools"].as_array().unwrap().iter().map(|t| t["name"].as_str().unwrap().to_string()).collect();
    assert_eq!(names, ["report", "findings", "annotate", "fix_columns", "rules", "version"]);
    let rule = call(&mut rpc, "rules", json!({"code": "SSC-EWI-DBTSQL0007"}));
    assert_eq!(rule["code"], "SSC-EWI-DBTSQL0007");

    // The default out_dir is outside the project, so the tree stays clean.
    let rep = call(&mut rpc, "report", json!({"path": root}));
    let json_path = rep["json"].as_str().unwrap();
    assert!(Path::new(json_path).is_file());
    assert!(!Path::new(json_path).starts_with(std::fs::canonicalize(t.path()).unwrap()), "{json_path}");
    let original_json: Value = serde_json::from_str(&std::fs::read_to_string(json_path).unwrap()).unwrap();
    assert!(original_json.get("html").is_none());
    let rejected = rpc("tools/call", json!({"name": "report", "arguments": {"path": root, "html": false, "include_models": true}}));
    assert_eq!(rejected["isError"], true);
    assert!(rejected["content"][0]["text"].as_str().unwrap().contains("requires `html: true`"));
    let wrong_type = rpc("tools/call", json!({"name": "report", "arguments": {"path": root, "include_models": "true"}}));
    assert_eq!(wrong_type["isError"], true);
    let included = call(&mut rpc, "report", json!({"path": root, "include_models": true}));
    assert_eq!(included.as_object().unwrap().keys().collect::<Vec<_>>(), rep.as_object().unwrap().keys().collect::<Vec<_>>());
    let included_json: Value = serde_json::from_str(&std::fs::read_to_string(included["json"].as_str().unwrap()).unwrap()).unwrap();
    assert!(included_json.get("html").is_none());
    assert_eq!(included_json["suggestions"], original_json["suggestions"]);
    assert_eq!(included["counts"], rep["counts"]);

    let dry = call(&mut rpc, "annotate", json!({"path": root}));
    assert_eq!(dry["written"], false);
    assert!(dry["diff"].as_str().unwrap().contains("SSC-EWI-DBTSQL0007"));
    let w = call(&mut rpc, "annotate", json!({"path": root, "dry_run": false}));
    assert_eq!(w["written"], true, "{w}");
    assert!(std::fs::read_to_string(t.path().join("models/a.sql")).unwrap().contains("--** SSC-EWI-DBTSQL0007"));

    // fix_columns: no DDL is an error; a scai DDL dry run returns records and writes nothing.
    let no_ddl = rpc("tools/call", json!({"name": "fix_columns", "arguments": {"path": root}}));
    assert_eq!(no_ddl["isError"], true);
    let ddl = concat!(env!("CARGO_MANIFEST_DIR"), "/../../tests/fixtures/scai/sample_store");
    t.write("models/categories.sql", "select categoryname as CategoryName from {{ ref('s') }}");
    let fx = call(&mut rpc, "fix_columns", json!({"path": root, "ddl": [ddl]}));
    assert_eq!(fx["written"], false);
    assert_eq!(fx["files"][0]["status"], "changed", "{fx}");
    assert!(std::fs::read_to_string(t.path().join("models/categories.sql")).unwrap().starts_with("select categoryname as"));

    drop(stdin);
    assert!(child.wait().unwrap().success());
}
