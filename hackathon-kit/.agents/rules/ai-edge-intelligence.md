---
trigger: always_on
description: "Guidelines and patterns for integrating On-Device AI (LiteRT, Gemini Prompt API) or Cloud AI services into hackathon projects."
---

# Rule: AI & Edge Intelligence Integration

When the hackathon problem statement includes an AI/ML component (intelligent recommendations, summarization, vision analysis, natural language tasks):

## 1. On-Device First Philosophy
- **Why On-Device AI Wins Hackathons**:
  - Zero latency (instant response).
  - 100% offline privacy guarantee.
  - Zero cloud API billing or token exhaustion during demo.
  - Impresses judges by running intelligence locally on the user's hardware.

## 2. Supported AI Runtimes
1. **Google AI Edge LiteRT (`.tflite` / CompiledModel)**:
   - For fast classification, regression, sentiment scoring, or embedding generation.
   - Use `LiteRTQuickEngine.kt` blueprint in `blueprints/ai/`.
2. **Gemini Nano Prompt API (`androidx.mlkit.genai:prompt`)**:
   - For on-device LLM text generation, summarization, and structured JSON output.
3. **Simulated AI Engine (Zero-Flake Fallback)**:
   - If downloading an LLM weights file takes too long on the hackathon network, implement a heuristic/rule-based parser or pre-computed embedding cache that behaves identically from a UI perspective.

## 3. Threading Invariants (`INV-THREAD-01`)
- All inference invocations MUST execute off the main thread:
  ```kotlin
  suspend fun infer(prompt: String): AiResult = withContext(Dispatchers.Default) {
      // Model forward pass or Prompt API invocation
  }
  ```
- Streaming tokens should emit via `Flow<String>` to give judges the live typing animation effect.
