import json
import hashlib
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PluginPackageTests(unittest.TestCase):
    def test_published_evidence_preserves_frozen_bytes(self):
        for directory in (ROOT/"evals/results").iterdir():
            if not directory.is_dir():
                continue
            manifest = json.loads((directory/"manifest.json").read_text())
            for name, expected in manifest.items():
                self.assertEqual(hashlib.sha256((directory/name).read_bytes()).hexdigest(), expected)
            plan = json.loads((directory/"plan.json").read_text())
            for name, expected in plan["frozen_hashes"].items():
                target = "rubric.json" if name == "rubric.private.json" else name
                self.assertEqual(hashlib.sha256((directory/target).read_bytes()).hexdigest(), expected)

    def test_default_discovery_and_hook_contract(self):
        manifest = json.loads((ROOT/".claude-plugin/plugin.json").read_text())
        marketplace = json.loads((ROOT/".claude-plugin/marketplace.json").read_text())
        self.assertEqual(manifest["name"], marketplace["plugins"][0]["name"])
        self.assertEqual(marketplace["plugins"][0]["source"], "./")
        self.assertNotIn("hooks", manifest)
        hook = json.loads((ROOT/"hooks/hooks.json").read_text())["hooks"]["PreToolUse"][0]["hooks"][0]
        self.assertEqual(hook["failureMode"], "block")
        self.assertIn("CLAUDE_PLUGIN_ROOT", hook["command"])
        self.assertTrue((ROOT/"skills/research-rigor/SKILL.md").is_file())

    def test_reviewer_can_only_read(self):
        frontmatter = (ROOT/"agents/research-reviewer.md").read_text().split("---")[1]
        tools = next(line.split(":", 1)[1].strip() for line in frontmatter.splitlines() if line.startswith("tools:"))
        self.assertEqual({v.strip() for v in tools.split(",")}, {"Read", "Glob", "Grep"})

    def test_progressive_disclosure_reference_budget(self):
        for name, maximum in (("reviewer-red-team-and-resubmission.md", 9000), ("paper-review-submission.md", 8000)):
            self.assertLess(len((ROOT/"skills/research-rigor/references"/name).read_text(encoding="utf-8")), maximum)

    def test_compressed_instructions_reference_real_record_files(self):
        skill = ROOT/"skills/research-rigor"
        for name in ("reviewer-red-team-and-resubmission.md", "paper-review-submission.md"):
            text = (skill/"references"/name).read_text(encoding="utf-8")
            for record in re.findall(r"`(\d{2}_[A-Z_]+\.csv)`", text):
                self.assertTrue((skill/"assets/project-scaffold"/record).is_file(), record)
