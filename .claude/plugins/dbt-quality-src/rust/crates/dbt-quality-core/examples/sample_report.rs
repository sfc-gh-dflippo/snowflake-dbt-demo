//! Generate the sample from committed synthetic fixtures, never from local audit output.

use std::ffi::OsString;
use std::fs;
use std::io::{self, Write};
use std::path::{Component, Path, PathBuf};
use std::process::{Command, ExitCode};
use std::sync::atomic::{AtomicU64, Ordering};

use dbt_quality_core::discovery::{
    AuditConfig, PortfolioContext, build_project_context, find_projects, load_yaml_str, set_labels,
};
use dbt_quality_core::engine::run_audit;
use dbt_quality_core::html;
use dbt_quality_core::report::{HtmlReportOptions, build_html_report, build_report};
use serde_json::{Value, json};
use sha2::{Digest, Sha256};

const FIXTURE_PATH: &str = "rust/tests/fixtures/ewi_estate";
const SAMPLE_DATE: &str = "2026-10-15T00:00:00+00:00";
const GENERATOR_COMMAND: &str = "cargo +1.96 run --locked --manifest-path rust/Cargo.toml -p dbt-quality-core --example sample_report";
const SAMPLE_NOTICE: &str = "Synthetic test data from four fixture projects. This sample does not cover every rule. The fixed date makes regeneration reproducible; it is not an audit run time.";

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

#[derive(Debug, PartialEq)]
struct Options {
    check: bool,
    output: PathBuf,
    help: bool,
}

impl Options {
    fn parse(arguments: impl IntoIterator<Item = OsString>, product: &Path) -> Result<Self> {
        let mut options = Self {
            check: false,
            output: product.join("sample-report.html"),
            help: false,
        };
        let mut output_seen = false;
        let mut arguments = arguments.into_iter();
        while let Some(argument) = arguments.next() {
            match argument.to_str() {
                Some("--check") if !options.check => options.check = true,
                Some("--output") if !output_seen => {
                    let path = arguments.next().ok_or("--output requires a file path")?;
                    if path.is_empty() || path.to_string_lossy().starts_with("--") {
                        return Err("--output requires a file path".into());
                    }
                    options.output = PathBuf::from(path);
                    output_seen = true;
                }
                Some("--help" | "-h") => options.help = true,
                _ => {
                    return Err(format!(
                        "Unknown or repeated argument: {}",
                        argument.to_string_lossy()
                    )
                    .into());
                }
            }
        }
        Ok(options)
    }
}

struct Scratch(PathBuf);

impl Scratch {
    fn new() -> Result<Self> {
        static NEXT: AtomicU64 = AtomicU64::new(0);
        for _ in 0..100 {
            let path = std::env::temp_dir().join(format!(
                "dbt-quality-sample-{}-{}",
                std::process::id(),
                NEXT.fetch_add(1, Ordering::Relaxed),
            ));
            match fs::create_dir(&path) {
                Ok(()) => return Ok(Self(fs::canonicalize(path)?)),
                Err(error) if error.kind() == io::ErrorKind::AlreadyExists => continue,
                Err(error) => return Err(error.into()),
            }
        }
        Err("Could not create a new scratch directory".into())
    }
}

impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}

#[derive(Debug)]
struct FixtureFile {
    path: String,
    bytes: Vec<u8>,
}

struct FixtureSnapshot {
    tree_sha: String,
    files: Vec<FixtureFile>,
}

fn git(directory: &Path, arguments: &[&str]) -> Result<Vec<u8>> {
    let output = Command::new("git")
        .arg("-C")
        .arg(directory)
        .args(arguments)
        .output()?;
    if !output.status.success() {
        return Err(format!(
            "git {} failed: {}",
            arguments.join(" "),
            String::from_utf8_lossy(&output.stderr).trim()
        )
        .into());
    }
    Ok(output.stdout)
}

fn generated_path(path: &str) -> bool {
    path.split('/').any(|part| {
        dbt_quality_core::discovery::EXCLUDED_DIRS.contains(&part)
            || matches!(
                part,
                "manifest.json" | "partial_parse.msgpack" | "run_results.json" | "catalog.json"
            )
    })
}

fn tree_entries(bytes: &[u8]) -> Result<Vec<(String, String)>> {
    let mut entries = Vec::new();
    for record in bytes
        .split(|byte| *byte == 0)
        .filter(|record| !record.is_empty())
    {
        let record = std::str::from_utf8(record)?;
        let (header, path) = record.split_once('\t').ok_or("Invalid Git tree record")?;
        let fields: Vec<_> = header.split_whitespace().collect();
        if fields.len() != 3 || !matches!(fields[0], "100644" | "100755") || fields[1] != "blob" {
            return Err("Synthetic fixtures must contain only regular tracked files".into());
        }
        if path.is_empty()
            || path.contains(['\\', ':'])
            || path.chars().any(char::is_control)
            || !Path::new(path)
                .components()
                .all(|part| matches!(part, Component::Normal(_)))
            || path
                .split('/')
                .any(|part| part.is_empty() || matches!(part, "." | ".."))
        {
            return Err("Unsafe path in synthetic fixture tree".into());
        }
        if !fields[2].bytes().all(|byte| byte.is_ascii_hexdigit())
            || !matches!(fields[2].len(), 40 | 64)
        {
            return Err("Invalid Git blob identity".into());
        }
        if !generated_path(path) {
            entries.push((path.to_string(), fields[2].to_string()));
        }
    }
    entries.sort();
    if entries.is_empty() || entries.windows(2).any(|pair| pair[0].0 == pair[1].0) {
        return Err("The synthetic fixture tree is empty or contains duplicate paths".into());
    }
    Ok(entries)
}

impl FixtureSnapshot {
    fn load(product: &Path) -> Result<Self> {
        let repository = PathBuf::from(
            String::from_utf8(git(product, &["rev-parse", "--show-toplevel"])?)?.trim(),
        );
        let fixture = product.join(FIXTURE_PATH);
        let relative = fixture
            .strip_prefix(&repository)?
            .to_str()
            .ok_or("Fixture path must be UTF-8")?
            .replace('\\', "/");
        // The tree ID changes only when fixture content changes, not on each source commit.
        let tree_sha =
            String::from_utf8(git(product, &["rev-parse", &format!("HEAD:{relative}")])?)?
                .trim()
                .to_string();
        let entries = tree_entries(&git(
            product,
            &["ls-tree", "--full-tree", "-r", "-z", &tree_sha],
        )?)?;
        let mut files = Vec::with_capacity(entries.len());
        for (path, blob) in entries {
            files.push(FixtureFile {
                path,
                bytes: git(product, &["cat-file", "blob", &blob])?,
            });
        }
        Ok(Self { tree_sha, files })
    }

    fn copy_to(&self, root: &Path) -> Result<()> {
        for file in &self.files {
            let destination = root.join(&file.path);
            fs::create_dir_all(
                destination
                    .parent()
                    .ok_or("Fixture has no parent directory")?,
            )?;
            fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(destination)?
                .write_all(&file.bytes)?;
        }
        Ok(())
    }

    fn sha256(&self) -> String {
        let mut digest = Sha256::new();
        for file in &self.files {
            digest.update((file.path.len() as u64).to_be_bytes());
            digest.update(file.path.as_bytes());
            digest.update((file.bytes.len() as u64).to_be_bytes());
            digest.update(&file.bytes);
        }
        format!("{digest:x}", digest = digest.finalize())
    }

    fn sensitive_values(&self) -> Result<Vec<String>> {
        fn collect(value: &Value, values: &mut Vec<String>) {
            match value {
                Value::Object(fields) => {
                    for (name, value) in fields {
                        if matches!(
                            name.to_ascii_lowercase().as_str(),
                            "password"
                                | "pass"
                                | "token"
                                | "private_key"
                                | "private_key_passphrase"
                        ) && let Some(text) = value.as_str()
                            && !text.is_empty()
                            && !text.contains("{{")
                        {
                            values.push(text.to_string());
                        }
                        collect(value, values);
                    }
                }
                Value::Array(items) => items.iter().for_each(|item| collect(item, values)),
                _ => {}
            }
        }
        let mut values = Vec::new();
        for file in &self.files {
            if matches!(
                Path::new(&file.path)
                    .file_name()
                    .and_then(|name| name.to_str()),
                Some("profiles.yml" | "profiles.yaml" | "dbt_project.yml")
            ) {
                let source = std::str::from_utf8(&file.bytes)?;
                let config = load_yaml_str(source)
                    .map_err(|_| "Could not check fixture configuration for sensitive literals")?;
                collect(&config, &mut values);
            }
        }
        Ok(values)
    }
}

fn replace_roots(value: &mut Value, replacements: &[(String, String)]) {
    let clean = |text: &str| {
        replacements
            .iter()
            .fold(text.to_string(), |result, (from, to)| {
                result.replace(from, to)
            })
    };
    match value {
        Value::String(text) => *text = clean(text),
        Value::Array(items) => items
            .iter_mut()
            .for_each(|item| replace_roots(item, replacements)),
        Value::Object(fields) => {
            let old = std::mem::take(fields);
            for (name, mut item) in old {
                replace_roots(&mut item, replacements);
                fields.insert(clean(&name), item);
            }
        }
        _ => {}
    }
}

/// Maps the scratch copy to the fixture's full path in this checkout, so the sample
/// records absolute paths that exist on the machine that generated it.
fn path_replacements(root: &Path, product: &Path) -> Vec<(String, String)> {
    let target = fixture_root(product);
    let mut replacements = Vec::new();
    let text = root.to_string_lossy();
    for spelling in [text.to_string(), text.replace('\\', "/")] {
        if !spelling.is_empty() {
            replacements.push((spelling, target.clone()));
        }
    }
    replacements.sort_by(|left, right| right.0.len().cmp(&left.0.len()).then(left.0.cmp(&right.0)));
    replacements.dedup();
    replacements
}

/// The full path of the committed fixtures in this checkout.
fn fixture_root(product: &Path) -> String {
    product.join(FIXTURE_PATH).to_string_lossy().to_string()
}

/// Key under which the sample records the checkout it was generated in.
const CHECKOUT_KEY: &str = "\"checkout\":\"";
const CHECKOUT_TOKEN: &str = "<checkout>";

/// Replaces the checkout path recorded in `html` with a fixed token, so a sample made in
/// one checkout compares equal to the same sample made in another.
fn normalize_checkout(html: &str) -> String {
    let Some(start) = html.find(CHECKOUT_KEY).map(|i| i + CHECKOUT_KEY.len()) else { return html.to_string() };
    let Some(length) = html[start..].find('"') else { return html.to_string() };
    let checkout = &html[start..start + length];
    if checkout.is_empty() { html.to_string() } else { html.replace(checkout, CHECKOUT_TOKEN) }
}

fn contains_text(value: &Value, text: &str) -> bool {
    match value {
        Value::String(value) => value.contains(text),
        Value::Array(items) => items.iter().any(|item| contains_text(item, text)),
        Value::Object(fields) => fields
            .iter()
            .any(|(name, item)| name.contains(text) || contains_text(item, text)),
        _ => false,
    }
}

fn sample_payload(snapshot: &FixtureSnapshot, root: &Path, product: &Path) -> Result<Value> {
    let root = fs::canonicalize(root)?;
    // Explicit defaults prevent a parent directory's private audit config from changing the sample.
    let config = AuditConfig::default();
    let mut projects: Vec<_> = find_projects(&root)
        .iter()
        .map(|path| build_project_context(path, &root, &config))
        .collect();
    set_labels(&mut projects);
    let mut names: Vec<_> = projects
        .iter()
        .map(|project| project.name.as_str())
        .collect();
    names.sort();
    if names
        != [
            "migrated_flow_a",
            "migrated_flow_b",
            "migrated_flow_c",
            "native_core",
        ]
    {
        return Err("The sample requires the four expected synthetic fixture projects".into());
    }
    let mut portfolio = PortfolioContext {
        root: root.clone(),
        projects,
        config,
        read_errors: vec![],
    };
    let result = run_audit(&mut portfolio);
    if !result.errors.is_empty() || result.suggestions.is_empty() {
        return Err(
            "The sample audit failed or returned no findings; run core tests for details".into(),
        );
    }
    let options = HtmlReportOptions {
        include_models: true,
        ..Default::default()
    };
    let report = build_report(&result, &fixture_root(product));
    let mut report = build_html_report(&report, &portfolio, &options);
    report["generated"] = SAMPLE_DATE.into();
    report["provenance"] = json!({
        "kind": "synthetic-test-data", "notice": SAMPLE_NOTICE,
        "fixture_root": fixture_root(product), "checkout": product.to_string_lossy(), "fixture_git_tree": snapshot.tree_sha,
        "fixture_sha256": snapshot.sha256(), "fixture_file_count": snapshot.files.len(),
        "generator": format!("dbt-quality {} sample_report", dbt_quality_core::VERSION),
        "command": GENERATOR_COMMAND, "generated_date_policy": "fixed display date, not execution time",
        "settings": { "include_models": true, "categories": [], "min_level": "information", "audit_config": "built-in defaults" },
        "source_policy": "Committed regular fixture files only. Generated directories and artifacts are excluded. The report includes the text of each SQL, Python, YAML, or shell file that a finding names. Profiles and credentials are audited but never included.",
        "sections": ["overview", "categories", "projects", "remediation", "findings", "suppressed", "checks", "rules"],
    });
    let source_notice = report["html"]["source_notice"]
        .as_str()
        .ok_or("Missing HTML source contract")?;
    report["html"]["source_notice"] = format!("{SAMPLE_NOTICE} {source_notice}").into();
    let replacements = path_replacements(&root, product);
    replace_roots(&mut report, &replacements);
    for (path, _) in &replacements {
        if contains_text(&report, path) {
            return Err("The sample still contains a scratch path".into());
        }
    }
    for literal in snapshot.sensitive_values()? {
        if contains_text(&report, &literal) {
            return Err(
                "The sample contains a sensitive fixture literal; refuse to write it".into(),
            );
        }
    }
    let models = report["html"]["models"]
        .as_object()
        .ok_or("Missing HTML model map")?;
    if models.is_empty()
        || models
            .values()
            .any(|model| model["source"]["status"] != "included")
    {
        return Err("The sample requires complete, verified model snapshots".into());
    }
    Ok(report)
}

fn write_or_check(path: &Path, content: &[u8], check: bool) -> Result<()> {
    if check {
        let existing = fs::read(path).map_err(|error| {
            format!(
                "Cannot check {}: {error}. Regenerate with `{GENERATOR_COMMAND}`.",
                path.display()
            )
        })?;
        if normalize_checkout(&String::from_utf8_lossy(&existing)) != normalize_checkout(&String::from_utf8_lossy(content)) {
            return Err(format!(
                "Sample report is out of date. Regenerate with `{GENERATOR_COMMAND}`."
            )
            .into());
        }
    } else {
        fs::write(path, content)?;
    }
    Ok(())
}

fn run() -> Result<()> {
    let product = fs::canonicalize(Path::new(env!("CARGO_MANIFEST_DIR")).join("../../.."))?;
    let options = Options::parse(std::env::args_os().skip(1), &product)?;
    if options.help {
        println!(
            "Generate sample-report.html from committed synthetic fixtures.\n\n{GENERATOR_COMMAND} -- [--check] [--output PATH]\n\n--check        Check byte-for-byte drift without writing.\n--output PATH  Use a different output file. Its parent must exist.\n\nRequires Git and the source checkout. Local fixture edits and generated files are not used."
        );
        return Ok(());
    }
    let snapshot = FixtureSnapshot::load(&product)?;
    let scratch = Scratch::new()?;
    // Some findings name the audit root, so keep its basename stable across runs.
    let root = scratch.0.join("ewi_estate");
    snapshot.copy_to(&root)?;
    let report = sample_payload(&snapshot, &root, &product)?;
    let rendered = html::render(&report);
    write_or_check(&options.output, rendered.as_bytes(), options.check)?;
    println!(
        "{} {} ({} bytes; fixture tree {})",
        if options.check { "Checked" } else { "Wrote" },
        options.output.display(),
        rendered.len(),
        snapshot.tree_sha
    );
    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("sample_report: {error}");
            ExitCode::FAILURE
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn arguments_are_explicit_and_check_does_not_change_output() {
        let product = Path::new("product");
        let parse = |args: &[&str]| Options::parse(args.iter().map(OsString::from), product);
        assert_eq!(
            parse(&[]).unwrap().output,
            product.join("sample-report.html")
        );
        let options = parse(&["--check", "--output", "a path/sample.html"]).unwrap();
        assert!(options.check);
        assert_eq!(options.output, Path::new("a path/sample.html"));
        for args in [
            vec!["--output"],
            vec!["--output", "--check"],
            vec!["--check", "--check"],
            vec!["--unknown"],
        ] {
            assert!(parse(&args).is_err());
        }
    }

    #[test]
    fn git_tree_rejects_non_regular_and_unsafe_paths_and_excludes_artifacts() {
        let blob = "0".repeat(40);
        let record = |mode: &str, path: &str| format!("{mode} blob {blob}\t{path}\0");
        for (mode, path) in [
            ("120000", "models/link.sql"),
            ("100644", "../outside.sql"),
            ("100644", "/outside.sql"),
            ("100644", "C:\\outside.sql"),
            ("100644", "a/./file.sql"),
        ] {
            assert!(tree_entries(record(mode, path).as_bytes()).is_err());
        }
        let listing = [
            "model.sql",
            "target/manifest.json",
            "manifest.json",
            "dbt_packages/pkg/model.sql",
            "logs/dbt.log",
            "run_results.json",
        ]
        .map(|path| record("100644", path))
        .join("");
        assert_eq!(
            tree_entries(listing.as_bytes()).unwrap(),
            vec![("model.sql".into(), blob)]
        );
    }

    #[test]
    fn nested_paths_and_error_messages_are_sanitized() {
        let mut report = json!({
            "error": "read /tmp/sample/model.sql", "nested": [{"/tmp/sample/key": "C:\\scratch\\sample\\model.sql"}],
            "reference": "https://docs.getdbt.com/reference",
        });
        replace_roots(
            &mut report,
            &[
                ("/tmp/sample".into(), FIXTURE_PATH.into()),
                ("C:\\scratch\\sample".into(), FIXTURE_PATH.into()),
            ],
        );
        assert!(!contains_text(&report, "/tmp/sample"));
        assert!(!contains_text(&report, "C:\\scratch"));
        assert!(
            report["nested"][0]
                .get(format!("{FIXTURE_PATH}/key"))
                .is_some()
        );
        assert_eq!(report["reference"], "https://docs.getdbt.com/reference");
    }

    #[test]
    fn drift_check_does_not_create_or_rewrite_files() {
        let scratch = Scratch::new().unwrap();
        let output = scratch.0.join("sample.html");
        assert!(write_or_check(&output, b"new", true).is_err());
        assert!(!output.exists());
        write_or_check(&output, b"old", false).unwrap();
        assert!(write_or_check(&output, b"new", true).is_err());
        assert_eq!(fs::read(&output).unwrap(), b"old");
        write_or_check(&output, b"old", true).unwrap();
    }

    #[test]
    fn drift_check_ignores_the_checkout_path() {
        let scratch = Scratch::new().unwrap();
        let output = scratch.0.join("sample.html");
        let page = |checkout: &str, text: &str| format!("{{\"checkout\":\"{checkout}\",\"path\":\"{checkout}/rust/a.sql\"}}<p>{checkout}/rust/a.sql {text}</p>");
        write_or_check(&output, page("/home/a/dbt-quality", "same").as_bytes(), false).unwrap();
        write_or_check(&output, page("/work/b/dbt-quality", "same").as_bytes(), true).unwrap();
        assert!(write_or_check(&output, page("/work/b/dbt-quality", "changed").as_bytes(), true).is_err());
    }

    #[test]
    fn sample_is_identical_in_different_roots_and_contains_only_safe_sources() {
        let product =
            fs::canonicalize(Path::new(env!("CARGO_MANIFEST_DIR")).join("../../..")).unwrap();
        let snapshot = FixtureSnapshot::load(&product).unwrap();
        assert!(!snapshot.files.iter().any(|file| generated_path(&file.path)));
        assert!(
            snapshot
                .files
                .iter()
                .any(|file| file.path.ends_with("profiles.yml"))
        );
        let first = Scratch::new().unwrap();
        let second = Scratch::new().unwrap();
        let root_one = first.0.join("first fixture/ewi_estate");
        let root_two = second.0.join("different/nested fixture/ewi_estate");
        fs::create_dir_all(&root_one).unwrap();
        fs::create_dir_all(&root_two).unwrap();
        // A private parent config must not alter the audit or enter the report.
        fs::write(
            first.0.join(".dbt-quality.yml"),
            "disabled_rules: [SSC-EWI-DBTPRJ0001]\n",
        )
        .unwrap();
        snapshot.copy_to(&root_one).unwrap();
        snapshot.copy_to(&root_two).unwrap();
        let report_one = sample_payload(&snapshot, &root_one, &product).unwrap();
        let report_two = sample_payload(&snapshot, &root_two, &product).unwrap();
        assert!(
            report_one == report_two,
            "Sample payload differs across scratch roots"
        );
        assert_eq!(report_one["summary"]["project_count"], 4);
        let models = report_one["html"]["models"].as_object().unwrap();
        assert_eq!(report_one["html"]["included"]["files"], models.len());
        let referenced: std::collections::BTreeSet<&str> = report_one["html"]["finding_files"]
            .as_array()
            .unwrap()
            .iter()
            .flat_map(|files| files.as_array().into_iter().flatten())
            .filter_map(|file| file["id"].as_str())
            .collect();
        assert!(models.keys().all(|id| referenced.contains(id.as_str())), "Only files named by findings are embedded");
        for model in report_one["html"]["models"].as_object().unwrap().values() {
            let path = model["file"].as_str().unwrap();
            assert!([".sql", ".py", ".yml", ".yaml", ".sh"].iter().any(|ext| path.ends_with(ext)));
            assert!(!path.contains("profiles"));
            let file = snapshot
                .files
                .iter()
                .find(|file| file.path == path)
                .unwrap();
            assert_eq!(
                model["source"]["sha256"],
                format!("{:x}", Sha256::digest(&file.bytes))
            );
            let source = &model["source"];
            let mut original = Vec::new();
            if source["bom"] == true {
                original.extend_from_slice(b"\xef\xbb\xbf");
            }
            original.extend_from_slice(source["text"].as_str().unwrap().as_bytes());
            assert!(
                original == file.bytes,
                "Model snapshot must retain original bytes: {path}"
            );
        }
        let rendered_one = html::render(&report_one);
        let rendered_two = html::render(&report_two);
        assert!(
            rendered_one == rendered_two,
            "Rendered sample differs across scratch roots"
        );
        assert!(rendered_one.contains("Synthetic test data"));
        for root in [&first.0, &second.0] {
            assert!(!rendered_one.contains(root.to_str().unwrap()));
        }
        assert!(rendered_one.contains(&fixture_root(&product)), "Sample must record full paths");
        for value in snapshot.sensitive_values().unwrap() {
            assert!(
                !rendered_one.contains(&value),
                "Sensitive fixture literal must not enter HTML"
            );
        }
    }
}
