//! dbt-quality: anti-pattern detection for dbt projects.

pub mod anchors;
pub mod annotate;
pub mod catalog;
pub mod ddl;
pub mod discovery;
pub mod engine;
pub mod fix_columns;
pub mod graph;
pub mod html;
pub mod jinja;
pub mod model;
pub mod projection;
pub mod provenance;
pub mod report;
pub mod rules;
pub mod sqlutil;
pub mod tasks;
#[doc(hidden)]
pub mod testing;
pub mod waivers;

/// The pinned dbt commit, from `vendor/DBT_PIN.md`.
pub const DBT_PIN_SHA: &str = "be18b6572ffd2066ffb038dee5d82bbbe9cdfc1a";
pub const DBT_PIN_VERSION: &str = "2.0.8";
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
