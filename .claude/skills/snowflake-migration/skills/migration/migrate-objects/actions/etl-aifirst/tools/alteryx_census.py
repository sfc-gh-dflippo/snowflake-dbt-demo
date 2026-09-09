"""One-shot corpus census over poc/inputs/alteryx-public.

NOT part of the framework or the platform table -- a throwaway measurement
script whose OUTPUT (a plugin-frequency table) is what platform_alteryx.json
is designed against. Deliberately does not import identify.py/docmodel.py:
this has to work even if the platform table doesn't exist yet, and its job
is to describe the corpus, not to run the framework over it.

Walks every real .yxmd and .yxmc (never __MACOSX/* -- verified 1:1 resource-
fork duplicates of the real files, see the extraction log) and additionally
opens every .yxzp (an Alteryx PACKAGE, itself a zip containing a .yxmd/.yxmc
plus any macros it depends on under _externals/) to reach workflows that
exist ONLY inside a package.

Three separate counts, because they answer three different questions:
  WORKFLOW_PLUGIN  -- every <Node> found while walking .yxmd files (loose or
                       inside a .yxzp). This is "what does a workflow call".
  MACRO_INTERNAL_PLUGIN -- every <Node> found while walking .yxmc files. This
                       is "what does a macro's own internal graph call" --
                       a different population (MacroInput/MacroOutput appear
                       here and nowhere in a .yxmd) and answering the
                       coordinator's "does the table handle macros" question
                       needs both counted, not blended into one number.
  MACRO_REFERENCES -- every <Node> in a .yxmd whose GuiSettings has NO
                       Plugin attribute, tallied by its EngineSettings/@Macro
                       filename (or "(no @Macro attribute)" if that is also
                       absent). This is "how often does a real workflow hand
                       off to a macro, and to how many distinct ones".
"""
import collections
import xml.etree.ElementTree as ET
import zipfile
import sys
from pathlib import Path

import os

def resolve_root(argv: list[str] | None = None) -> Path:
    """Corpus is not shipped. Pass root as argv[1] or set AIFIRST_ALTERYX_CORPUS."""
    argv = argv if argv is not None else sys.argv
    if len(argv) > 1:
        return Path(argv[1])
    env = os.environ.get("AIFIRST_ALTERYX_CORPUS")
    if env:
        return Path(env)
    raise SystemExit(
        "usage: python3 alteryx_census.py <alteryx-public-corpus-root>\n"
        "or set AIFIRST_ALTERYX_CORPUS"
    )

ROOT = None  # set in __main__


def iter_nodes_from_bytes(data: bytes):
    root = ET.fromstring(data)
    return root.iter("Node")


def tally_workflow(nodes_iter, plugin_counter, macro_ref_counter, parse_errors, src):
    for node in nodes_iter:
        gui = node.find("GuiSettings")
        plugin = gui.get("Plugin") if gui is not None else None
        if plugin:
            plugin_counter[plugin] += 1
        else:
            eng = node.find("EngineSettings")
            macro = eng.get("Macro") if eng is not None else None
            macro_ref_counter[macro or "(no @Macro attribute)"] += 1


def main():
    global ROOT
    ROOT = resolve_root()
    workflow_plugin = collections.Counter()
    macro_internal_plugin = collections.Counter()
    macro_refs = collections.Counter()
    parse_errors = []

    loose_yxmd = sorted(ROOT.rglob("*.yxmd"))
    loose_yxmc = sorted(ROOT.rglob("*.yxmc"))
    yxzp = sorted(ROOT.rglob("*.yxzp"))

    n_workflows = 0
    n_macro_defs = 0

    for p in loose_yxmd:
        try:
            tally_workflow(iter_nodes_from_bytes(p.read_bytes()),
                            workflow_plugin, macro_refs, parse_errors, str(p))
            n_workflows += 1
        except ET.ParseError as e:
            parse_errors.append((str(p), str(e)))

    for p in loose_yxmc:
        try:
            tally_workflow(iter_nodes_from_bytes(p.read_bytes()),
                            macro_internal_plugin, collections.Counter(),
                            parse_errors, str(p))
            n_macro_defs += 1
        except ET.ParseError as e:
            parse_errors.append((str(p), str(e)))

    zp_yxmd_count = 0
    zp_yxmc_count = 0
    for zp in yxzp:
        try:
            with zipfile.ZipFile(zp) as zf:
                for name in zf.namelist():
                    if name.startswith("__MACOSX/"):
                        continue
                    lname = name.lower()
                    if lname.endswith(".yxmd"):
                        try:
                            data = zf.read(name)
                            tally_workflow(iter_nodes_from_bytes(data),
                                           workflow_plugin, macro_refs,
                                           parse_errors, f"{zp}!{name}")
                            zp_yxmd_count += 1
                        except ET.ParseError as e:
                            parse_errors.append((f"{zp}!{name}", str(e)))
                    elif lname.endswith(".yxmc"):
                        try:
                            data = zf.read(name)
                            tally_workflow(iter_nodes_from_bytes(data),
                                           macro_internal_plugin,
                                           collections.Counter(),
                                           parse_errors, f"{zp}!{name}")
                            zp_yxmc_count += 1
                        except ET.ParseError as e:
                            parse_errors.append((f"{zp}!{name}", str(e)))
        except zipfile.BadZipFile as e:
            parse_errors.append((str(zp), f"BadZipFile: {e}"))

    print(f"loose .yxmd files parsed : {n_workflows}")
    print(f"loose .yxmc files parsed : {n_macro_defs}")
    print(f".yxzp packages found     : {len(yxzp)}")
    print(f".yxmd found inside .yxzp : {zp_yxmd_count}")
    print(f".yxmc found inside .yxzp : {zp_yxmc_count}")
    print(f"TOTAL workflows censused : {n_workflows + zp_yxmd_count}")
    print(f"TOTAL macro defs censused: {n_macro_defs + zp_yxmc_count}")
    print(f"parse errors             : {len(parse_errors)}")
    for path, err in parse_errors[:20]:
        print(f"    PARSE ERROR: {path}: {err}")
    print()
    print(f"total <Node> elements across all workflows: {sum(workflow_plugin.values()) + sum(macro_refs.values())}")
    print()
    print("=== WORKFLOW_PLUGIN: distinct GuiSettings/@Plugin values across all .yxmd (workflows), by frequency ===")
    for plugin, n in workflow_plugin.most_common():
        print(f"{n:6d}  {plugin}")
    print()
    print(f"distinct plugin values (workflows): {len(workflow_plugin)}")
    print(f"total tool invocations (workflows, built-in tools only): {sum(workflow_plugin.values())}")
    print()
    print("=== MACRO_REFERENCES: <Node> elements in .yxmd with NO GuiSettings/@Plugin, by EngineSettings/@Macro ===")
    for macro, n in macro_refs.most_common():
        print(f"{n:6d}  {macro}")
    print(f"total macro-invoking Node elements: {sum(macro_refs.values())}")
    print(f"distinct macro filenames referenced: {len([k for k in macro_refs if k != '(no @Macro attribute)'])}")
    print()
    print("=== MACRO_INTERNAL_PLUGIN: distinct GuiSettings/@Plugin values across all .yxmc (macro definitions' own internals) ===")
    for plugin, n in macro_internal_plugin.most_common(40):
        print(f"{n:6d}  {plugin}")
    print(f"... ({len(macro_internal_plugin)} distinct plugin values total inside .yxmc files)")


if __name__ == "__main__":
    main()
