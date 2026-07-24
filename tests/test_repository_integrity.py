from __future__ import annotations

import re
from pathlib import Path
import unittest
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "research-rigor"
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


class RepositoryIntegrityTests(unittest.TestCase):
    def test_local_markdown_links_exist(self) -> None:
        missing: list[str] = []
        for document in REPO_ROOT.rglob("*.md"):
            if ".git" in document.parts:
                continue
            text = document.read_text(encoding="utf-8")
            for raw_target in MARKDOWN_LINK.findall(text):
                target = raw_target.strip().strip("<>")
                if (
                    not target
                    or target.startswith("#")
                    or "://" in target
                    or target.startswith("mailto:")
                ):
                    continue
                relative = unquote(target.split("#", 1)[0])
                if not (document.parent / relative).resolve().exists():
                    missing.append(
                        f"{document.relative_to(REPO_ROOT).as_posix()} -> {target}"
                    )
        self.assertEqual(missing, [], "\n".join(missing))

    def test_skill_frontmatter_and_entrypoint_are_portable(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        frontmatter = skill.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name:\s*research-rigor\s*$")
        self.assertRegex(frontmatter, r"(?m)^description:\s*\S")
        windows_user_prefix = "C:" + "\\Users\\"
        self.assertNotIn(windows_user_prefix, skill)
        self.assertLessEqual(len(skill.splitlines()), 500)

    def test_public_text_has_no_absolute_user_path_or_secret_marker(self) -> None:
        findings: list[str] = []
        forbidden = (
            re.compile(r"(?i)[A-Z]:\\Users\\"),
            re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        )
        for path in REPO_ROOT.rglob("*"):
            if (
                not path.is_file()
                or ".git" in path.parts
                or "__pycache__" in path.parts
                or path.suffix.lower()
                not in {".md", ".py", ".json", ".csv", ".yaml", ".yml", ".txt"}
            ):
                continue
            text = path.read_text(encoding="utf-8")
            if any(pattern.search(text) for pattern in forbidden):
                findings.append(path.relative_to(REPO_ROOT).as_posix())
        self.assertEqual(findings, [], "\n".join(findings))

    def test_full_cycle_runtime_is_bundled(self) -> None:
        expected = (
            "00_AUTONOMY_CONTRACT.md",
            "01_IDEA_CANDIDATES.csv",
            "04_EXPERIMENT_MATRIX.csv",
            "04_PROTOCOL_AMENDMENTS.csv",
            "07_MANUSCRIPT_AUDIT.csv",
            "RESEARCH_CYCLE_LOG.csv",
        )
        scaffold = SKILL_ROOT / "assets" / "project-scaffold"
        self.assertTrue((SKILL_ROOT / "scripts" / "research_cycle.py").is_file())
        self.assertTrue((SKILL_ROOT / "references" / "full-cycle-execution.md").is_file())
        for name in expected:
            self.assertTrue((scaffold / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
