# Rule: Continuous Learning Protocol & /learn Engine (`INV-LEARN-01`)

This rule governs how the multi-agent system records runtime observations, debugging insights, platform anomalies (such as Kotlin/Wasm or Compose quirks), and user feedback into atomic instincts stored in `Docs/learnings/hackathon_learnings.md`.

---

## 1. Why Continuous Learning is Critical
In 4-hour hackathons, there is zero time to make the same mistake twice:
- If a specific Compose Multiplatform component has a rendering bug on Web (Wasm), the system logs it once and avoids it for the rest of the sprint.
- If an API or library is prone to Gradle sync failures, the system records the working configuration or bypass.
- If Dhruv expresses a specific styling or architectural preference, it becomes an active invariant immediately.

---

## 2. The Learning Lifecycle

```
[Issue / Insight Observed] ──► [/learn Command]
                                      │
                                      ▼
                        [Atomic Instinct Formulation]
                        - Trigger condition
                        - Trap / failure mode
                        - Canonical defensive solution
                                      │
                                      ▼
                        [Append to hackathon_learnings.md]
                                      │
                                      ▼
                        [Active Memory for /boost & /plan]
```

---

## 3. Instinct Template Format

Each entry added via `/learn` must follow this structure:

```markdown
### [INSTINCT-XXX] [Short Title]
- **Date / Sprint Phase**: [e.g. Hour 2 / Compose UI]
- **Trigger**: [When building X or configuring Y]
- **The Trap**: [What fails or causes lag / compilation errors]
- **The Defensive Pattern**: [Concrete code snippet or rule to apply]
- **Agents Impacted**: [e.g. cmp-ui-designer, engine-data-integrator]
```

---

## 4. Autonomous Triggers for /learn

The system automatically suggests or executes `/learn` when:
1. A compilation error requires more than 1 fix attempt.
2. A Wasm-specific or Desktop-specific rendering bug is identified.
3. An edge case was missed and caught during quality auditing.
4. Dhruv provides feedback on layout, spacing, or architecture.

---

## 5. Active Instinct Integration into /boost and /plan

During prompt auto-expansion (`/boost` / PEP) and roadmap planning (`/plan`), assistants MUST consult the active instincts in [Docs/learnings/hackathon_learnings.md](../Docs/learnings/hackathon_learnings.md):
- **INSTINCT-001**: Always use `Dispatchers.Default` for shared CPU tasks; avoid `Dispatchers.IO` on Wasm.
- **INSTINCT-002**: Always clamp ultrawide displays with `AdaptiveContainer(1200.dp)`.
- **INSTINCT-003**: Always guard action buttons with `debouncedClickable()`.
- **INSTINCT-004**: Always provide `DemoModeBanner` with an offline mock toggle.
- **INSTINCT-005**: Always wrap mobile forms in `AdaptiveFormLayout` for `imePadding()`.
- **INSTINCT-006**: Always preserve `CancellationException` in coroutine exception handling.
- **INSTINCT-007**: Always use monotonic counters for mock ID generation to avoid LazyColumn key collisions.
- **INSTINCT-008**: Always preserve ripple indication in `debouncedClickable`.
- **INSTINCT-009**: Always provide `resetToSeedData()` for clean stage demo resets.
- **INSTINCT-010**: Always dual-shield on-device AI with `withTimeoutOrNull` and `runCatching`.
