---
trigger: always_on
description: "Continuous technical documentation and codebase structure synchronization protocol. Enforces updating READMEs and technical docs with direct file links upon task completion."
---

# Rule: Continuous Documentation & Structure Synchronization (`INV-DOCS-SYNC-01`)

This rule governs how AI assistants (Antigravity, Claude Code, Cursor) must maintain living, synchronized technical documentation whenever code changes, features are implemented, or architecture evolves.

---

## 1. Core Invariant (`INV-DOCS-SYNC-01`)

**Documentation and code MUST never drift apart.**
Whenever any task, feature implementation, refactoring, or blueprint addition is completed:
1. **Update Technical Information**:
   - Record newly added libraries, Gradle plugins, version catalog entries, or API integrations.
   - Document any architectural decisions, state management flows (MVI), and edge-case defenses introduced.
2. **Synchronize File Structure**:
   - Update the ASCII directory tree in `README.md` and [Docs/architecture_template.md](../../Docs/architecture_template.md) to reflect newly created directories, files, and modules.
3. **Link to Relevant Files & Symbols**:
   - Every newly implemented component, screen, ViewModel, engine, or script MUST be linked using relative Markdown links (e.g. `[MyFeatureScreen.kt](hackathon-kit/blueprints/compose/...)`).
   - Use concise, readable link anchors.
4. **Zero Broken Links**:
   - Never use machine-absolute paths (`/Users/...`).
   - Ensure all relative paths resolve accurately from the document's location.

---

## 2. Post-Task Completion Checklist

Before declaring any feature or sprint task complete, the active agent MUST execute this synchronization cycle:

```
Task Execution ──► Code Verification ──► [Docs & Structure Sync] ──► Task Done
                                                │
                                                ├── 1. Update README.md technical specs
                                                ├── 2. Update directory tree in README.md
                                                ├── 3. Add relative links to new code files
                                                └── 4. Update Docs/learnings if bug/trap resolved
```

### Required Updates:
- [README.md](../../../README.md) (Workspace root): Update component overview, technical specs, and file index.
- [hackathon-kit/README.md](../../README.md): Update blueprint catalogue and architecture details.
- [Docs/architecture_template.md](../../Docs/architecture_template.md): Update layer mapping and Mermaid diagrams if data flow changed.
- [Docs/learnings/hackathon_learnings.md](../../Docs/learnings/hackathon_learnings.md): Add newly learned instincts if tricky bugs or platform quirks were resolved.

---

## 3. Formatting Standards for File Links

- Always link files with relative paths:
  - From workspace root: `[AdaptiveAppScaffold.kt](hackathon-kit/blueprints/compose/AdaptiveAppScaffold.kt)`
  - From subfolders: `[SpacingTokens.kt](../compose/SpacingTokens.kt)`
- If referencing key code symbols (classes, functions, interfaces), specify the symbol:
  - `[`AdaptiveTwoPaneLayout`](hackathon-kit/blueprints/compose/AdaptiveTwoPaneLayout.kt)`
  - `[`BaseMviViewModel`](hackathon-kit/blueprints/presentation/BaseMviViewModel.kt)`
  - `[`MockEngineFixture`](hackathon-kit/blueprints/data/MockEngineFixture.kt)`
