"""The AI-first migrator's own issue framework.

Log what was found, classify it against an inventory of issue TYPES, reuse a matching
type or mint a new one. Ids are content-addressed so concurrent finders converge; the
inventory is append-only so an emitted artifact's citation stays readable; every mint
records why no existing type matched; and every text is checked against a rule that
refuses claims about what the source platform does.

This is a DIFFERENT AXIS from provenance. `SSC-AI-AUTHORED` and the MODEL provenance
class answer "who produced this". An issue answers "what went wrong". A model-authored
model with no issues and an engine-rendered model with three are both possible, and
collapsing the two axes would lose that.
"""

from .signature import (CATEGORIES, SIG_VERSION, PlatformInSignature, canonical,
                        normalise, signature_id)
from .textrule import TEXT_RULE_VERSION, lint

__all__ = ["CATEGORIES", "SIG_VERSION", "TEXT_RULE_VERSION", "PlatformInSignature",
           "canonical", "normalise", "signature_id", "lint"]
