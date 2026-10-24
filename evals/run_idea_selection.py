#!/usr/bin/env python3
"""Compare a frozen previous skill context with updated idea-selection guidance.

Uses the established blind/scoring/export machinery without changing its audit
baseline. Only synthetic tasks and reviewed public guidance go to the model.
"""
import argparse
import importlib.util
from pathlib import Path
import shutil

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO/"skills/research-rigor/scripts/rigor_eval.py"
spec = importlib.util.spec_from_file_location("idea_eval_core", SCRIPT)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
REFS = ("SKILL.md", "references/idea-and-literature.md",
        "references/research-playbooks.md", "references/empirical-idea-discovery.md")


def prepare(directory, baseline_context, model, effort, suite_directory=None):
    baseline = baseline_context.read_bytes()
    core.ASSETS = suite_directory or REPO/"evals/idea-selection-v1"
    core.REFERENCE_FILES = REFS
    core.prepare(directory, model, effort, seed=20261025)
    (directory/"baseline-context.txt").write_bytes(baseline)
    shutil.copyfile(SCRIPT, directory/"runner-snapshot.py")
    shutil.copyfile(Path(__file__), directory/"driver-snapshot.py")
    plan = core.load_plan(directory)
    plan["design"] = "old-skill versus updated-skill, prompt-only, synthetic development tasks, paired independent sessions"
    plan["condition_meanings"] = {"baseline": "frozen previous skill context", "skill": "updated skill context"}
    for name in ("baseline-context.txt", "runner-snapshot.py", "driver-snapshot.py"):
        plan["frozen_hashes"][name] = core.digest(directory/name)
    core.write(directory/"plan.private.json", plan)
    (directory/"plan.sha256").write_text(core.digest(directory/"plan.private.json"), encoding="ascii")


def run(directory, limit=None):
    plan = core.load_plan(directory)
    tasks = {t["id"]: t for t in core.read(directory/"tasks.json")["tasks"]}
    contexts = {"baseline": (directory/"baseline-context.txt").read_text(encoding="utf-8"),
                "skill": (directory/"skill-context.txt").read_text(encoding="utf-8")}
    count = 0
    for row in plan["rows"]:
        target = directory/"responses"/(row["run_id"]+".json")
        if target.exists():
            continue
        prompt = ("Assist a researcher on this closed-book synthetic task. Do not use tools, files, web or delegation. "
                  "Use only supplied material; answer in Chinese, at most 1600 Chinese characters across the four fields. "
                  "Verdict concerns the requested scoped proposal or statement: supported, revise, or insufficient. "
                  "A provisional proposed study is not a verified novelty/result claim.\n"
                  "Apply this guidance:\n<guidance>\n"+contexts[row["condition"]]+"\n</guidance>\nTask:\n"+tasks[row["task_id"]]["prompt"])
        result = core.call_codex(prompt, plan["model"], plan["effort"], target, directory/"answer-schema.json")
        print(f"{row['run_id']} {row['task_id']}: {result['status']}", flush=True)
        count += 1
        if limit and count >= limit:
            break


def export(directory, destination):
    core.export(directory, destination)
    for name in ("baseline-context.txt", "driver-snapshot.py", "execution-settings.json"):
        if (directory/name).exists():
            shutil.copyfile(directory/name, destination/name)
    core.write(destination/"manifest.json", {p.name: core.digest(p) for p in sorted(destination.iterdir())
                                            if p.is_file() and p.name != "manifest.json"})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "run", "blind", "judge", "summarize", "export"))
    parser.add_argument("directory", type=Path)
    parser.add_argument("--baseline-context", type=Path)
    parser.add_argument("--suite-dir", type=Path, help="optional frozen result/input directory for exact task-version replay")
    parser.add_argument("--model")
    parser.add_argument("--effort", default="medium", choices=("low", "medium", "high", "xhigh", "max", "ultra"))
    parser.add_argument("--limit", type=int)
    parser.add_argument("--destination", type=Path)
    args = parser.parse_args()
    try:
        if args.action == "prepare":
            if not args.baseline_context or not args.model:
                parser.error("prepare requires --baseline-context and --model")
            prepare(args.directory, args.baseline_context, args.model, args.effort, args.suite_dir)
        elif args.action == "run":
            run(args.directory, args.limit)
        elif args.action == "export":
            if not args.destination:
                parser.error("export requires --destination")
            export(args.directory, args.destination)
        else:
            getattr(core, args.action)(args.directory)
        return 0
    except (ValueError, KeyError, OSError) as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
