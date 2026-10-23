#!/usr/bin/env bash
# ==============================================================================
# Script: bootstrap-new-hackathon-repo.sh
# Purpose: Instantly injects the multi-agent system, rules, blueprints, and
#          documentation into a new or existing hackathon project repository.
# Usage: ./bootstrap-new-hackathon-repo.sh /path/to/target-project [--init-gradle]
# ==============================================================================

set -euo pipefail

TARGET_DIR="${1:-}"
INIT_GRADLE=false

if [[ "${2:-}" == "--init-gradle" ]] || [[ "${TARGET_DIR:-}" == "--init-gradle" ]]; then
    INIT_GRADLE=true
    if [[ "$TARGET_DIR" == "--init-gradle" ]]; then
        TARGET_DIR="${2:-}"
    fi
fi

if [[ -z "$TARGET_DIR" ]]; then
    echo "❌ Error: Target project directory must be provided."
    echo "Usage: $0 /path/to/target-project [--init-gradle]"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🚀 Bootstrapping Hackathon Kit into: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

# Enable dotglob to ensure all hidden files in subdirectories are included
shopt -s dotglob

# 1. Copy Agent Configurations, Commands & Personas
echo "📦 Injecting Agent Rules, Commands & Personas..."
mkdir -p "$TARGET_DIR/.agents"
cp -R "$KIT_ROOT/.agents/"* "$TARGET_DIR/.agents/"
cp "$KIT_ROOT/AGENTS.md" "$TARGET_DIR/AGENTS.md"
cp "$KIT_ROOT/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"
cp "$KIT_ROOT/.cursorrules" "$TARGET_DIR/.cursorrules"

# 2. Copy Documentation Templates & Learnings Registry
echo "📄 Injecting Hack2Skill Documentation Templates & Learnings Registry..."
mkdir -p "$TARGET_DIR/Docs"
cp -R "$KIT_ROOT/Docs/"* "$TARGET_DIR/Docs/"

# 3. Copy Blueprints & Scaffolding
echo "🏗️ Injecting Architecture Blueprints..."
mkdir -p "$TARGET_DIR/blueprints"
cp -R "$KIT_ROOT/blueprints/"* "$TARGET_DIR/blueprints/"

# 4. Optional: Scaffold complete working Gradle multiplatform project
if [[ "$INIT_GRADLE" == true ]]; then
    echo "⚡ Initializing complete Gradle Multiplatform Project structure..."
    cp "$KIT_ROOT/blueprints/gradle/build.gradle.kts" "$TARGET_DIR/build.gradle.kts"
    cp "$KIT_ROOT/blueprints/gradle/settings.gradle.kts" "$TARGET_DIR/settings.gradle.kts"
    mkdir -p "$TARGET_DIR/gradle"
    cp "$KIT_ROOT/blueprints/gradle/libs.versions.toml" "$TARGET_DIR/gradle/libs.versions.toml"
    
    # Shared module
    mkdir -p "$TARGET_DIR/shared"
    cp "$KIT_ROOT/blueprints/shared/build.gradle.kts" "$TARGET_DIR/shared/build.gradle.kts"
    
    # Common source sets
    SHARED_SRC="$TARGET_DIR/shared/src/commonMain/kotlin/com/deardhruv/hackathon"
    mkdir -p "$SHARED_SRC/ui/navigation"
    mkdir -p "$SHARED_SRC/ui/components"
    mkdir -p "$SHARED_SRC/ui/theme"
    mkdir -p "$SHARED_SRC/presentation"
    mkdir -p "$SHARED_SRC/data/mock"
    mkdir -p "$SHARED_SRC/ai"

    cp "$KIT_ROOT/blueprints/compose/AdaptiveAppScaffold.kt" "$SHARED_SRC/ui/navigation/"
    cp "$KIT_ROOT/blueprints/compose/AdaptiveTwoPaneLayout.kt" "$SHARED_SRC/ui/components/"
    cp "$KIT_ROOT/blueprints/compose/EdgeCaseComponents.kt" "$SHARED_SRC/ui/components/"
    cp "$KIT_ROOT/blueprints/compose/AdaptiveLayoutTokens.kt" "$SHARED_SRC/ui/theme/"
    cp "$KIT_ROOT/blueprints/compose/SpacingTokens.kt" "$SHARED_SRC/ui/theme/"
    cp "$KIT_ROOT/blueprints/presentation/BaseMviViewModel.kt" "$SHARED_SRC/presentation/"
    cp "$KIT_ROOT/blueprints/data/MockEngineFixture.kt" "$SHARED_SRC/data/mock/"
    cp "$KIT_ROOT/blueprints/ai/LiteRTQuickEngine.kt" "$SHARED_SRC/ai/"
    echo "✅ Gradle Multiplatform project initialized with core CMP source sets & edge-case components!"
fi

# 5. Copy Scripts
mkdir -p "$TARGET_DIR/scripts"
cp "$KIT_ROOT/scripts/check-hackathon-readiness.sh" "$TARGET_DIR/scripts/"
cp "$KIT_ROOT/scripts/bootstrap-new-hackathon-repo.sh" "$TARGET_DIR/scripts/"
chmod +x "$TARGET_DIR/scripts/"*.sh

shopt -u dotglob

echo "✅ Bootstrap complete! Project is now primed for high-velocity pair-programming."
echo "💡 Next Steps:"
echo "   1. Open $TARGET_DIR in your IDE."
echo "   2. Fill out Docs/problem_assessment_worksheet.md."
echo "   3. Launch your assistant and run: '/plan' or '/boost build MVP'."
