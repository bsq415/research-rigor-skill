# Platform compatibility

Rigorous Research Assistant keeps one canonical skill at `skills/research-rigor/`.

## Codex

- Install the directory at `$CODEX_HOME/skills/research-rigor/`.
- If `CODEX_HOME` is unset, the installer uses `~/.codex/skills/research-rigor/`.
- Invoke explicitly with `$research-rigor`.
- `agents/openai.yaml` provides Codex-facing display metadata.

## Claude Code

- User installation: `~/.claude/skills/research-rigor/SKILL.md`.
- Project installation: `<project>/.claude/skills/research-rigor/SKILL.md`.
- Invoke explicitly with `/research-rigor`.
- Claude Code can also load the skill automatically from its description.
- `${CLAUDE_SKILL_DIR}` resolves to the directory containing `SKILL.md`.
- Claude Code ignores the Codex-specific `agents/openai.yaml`; the shared instructions, references, scripts, and assets remain usable.

Claude Code documents these personal and project skill locations in its official [skills guide](https://code.claude.com/docs/en/skills).

## Shared-format decisions

- Frontmatter uses only the portable `name` and `description` fields.
- Host-specific tool allowlists, forced subagent context, hooks, and dynamic shell injection are not required.
- All bundled resource links are relative to `SKILL.md`.
- Script instructions define `<SKILL_DIR>` rather than assuming the research project contains the skill's scripts.
- The canonical skill is copied at install time; there are no platform-specific forks to keep in sync.

## Compatibility test

A release is compatible only if all of the following pass:

1. `SKILL.md` frontmatter validates and the directory name matches `research-rigor`.
2. Every linked reference, script, and scaffold file exists.
3. A clean install reaches the expected Codex and Claude Code target directories.
4. The installed skill can initialize a disposable project scaffold.
5. The state audit accepts the untouched scaffold.
6. The release privacy scan passes.
7. No instructions imply autonomous scientific authority or bypass a human-only gate.
