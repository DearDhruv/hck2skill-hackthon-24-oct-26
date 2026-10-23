---
trigger: always_on
description: "Mock-first architecture rule. Mandates offline seed data fixtures and dynamic live/mock toggle to guarantee 100% bug-free hackathon demonstrations."
---

# Rule: Mock-First Data Engine & Resilience (`INV-MOCK-01`)

This rule mandates a **Mock-First Architecture** to ensure hackathon presentations never crash or fail due to network outages, slow hotel Wi-Fi, rate-limited APIs, or third-party server errors.

## 1. Why Mock-First is Non-Negotiable in Hackathons
During live hackathon judging:
- Venue Wi-Fi is notorious for failing or blocking arbitrary outbound ports.
- Cloud APIs (OpenAI, HuggingFace, Supabase, Firebase) can hit rate limits or require expensive token setup.
- If an API call hangs or returns a 500 error, judges immediately deduct marks for "Incomplete Execution".

## 2. Implementation Pattern

Every repository interface MUST have a corresponding `MockEngineFixture`:

```kotlin
class MockTaskRepository : TaskRepository {
    private val _items = MutableStateFlow(SeedData.defaultTasks)

    override fun observeTasks(): Flow<List<TaskItem>> = _items.asStateFlow()

    override suspend fun addTask(title: String, category: String): TaskItem {
        delay(400) // Simulate realistic micro-latency
        val newItem = TaskItem(
            id = "mock_${Clock.System.now().toEpochMilliseconds()}",
            title = title,
            category = category,
            createdAt = Clock.System.now()
        )
        _items.update { listOf(newItem) + it }
        return newItem
    }
}
```

## 3. Dynamic Engine Delegation

The unified repository implementation delegates based on a configuration flag:

```kotlin
class UnifiedTaskRepository(
    private val mockEngine: MockTaskRepository,
    private val remoteEngine: RemoteTaskRepository,
    private val isMockMode: Boolean = true // Default to true for zero-flake demo!
) : TaskRepository {
    override fun observeTasks(): Flow<List<TaskItem>> =
        if (isMockMode) mockEngine.observeTasks() else remoteEngine.observeTasks()
}
```

## 4. Realistic Seed Fixtures
- Never use boring `Item 1`, `Item 2` placeholders.
- Seed data MUST look like a real, populated production database with relevant industry terminology, diverse tags, realistic timestamps, avatars, and metrics matching the hackathon problem statement.
