//! Rule detectors, one module per pack. Metadata is in `rules/<PACK>.json`.

use std::sync::LazyLock;

use crate::engine::Detector;

pub mod arc;
pub mod col;
pub mod doc;
pub mod inc;
pub mod mac;
pub mod mat;
pub mod mig;
pub mod ops;
pub mod prj;
pub mod sql;
pub mod tst;

pub static DETECTORS: LazyLock<Vec<Detector>> = LazyLock::new(|| {
    [arc::DETECTORS, col::DETECTORS, doc::DETECTORS, inc::DETECTORS, mac::DETECTORS, mat::DETECTORS, mig::DETECTORS, ops::DETECTORS, prj::DETECTORS, sql::DETECTORS, tst::DETECTORS]
        .concat()
});

#[cfg(test)]
mod tests {
    use std::collections::BTreeSet;

    use super::DETECTORS;
    use crate::model::RULES;

    #[test]
    fn every_record_has_exactly_one_detector_and_back() {
        let mut seen = BTreeSet::new();
        for d in DETECTORS.iter() {
            assert!(seen.insert(d.code), "{} has more than one detector", d.code);
            let m = crate::model::meta(d.code).unwrap_or_else(|| panic!("{} has no metadata record", d.code));
            assert_eq!(m.scope, d.detect.scope(), "{}: scope in JSON disagrees with the detector", d.code);
        }
        let missing: Vec<_> = RULES.iter().filter(|r| !seen.contains(r.code)).map(|r| r.code).collect();
        assert!(missing.is_empty(), "records without a detector: {missing:?}");
    }
}
