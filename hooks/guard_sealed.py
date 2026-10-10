#!/usr/bin/env python3
"""Claude PreToolUse guard for explicitly registered sealed result roots."""
import json
import os
from pathlib import Path
import sys

READ_TOOLS = {"Read", "Glob", "Grep", "WebFetch", "WebSearch", "ListMcpResourcesTool", "ReadMcpResourceTool"}
FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit", "Delete", "Move"}


def decision(payload):
    cwd = Path(payload.get("cwd") or Path.cwd()).resolve()
    candidates = [Path(os.environ["CLAUDE_PROJECT_DIR"]).resolve()] if os.environ.get("CLAUDE_PROJECT_DIR") else []
    candidates += [cwd, *cwd.parents]
    project = next((p for p in candidates if (p/".research"/"seals.json").exists()), None)
    if project is None: return None
    registry = project / ".research" / "seals.json"
    tool = payload.get("tool_name", "")
    if tool in READ_TOOLS: return None
    try:
        data = json.loads(registry.read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or not isinstance(data.get("seals"), list):
            raise ValueError("invalid seal registry")
        protected = [registry.resolve(), (project / ".claude").resolve(), Path(__file__).resolve().parent.parent]
        for seal in data["seals"]:
            for field in ("root", "manifest"):
                raw = Path(seal[field])
                target = (project / raw).resolve()
                if raw.is_absolute() or ".." in raw.parts or not target.is_relative_to(project):
                    raise ValueError("seal registry path escapes workspace")
                if not target.exists(): raise ValueError("registered seal artifact is missing")
                protected.append(target)
        if not data["seals"]: return None
        if tool not in FILE_TOOLS:
            return "Active result seals: shell and unknown tool calls are blocked because arbitrary commands cannot be proven non-mutating. Use read tools or a new mutable workspace."
        arguments = payload.get("tool_input", {})
        paths = [arguments[k] for k in ("file_path", "notebook_path", "path", "source", "destination") if arguments.get(k)]
        for edit in arguments.get("edits", []):
            if isinstance(edit, dict) and edit.get("file_path"): paths.append(edit["file_path"])
        if not paths: return "Cannot resolve mutating tool targets while result seals are active."
        for raw in paths:
            target = (cwd / raw).resolve()
            if any(target == p or target.is_relative_to(p) or p.is_relative_to(target) for p in protected):
                return "Attempt to modify a sealed result, its manifest, guard or seal configuration. Preserve the snapshot and create a versioned successor."
        return None
    except (ValueError, KeyError, TypeError, OSError) as exc:
        return f"Result seal registry cannot be validated ({type(exc).__name__}); mutating tool call blocked."


def main():
    try:
        payload = json.load(sys.stdin)
        reason = decision(payload)
    except Exception:
        reason = "Malformed hook input; refusing an unvalidated tool call."
    if reason:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
