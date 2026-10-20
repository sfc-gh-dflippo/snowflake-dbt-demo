//! The model dependency graph, built from each model's `ref()` calls.
//!
//! The audit reads model files directly with the dbt Jinja parser. It does
//! not run dbt and does not read `target/manifest.json`, because a manifest
//! can be older than the files. A `ref()` whose name is built at render time
//! (for example from a variable) is not found, so the graph can miss edges;
//! it never adds edges that the files do not contain.

use std::collections::{BTreeMap, BTreeSet};

use crate::discovery::ModelFile;

#[derive(Debug, Clone, Default)]
pub struct Graph {
    /// Model name -> names of the models it refs in the same project.
    pub parents: BTreeMap<String, BTreeSet<String>>,
    /// Model name -> names of the models that ref it in the same project.
    pub children: BTreeMap<String, BTreeSet<String>>,
}

impl Graph {
    /// Build the graph for one project. A ref to a name that is not a model
    /// in this project (a package or another project) is not an edge.
    pub fn from_models(models: &[ModelFile]) -> Self {
        let names: BTreeSet<&str> = models.iter().map(|m| m.name.as_str()).collect();
        let mut graph = Graph::default();
        for model in models {
            for parent in model.refs.iter().filter(|r| names.contains(r.as_str()) && **r != model.name) {
                graph.parents.entry(model.name.clone()).or_default().insert(parent.clone());
                graph.children.entry(parent.clone()).or_default().insert(model.name.clone());
            }
        }
        graph
    }

    pub fn parent_names(&self, model: &str) -> Vec<String> {
        self.parents.get(model).map(|p| p.iter().cloned().collect()).unwrap_or_default()
    }

    pub fn child_names(&self, model: &str) -> Vec<String> {
        self.children.get(model).map(|c| c.iter().cloned().collect()).unwrap_or_default()
    }

    pub fn child_count(&self, model: &str) -> usize {
        self.children.get(model).map_or(0, BTreeSet::len)
    }
}
