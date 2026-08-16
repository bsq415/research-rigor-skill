from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "install.py"


class InstallationTests(unittest.TestCase):
    def run_command(
        self, arguments: list[str], *, environment: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, *arguments],
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=False,
            env=environment,
        )
        if result.returncode != 0:
            self.fail(
                f"command failed with exit {result.returncode}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    def test_codex_and_claude_code_installations_are_executable(self) -> None:
        with tempfile.TemporaryDirectory(prefix="research-skill-install-") as raw:
            root = Path(raw)
            codex_home = root / "codex-home"
            environment = dict(os.environ)
            environment["CODEX_HOME"] = str(codex_home)
            self.run_command(
                [str(INSTALLER), "--host", "codex", "--scope", "user"],
                environment=environment,
            )
            codex_skill = codex_home / "skills" / "research-rigor"

            claude_project = root / "claude-project"
            claude_project.mkdir()
            self.run_command(
                [
                    str(INSTALLER),
                    "--host",
                    "claude-code",
                    "--scope",
                    "project",
                    "--project-dir",
                    str(claude_project),
                ]
            )
            claude_skill = (
                claude_project / ".claude" / "skills" / "research-rigor"
            )

            for installed_skill in (codex_skill, claude_skill):
                self.assertTrue((installed_skill / "SKILL.md").is_file())
                self.assertTrue(
                    (installed_skill / "scripts" / "research_cycle.py").is_file()
                )
                self.assertTrue(
                    (installed_skill / "scripts" / "audit_revision_package.py").is_file()
                )
                synthetic_project = root / f"project-{installed_skill.parent.parent.name}"
                self.run_command(
                    [
                        str(installed_skill / "scripts" / "init_research_project.py"),
                        str(synthetic_project),
                        "--mode",
                        "full-cycle",
                        "--deep-read-min",
                        "0",
                        "--forensic-neighbor-min",
                        "0",
                        "--independent-audit-fraction",
                        "0",
                    ]
                )
                self.run_command(
                    [
                        str(installed_skill / "scripts" / "audit_research_state.py"),
                        str(synthetic_project),
                    ]
                )
                self.run_command(
                    [
                        str(
                            installed_skill
                            / "scripts"
                            / "audit_revision_package.py"
                        ),
                        str(synthetic_project),
                    ]
                )


if __name__ == "__main__":
    unittest.main()
