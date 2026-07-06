#!/usr/bin/env python3
"""
scan_skill.py — deterministic structural inventory of a Claude Code skill.

Part of g14-skill-audit (Control 2 — Process). This script does the MECHANICAL,
non-judgement half of an audit: it reads a skill folder and emits a single JSON
object describing what is there and how it is wired. The judgement half (is a
control NEEDED? is it done WELL?) is done by the LLM auditors — never here.

Usage:
    python scan_skill.py /abs/path/to/skill-folder
    python scan_skill.py /abs/path/to/skill-folder --pretty

The skill folder is the directory that contains SKILL.md.

It NEVER writes files and NEVER edits the target. Read-only by construction.
"""
from __future__ import annotations

import json
import os
import re
import sys

# The five controls, mapped to their conventional folders.
CONTROL_FOLDERS = {
    "1_input": "references",
    "2_process": "scripts",
    "3_output": "assets",
    "4_speed": "agents",
    "5_tests": "tests",
}

# Files we never count as real skill content.
JUNK = {".DS_Store", "Thumbs.db", ".gitkeep"}


def read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except (OSError, UnicodeError):
        return ""


def split_frontmatter(text: str):
    """Return (frontmatter_dict, body) for a `---` delimited markdown file.

    Minimal YAML: only top-level `key: value` pairs are parsed (enough for
    name/description/model/tools). Returns ({}, text) if no frontmatter.
    """
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    raw, body = parts[1], parts[2]
    fm = {}
    key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m and not line.startswith((" ", "\t")):
            key = m.group(1).strip()
            fm[key] = m.group(2).strip()
        elif key is not None and line.startswith((" ", "\t")):
            # continuation of a multi-line value (e.g. a wrapped description)
            fm[key] = (fm[key] + " " + line.strip()).strip()
    for k, v in list(fm.items()):
        # YAML block scalar indicators (>, |, >-, |-, >+, |+) leak into the
        # hand-parsed value — strip them so size/content signals are accurate.
        mblock = re.match(r"^[|>][+-]?\s+(.*)$", v)
        if mblock:
            v = mblock.group(1).strip()
        elif v in ("|", ">", "|-", ">-", "|+", ">+"):
            v = ""
        # YAML inline/flow list ("- Read - Bash") -> "Read, Bash"
        if v.startswith("- "):
            items = [x.strip() for x in re.split(r"\s*-\s+", v) if x.strip()]
            v = ", ".join(items)
        # strip surrounding quotes
        if len(v) >= 2 and v[0] in "\"'" and v[-1] == v[0]:
            v = v[1:-1]
        fm[k] = v
    return fm, body


def list_files(folder: str):
    out = []
    for root, _dirs, files in os.walk(folder):
        for f in files:
            if f in JUNK:
                continue
            rel = os.path.relpath(os.path.join(root, f), folder)
            out.append(rel)
    return sorted(out)


USAGE = """\
scan_skill.py — deterministic structural inventory of a Claude Code skill.

Usage:
    python scan_skill.py <skill-folder> [--pretty]

Arguments:
    <skill-folder>   directory that contains SKILL.md (the skill to scan)

Options:
    --pretty         pretty-print the JSON output (indented)
    -h, --help       show this message and exit

Emits a single JSON object on stdout describing the skill's structure and
wiring. Read-only; never writes or edits the target.

Exit codes: 0 ok · 1 not a valid skill folder (no SKILL.md) · 2 bad usage.
"""


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(USAGE, file=sys.stderr)
        sys.exit(0)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    pretty = "--pretty" in sys.argv
    if not args:
        print(json.dumps({"error": "usage: scan_skill.py <skill-folder> [--pretty]"}))
        sys.exit(2)

    skill_dir = os.path.abspath(args[0])
    result = {
        "skill_dir": skill_dir,
        "folder_name": os.path.basename(skill_dir.rstrip("/")),
        "ok": True,
        "errors": [],
    }

    skillmd_path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skillmd_path):
        result["ok"] = False
        result["errors"].append("No SKILL.md found at skill root — not a valid skill folder.")
        print(json.dumps(result, indent=2 if pretty else None))
        sys.exit(1)

    skillmd = read_text(skillmd_path)
    fm, body = split_frontmatter(skillmd)
    # starts with --- but parse yielded nothing => unterminated/malformed, which
    # is a different (more actionable) defect than "no frontmatter at all".
    frontmatter_malformed = skillmd.startswith("---") and not fm

    # ---- SKILL.md frontmatter & size -------------------------------------
    name = fm.get("name", "")
    desc = fm.get("description", "")
    result["skillmd"] = {
        "has_frontmatter": bool(fm),
        "frontmatter_malformed": frontmatter_malformed,
        "name": name,
        "name_matches_folder": name == result["folder_name"],
        "description_present": bool(desc),
        "description_chars": len(desc),
        "description_words": len(desc.split()),
        "line_count": skillmd.count("\n") + 1,
        "char_count": len(skillmd),
        "extra_frontmatter_keys": [k for k in fm if k not in ("name", "description")],
        "uses_plugin_root": skillmd.count("${CLAUDE_PLUGIN_ROOT}"),
    }

    body_lower = skillmd.lower()

    # ---- Controls: present? wired? ---------------------------------------
    controls = {}
    for ckey, folder in CONTROL_FOLDERS.items():
        fpath = os.path.join(skill_dir, folder)
        present = os.path.isdir(fpath)
        files = list_files(fpath) if present else []
        non_empty = len(files) > 0
        # "wired" = a PATH-SHAPED reference to the folder appears in SKILL.md
        # (e.g. `references/x.md`), not just the bare prose word "references".
        # Matching the word caused orphan false-negatives.
        path_referenced = bool(re.search(r"(?<![\w/])" + re.escape(folder) + r"/", skillmd))
        # A folder that doesn't exist cannot be meaningfully "wired" — reporting
        # present:false + wired:true is a self-contradiction that misleads the
        # auditor (a skill that *teaches* about scripts/ or tests/ mentions those
        # path strings in examples). Only call it wired when it actually exists;
        # a referenced-but-absent path is caught separately as broken wiring.
        wired = path_referenced and present
        controls[ckey] = {
            "control": ckey,
            "folder": folder,
            "present": present,
            "non_empty": non_empty,
            "file_count": len(files),
            "files": files,
            "wired_in_skillmd": wired,
            "orphan": present and non_empty and not wired,  # exists but never referenced
        }
    result["controls"] = controls

    # ---- Agents: model & tool declarations -------------------------------
    agents = []
    agents_dir = os.path.join(skill_dir, "agents")
    if os.path.isdir(agents_dir):
        for rel in list_files(agents_dir):
            if not rel.endswith(".md"):
                continue
            atext = read_text(os.path.join(agents_dir, rel))
            afm, _ = split_frontmatter(atext)
            agents.append({
                "file": rel,
                "name": afm.get("name", ""),
                "model_declared": "model" in afm,
                "model": afm.get("model", ""),
                "effort_declared": "effort" in afm,
                "effort": afm.get("effort", ""),
                "tools_declared": "tools" in afm,
                "tools": afm.get("tools", ""),
                "description_present": bool(afm.get("description", "")),
            })
    result["agents"] = agents

    # ---- Wiring integrity: referenced paths that don't exist -------------
    # Two kinds of in-repo references can appear in SKILL.md:
    #   (a) plugin-root refs:  ${CLAUDE_PLUGIN_ROOT}/skills/<name>/<rel>
    #       — these may point at THIS skill or a SIBLING skill; resolve against
    #         the plugin root (two levels up from the skill folder).
    #   (b) bare refs:         references/x.md, scripts/y.py, assets/z, tests/r
    #       — resolve against THIS skill folder.
    # We resolve (a) first and remove them so their tails aren't double-counted
    # as bare refs against the wrong skill (that was a false-positive bug).
    plugin_root = os.path.dirname(os.path.dirname(skill_dir))  # …/skills/<x> -> …(plugin)

    def is_globby(p: str) -> bool:
        return p.endswith("/") or any(c in p for c in "*<{}")

    referenced = []
    broken = []
    seen_root_refs = []

    # (a) plugin-root references
    for m in re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/[A-Za-z0-9_./-]+", skillmd):
        clean = m.rstrip(".,)`*'\"")
        seen_root_refs.append(clean)
        referenced.append(clean)
        rel = clean[len("${CLAUDE_PLUGIN_ROOT}/"):]
        if is_globby(rel):
            continue
        if not os.path.exists(os.path.join(plugin_root, rel)):
            broken.append(clean)

    # remove plugin-root refs from the text before scanning bare refs
    stripped = skillmd
    for r in seen_root_refs:
        stripped = stripped.replace(r, " ")

    # (b) bare references — left boundary stops matching inside longer words
    # like "frontend/scripts/build.py" or "myassets/logo.png".
    for ref in re.findall(r"(?<![\w/])(?:references|scripts|assets|agents|tests)/[A-Za-z0-9_./-]+", stripped):
        clean = ref.rstrip(".,)`*'\"")
        if is_globby(clean):
            continue
        referenced.append(clean)
        if not os.path.exists(os.path.join(skill_dir, clean)):
            broken.append(clean)

    result["referenced_paths"] = sorted(set(referenced))
    result["broken_referenced_paths"] = sorted(set(broken))

    # hardcoded absolute user paths in SKILL.md are a portability red flag
    result["hardcoded_abs_paths"] = sorted(set(
        p.rstrip(".,)`*'\"") for p in re.findall(r"/Users/[A-Za-z0-9_./-]+", skillmd)
    ))

    # ---- Signal flags the LLM auditors use as hints ----------------------
    result["signals"] = {
        "mentions_parallel": any(w in body_lower for w in ("in parallel", "at the same time", "simultaneously", "fan out", "fan-out")),
        "mentions_subagent": any(w in body_lower for w in ("subagent", "sub-agent", "dispatch", "general-purpose")),
        "mentions_grader_or_fresh_context": any(w in body_lower for w in ("fresh context", "fresh-context", "grader", "llm-as-judge", "quality gate")),
        "mentions_model_choice": bool(re.search(r"model:\s*(haiku|sonnet|opus|fable)", body_lower)),
        "mentions_haiku": "haiku" in body_lower,
        "mentions_escape_hatch": any(w in body_lower for w in ("escape hatch", "if it fails", "if a script fails", "improvise", "fall back", "fallback", "if unreachable", "record it as skipped", "report the failure")),
        "mentions_preflight_check": any(w in body_lower for w in ("preflight", "pre-flight", "before starting", "before you begin", "first, verify", "verify access", "verify you have", "check access", "check that you have", "confirm access", "required tools", "prerequisite", "prerequisites", "dependencies are available", "fail fast", "fail-fast", "abort early")),
        "writes_scripts_on_the_fly": any(w in body_lower for w in ("write a script", "create a script", "generate a script", "write a python script", "write a bash script", "create a python", "author a script")),
        "mentions_dynamic_workflow": any(w in body_lower for w in ("dynamic workflow", "workflow tool", "workflow(", "pipeline(", "fan out hundreds", "fan-out hundreds")),
        "mentions_large_fanout": any(w in body_lower for w in ("one per page", "one per item", "one per url", "one per record", "hundreds of", "thousands of", "whole site", "entire site", "every page", "all pages", "crawl")),
        # work that repeats per unit and is a candidate to extract into a parallel
        # worker agent rather than describe inline in SKILL.md.
        "mentions_per_item_work": any(w in body_lower for w in ("for each", "per source", "per page", "per item", "per record", "per file", "per url", "per query", "each source", "each page", "each url", "each file", "scrape", "fetch each", "one per", "for every")),
        "mentions_state_checkpoint": any(w in body_lower for w in ("state.json", "checkpoint", "intermediate state", "resume from", "pick up from", "progress file", "save progress", "write state", "persist state", "store state")),
        # count numbered steps as headings ("### Step 3"), bold ("**Step 3**")
        # or ordered-list items ("3. Step ...") so prose-numbered skills aren't
        # read as having zero steps.
        "step_count": len(set(re.findall(r"(?:#+\s*|\*\*\s*|^\s*\d+\.\s*)step\s*(\d+)", body_lower, re.MULTILINE))),
        "mentions_error_handling": any(w in body_lower for w in ("retry", "retries", "try again", "up to 3", "fallback", "fall back", "if this fails", "if it fails", "on error", "on failure", "stop the skill", "abort", "halt", "do not continue", "stop and report", "if you cannot", "if access is denied")),
        "mentions_retry": any(w in body_lower for w in ("retry", "retries", "try again", "up to 3", "attempt again", "re-attempt")),
        "mentions_stop_step": any(w in body_lower for w in ("stop the skill", "abort", "halt", "do not continue", "stop and report", "stop here", "exit early")),
        "mentions_only_these_sources": any(w in body_lower for w in ("use only these", "only these sources", "do not fall back", "do not add a source")),
        # --- speed / quality / cost economics (curriculum: lessons 06, 12, 10, 03) ---
        "mentions_effort": bool(re.search(r"effort:\s*(low|medium|high|xhigh|max)", body_lower)) or "effort" in body_lower,
        "mentions_batching": any(w in body_lower for w in ("batch", "batches", "per worker", "per subagent", "per agent", "group items", "chunk")),
        "mentions_return_only_result": any(w in body_lower for w in ("return only", "only the result", "only the final", "do not summarise", "do not include reasoning", "no transcript", "clean result")),
        "mentions_context_slice": any(w in body_lower for w in ("relevant slice", "only the relevant", "narrow", "do not pass the whole", "don't fan the whole", "scoped prompt")),
        "mentions_opus": "opus" in body_lower,
        "mentions_compact": any(w in body_lower for w in ("/compact", "compact the context", "context window", "context grows")),
        "mentions_memory_reuse": any(w in body_lower for w in ("claude.md", "auto-memory", "memory file", "cache derived", "avoid re-deriving", "do not re-derive")),
        "mentions_loop_or_routine": any(w in body_lower for w in ("/loop", "/routine", "scheduled", "cron", "every iteration", "high-frequency", "high frequency", "runs repeatedly", "per run cost", "per-run cost")),
        "mentions_cost_awareness": any(w in body_lower for w in ("cost per", "per-iteration cost", "token budget", "daily cost", "cost driver", "stay under budget")),
        "has_what_section": bool(re.search(r"#+\s*what this does", body_lower)),
        "has_when_section": bool(re.search(r"#+\s*when to use", body_lower)),
        "has_steps": bool(re.search(r"#+\s*step\s*\d", body_lower)),
    }

    # ---- Quick derived summary for the orchestrator ----------------------
    present_controls = [c for c, v in controls.items() if v["present"] and v["non_empty"]]
    result["summary"] = {
        "controls_present": present_controls,
        "controls_absent": [c for c in CONTROL_FOLDERS if c not in present_controls],
        "orphan_controls": [c for c, v in controls.items() if v["orphan"]],
        "agents_missing_model": [a["file"] for a in agents if not a["model_declared"]],
        "agents_missing_effort": [a["file"] for a in agents if not a["effort_declared"]],
        "agents_missing_tools": [a["file"] for a in agents if not a["tools_declared"]],
        "agent_count": len(agents),
        "broken_wiring_count": len(result["broken_referenced_paths"]),
        "hardcoded_abs_path_count": len(result["hardcoded_abs_paths"]),
    }
    # Hint (role-agnostic): the skill describes independent / repeated / fan-out
    # work but shows no sign of parallel subagent dispatch. A candidate for a
    # missing subagent that would parallelise the work. The LLM auditor confirms
    # by reading whether that work is already delegated.
    has_parallelisable_work = (result["signals"]["mentions_per_item_work"]
                               or result["signals"]["mentions_large_fanout"])
    result["summary"]["likely_missing_subagent_opportunity"] = bool(
        has_parallelisable_work and not result["signals"]["mentions_parallel"])

    print(json.dumps(result, indent=2 if pretty else None))


if __name__ == "__main__":
    main()
