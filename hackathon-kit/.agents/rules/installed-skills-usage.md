---
trigger: always_on
description: "Mandatory rule enforcing proactive discovery and execution of proper installed skills across Adaptive UI, Navigation, AI/LiteRT, Testing, Performance, and Edge-to-Edge."
---

# Rule: Installed Skills Utilization (`INV-SKILL-01`)

This rule governs how AI assistants (Antigravity, Claude Code, Cursor) must discover, consult, and execute using the proper specialized skills installed in the environment.

---

## 1. Core Principle: Skill-First Execution

Dhruv's development environment contains rich, verified skills installed under:
- `~/.gemini/config/skills/` (Antigravity & Gemini official skills)
- `~/.agents/skills/` (Comprehensive multiplatform, Kotlin, Compose, Swift, and AI skills)
- `~/.gemini/antigravity/builtin/skills/` (Antigravity built-in tools)
- `~/.gemini/config/plugins/` (Plugin-provided skills including Firebase and Android CLI)

**Mandatory Assistant Rule**:
When implementing, debugging, refactoring, or testing features, **NEVER** guess APIs, write deprecated syntax, or invent ad-hoc patterns when an installed skill covers the domain.
Assistants **MUST** consult the relevant `SKILL.md` before generating implementations.

---

## 2. Hackathon Domain Skills Matrix

| Domain / Task | Primary Installed Skills | Exact Skill Path / Location | When to Activate |
|---|---|---|---|
| **Adaptive Layout & Multi-Pane** | `adaptive` | `~/.gemini/config/skills/adaptive/` | Designing layouts across phones, foldables, tablets, desktop, TV; multi-pane scenes, `MediaQuery` APIs, window size classes. |
| **Jetpack Navigation 3** | `navigation-3` | `~/.gemini/config/skills/navigation-3/` | Multi-backstack routing, deep links, scenes (dialogs, bottom sheets, two-pane, supporting pane). |
| **Predictive Back Navigation** | `navigation-event` | `~/.gemini/config/skills/navigation-event/` | Predictive back gestures, `NavigationBackHandler`, SDK 36+ back dispatchers. |
| **System Bars & IME Insets** | `edge-to-edge` | `~/.gemini/config/skills/edge-to-edge/` | Edge-to-edge migration, status/nav bar protection, keyboard IME insets. |
| **Compose Styles & Theming** | `styles` | `~/.gemini/config/skills/styles/` | Compose Styles API, styleable design system components, unified style attributes. |
| **On-Device LLM & Text Gen** | `litert-lm` | `~/.gemini/config/skills/litert-lm/` | On-device LLM inference (Gemma, Qwen, Llama) with LiteRT-LM Kotlin API. |
| **On-Device Vision / TFLite** | `litert-runtime` | `~/.gemini/config/skills/litert-runtime/` | LiteRT CompiledModel API on CPU/GPU for vision, audio, embeddings, TensorBuffer optimization. |
| **Gemini Nano Prompt API** | `ml-kit-genai-prompt-api` | `~/.gemini/config/skills/ml-kit-genai-prompt-api/` | ML Kit GenAI Prompt API for on-device Gemini Nano, prefix caching, structured output. |
| **System AI Actions** | `appfunctions` | `~/.gemini/config/skills/appfunctions/` | Exposing on-device workflows to AI agents and voice shortcuts via AppFunctions. |
| **Testing Infrastructure** | `testing-setup` | `~/.gemini/config/skills/testing-setup/` | Setting up unit test, UI test, screenshot test, and E2E test harnesses. |
| **Verification Gate** | `verify` | `~/.gemini/config/skills/verify/` | Pre-submission diff review, targeted test runs, quality gate validation. |
| **Compose UI Performance** | `jetpack-compose-performance` | `~/.gemini/config/skills/jetpack-compose-performance/` | Diagnosing recompositions, eliminating frame drops, optimizing LazyLists. |
| **ANR & Threading Audit** | `anr-audit-and-fix` | `~/.gemini/config/skills/anr-audit-and-fix/` | Scanning for main-thread blocking, ANR risks, and coroutine stalls. |
| **Android CLI & Emulators** | `android-cli` | `~/.gemini/config/skills/android-cli/` | Creating projects, launching emulators, APK installation, UI inspection. |
| **Headless JDWP Debugging** | `debroid` | `~/.gemini/config/skills/debroid/` | Setting breakpoints, inspecting Compose runtime state, diagnosing crashes. |
| **Camera & Vision Hardware** | `camerax` | `~/.gemini/config/skills/camerax/` | CameraX integration, async recording, ML Kit vision interop. |
| **Cloud Backend & Auth** | `firebase-*` | `~/.gemini/config/plugins/firebase/skills/` | Firestore setup, Auth, Storage rules, App Hosting. |
| **KMP & Coroutines** | `kotlin-multiplatform`, `compose-multiplatform-patterns`, `kotlin-coroutines-flows` | `~/.agents/skills/` | Core KMP library design, multiplatform networking, reactive StateFlow patterns. |

---

## 3. Protocol for AI Assistants During Hackathon Sprints

1. **Step 0: Skill Identification**:
   - When an instruction touches a domain listed above, identify the matching skill.
2. **Step 1: Consult `SKILL.md`**:
   - Read the skill's instructions, code snippets, and anti-patterns before generating code.
3. **Step 2: Apply State-of-the-Art Patterns**:
   - Use the skill's recommended libraries, dependency versions, and idiomatic APIs.
4. **Step 3: Continuous Learning Cross-Pollination**:
   - If an issue or edge case arises that was solved using a skill's guidance, link the skill in `Docs/learnings/hackathon_learnings.md` via `/learn`.
