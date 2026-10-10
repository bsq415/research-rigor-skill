# Claude Code plugin

The repository is both the canonical skill and a plugin/marketplace source.
In Claude Code:

```text
/plugin marketplace add bsq415/research-rigor-skill
/plugin install research-rigor@research-rigor-marketplace
```

For local development use `claude --plugin-dir <repository>`, then invoke
`/research-rigor:research-rigor`. The Python tools require Python 3.10+ on PATH;
SymPy is optional. Run `claude plugin validate <repository> --strict` in an
available Claude Code installation. Static package/guard tests do not substitute
for this host check; no Claude CLI was available in the development environment.

## Explicit result protection

Create and verify a dedicated result snapshot, then register it:

```text
python "<SKILL_DIR>/scripts/seal_artifacts.py" create results/v1 results/v1.manifest.json
python "<SKILL_DIR>/scripts/seal_artifacts.py" protect results/v1 results/v1.manifest.json --project <PROJECT>
```

Registration creates `.research/seals.json`. A loaded plugin's PreToolUse hook
blocks editing/writing/moving sealed roots and manifests, guard files and project
hook settings. It resolves aliases/symlinks and ancestor targets. While a seal is
active, arbitrary shell and unknown tool calls are conservatively blocked because
their side effects cannot reliably be inferred; direct edits to unsealed source
files and read tools remain available. Continue computation in a separate
versioned mutable workspace; keep the original snapshot and seal record intact.

The guard is inactive without registered seals. It is a tool-level prevention
mechanism, not OS immutability: a person, an external app, disabled hooks or a
different unregistered workspace can bypass it. Verify hashes before using a
snapshot and before release. Unsupported hook hosts/versions must not claim
protection. A failing hook command is configured to block; validate support in
the actual Claude host. The standalone Codex skill does not install Claude hooks.

## Independent review context

The bundled `research-reviewer` agent has only Read/Glob/Grep tools. Request an
independent review of the frozen manuscript and relevant evidence, without the
author's preferred conclusions or prior favorable scores. Its separate context
reduces shared-history bias but is still model review, not a human referee or
an editorial decision. It cannot edit files or send confidential reviews out.

Official references: [plugin manifest](https://code.claude.com/docs/en/plugins-reference),
[hooks](https://code.claude.com/docs/en/hooks), [subagents](https://code.claude.com/docs/en/sub-agents).
