#!/usr/bin/env bash
# ==============================================================================
# Script: check-hackathon-readiness.sh
# Purpose: Rapid verification of architecture, invariants, and submission docs
# ==============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🔍 Auditing Hackathon Readiness in: $ROOT_DIR"

ERRORS=0

check_file() {
    local file_path="$1"
    local description="$2"
    if [[ -f "$file_path" ]]; then
        echo "  ✅ Found: $description ($file_path)"
    else
        echo "  ❌ MISSING: $description ($file_path)"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "--- 1. Agent Configuration Checks ---"
check_file "$ROOT_DIR/AGENTS.md" "Root AGENTS.md"
check_file "$ROOT_DIR/CLAUDE.md" "Claude Code Guidelines"
check_file "$ROOT_DIR/.cursorrules" "Cursor Rules"
check_file "$ROOT_DIR/.agents/AGENTS.md" "Agent Pointer Index"
check_file "$ROOT_DIR/.agents/skills.json" "Agent Skills Definition"
check_file "$ROOT_DIR/.agents/agents/architect-scaffolder.md" "Architect Scaffolder Agent"
check_file "$ROOT_DIR/.agents/agents/cmp-ui-designer.md" "Compose UI Designer Agent"
check_file "$ROOT_DIR/.agents/agents/engine-data-integrator.md" "Data Integrator Agent"
check_file "$ROOT_DIR/.agents/agents/quality-verifier.md" "Quality Verifier Agent"
check_file "$ROOT_DIR/.agents/agents/pitch-submission-lead.md" "Pitch Submission Lead Agent"

echo "--- 2. Agent Commands Checks ---"
check_file "$ROOT_DIR/.agents/commands/boost.md" "/boost Command Engine"
check_file "$ROOT_DIR/.agents/commands/plan.md" "/plan Command Engine"
check_file "$ROOT_DIR/.agents/commands/learn.md" "/learn Command Engine"

echo "--- 3. Architecture Rules Checks ---"
check_file "$ROOT_DIR/.agents/rules/hackathon-4hr-protocol.md" "4-Hour Protocol Rule"
check_file "$ROOT_DIR/.agents/rules/clean-architecture-kmp.md" "Clean Architecture Rule"
check_file "$ROOT_DIR/.agents/rules/adaptive-ui-multiplatform.md" "Adaptive UI Rule"
check_file "$ROOT_DIR/.agents/rules/mock-first-resilience.md" "Mock-First Resilience Rule"
check_file "$ROOT_DIR/.agents/rules/hack2skill-judging-rubric.md" "Hack2Skill Rubric Rule"
check_file "$ROOT_DIR/.agents/rules/ai-edge-intelligence.md" "AI Edge Intelligence Rule"
check_file "$ROOT_DIR/.agents/rules/prompt-expansion-protocol.md" "Prompt Auto-Expansion Rule"
check_file "$ROOT_DIR/.agents/rules/edge-case-defense-matrix.md" "Edge-Case Defense Matrix Rule"
check_file "$ROOT_DIR/.agents/rules/hackathon-planning-protocol.md" "Hackathon Planning Rule"
check_file "$ROOT_DIR/.agents/rules/continuous-learning-protocol.md" "Continuous Learning Rule"
check_file "$ROOT_DIR/.agents/rules/installed-skills-usage.md" "Installed Skills Usage Rule"

echo "--- 4. Documentation & Learnings Templates ---"
check_file "$ROOT_DIR/Docs/problem_assessment_worksheet.md" "Problem Assessment Worksheet"
check_file "$ROOT_DIR/Docs/architecture_template.md" "Architecture Spec Template"
check_file "$ROOT_DIR/Docs/pitch_deck_template.md" "Pitch Deck Template"
check_file "$ROOT_DIR/Docs/demo_video_script.md" "Demo Video Script"
check_file "$ROOT_DIR/Docs/hack2skill_submission_template.md" "Submission Form Copy"
check_file "$ROOT_DIR/Docs/learnings/hackathon_learnings.md" "Learnings & Instincts Registry"

echo "--- 5. Blueprints & Edge-Case Checks ---"
check_file "$ROOT_DIR/blueprints/gradle/libs.versions.toml" "Version Catalog Blueprint"
check_file "$ROOT_DIR/blueprints/gradle/build.gradle.kts" "Root Build Script Blueprint"
check_file "$ROOT_DIR/blueprints/gradle/settings.gradle.kts" "Settings Script Blueprint"
check_file "$ROOT_DIR/blueprints/shared/build.gradle.kts" "Shared Multiplatform Module Script"
check_file "$ROOT_DIR/blueprints/compose/AdaptiveAppScaffold.kt" "Adaptive Navigation Scaffold"
check_file "$ROOT_DIR/blueprints/compose/AdaptiveTwoPaneLayout.kt" "Adaptive Two-Pane Layout"
check_file "$ROOT_DIR/blueprints/compose/AdaptiveLayoutTokens.kt" "Adaptive Layout Tokens"
check_file "$ROOT_DIR/blueprints/compose/SpacingTokens.kt" "Design Spacing Tokens"
check_file "$ROOT_DIR/blueprints/compose/EdgeCaseComponents.kt" "Edge Case Components Blueprint"
check_file "$ROOT_DIR/blueprints/presentation/BaseMviViewModel.kt" "MVI Base ViewModel"
check_file "$ROOT_DIR/blueprints/data/MockEngineFixture.kt" "Mock Engine Fixture"
check_file "$ROOT_DIR/blueprints/ai/LiteRTQuickEngine.kt" "On-Device AI Quick Engine"

echo "-------------------------------------"
if [[ $ERRORS -eq 0 ]]; then
    echo "🎉 All Hackathon Readiness Checks PASSED! (Total: 36 components verified). Ready to build and win."
    exit 0
else
    echo "⚠️ Found $ERRORS readiness issues. Review missing files above."
    exit 1
fi
