//! Test helpers: create a temporary dbt project, audit it, and filter findings by rule.

use std::path::{Path, PathBuf};

use crate::discovery::build_portfolio;
use crate::engine::run_audit;
use crate::model::Suggestion;

/// A temporary directory removed on drop.
pub struct TempProject {
    pub root: PathBuf,
}

impl Drop for TempProject {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.root);
    }
}

impl TempProject {
    /// Create a project from `(relative path, content)` pairs. A
    /// `dbt_project.yml` naming the project `demo` is added when absent.
    pub fn new(files: &[(&str, &str)]) -> Self {
        use std::sync::atomic::{AtomicUsize, Ordering};
        static N: AtomicUsize = AtomicUsize::new(0);
        let root = std::env::temp_dir().join(format!(
            "dbtq-test-{}-{}",
            std::process::id(),
            N.fetch_add(1, Ordering::SeqCst)
        ));
        let _ = std::fs::remove_dir_all(&root);
        std::fs::create_dir_all(&root).unwrap();
        let t = TempProject { root };
        if !files.iter().any(|(p, _)| p.ends_with("dbt_project.yml")) {
            t.write("dbt_project.yml", "name: demo\nversion: '1.0'\nprofile: demo\n");
        }
        for (p, c) in files {
            t.write(p, c);
        }
        t
    }

    pub fn write(&self, rel: &str, content: &str) {
        let p = self.root.join(rel);
        std::fs::create_dir_all(p.parent().unwrap()).unwrap();
        std::fs::write(p, content).unwrap();
    }

    pub fn path(&self) -> &Path {
        &self.root
    }

    /// Every active suggestion from a full audit.
    pub fn audit(&self) -> Vec<Suggestion> {
        let mut p = build_portfolio(&self.root);
        run_audit(&mut p).suggestions
    }

    /// Suggestions for one rule code.
    pub fn findings(&self, code: &str) -> Vec<Suggestion> {
        self.audit().into_iter().filter(|s| s.rule_id == code).collect()
    }
}
