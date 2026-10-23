package com.deardhruv.hackathon.data.mock

import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.update
import kotlinx.datetime.Clock
import kotlinx.datetime.Instant

/**
 * Universal domain item for rapid prototyping during hackathons.
 * Rename/adapt fields based on the problem statement tomorrow.
 */
data class HackathonItem(
    val id: String,
    val title: String,
    val subtitle: String,
    val category: String,
    val score: Double,
    val isHighlighted: Boolean,
    val createdAt: Instant = Clock.System.now()
)

/**
 * Repository interface representing domain contracts with built-in search, full CRUD, and offline support.
 */
interface HackathonRepository {
    fun observeItems(): Flow<List<HackathonItem>>
    fun searchItems(query: String): Flow<List<HackathonItem>>
    suspend fun getItemById(id: String): HackathonItem?
    suspend fun createItem(title: String, subtitle: String, category: String): HackathonItem
    suspend fun updateItem(id: String, title: String, subtitle: String, category: String): HackathonItem?
    suspend fun deleteItem(id: String): Boolean
    suspend fun toggleHighlight(id: String): Boolean
    fun toggleOfflineMode(): Boolean
    fun setSimulateError(enable: Boolean)
    fun resetToSeedData()
}

/**
 * Resilient, zero-network-dependency Mock Data Engine with edge-case controls.
 * Guarantees a 100% bug-free demo under conference Wi-Fi conditions with live toggleable states.
 */
class MockEngineFixture(
    private val simulateLatencyMs: Long = 200L
) : HackathonRepository {

    private var idCounter = 100

    private val _isOfflineMode = MutableStateFlow(true)
    val isOfflineMode: Flow<Boolean> = _isOfflineMode.asStateFlow()

    private val _simulateError = MutableStateFlow(false)

    private val defaultSeedItems = listOf(
        HackathonItem(
            id = "mock_1",
            title = "Smart Edge Diagnostics",
            subtitle = "Real-time anomaly detection running on-device via LiteRT micro-kernels.",
            category = "AI / Edge",
            score = 98.4,
            isHighlighted = true
        ),
        HackathonItem(
            id = "mock_2",
            title = "Decentralized Ledger Sync",
            subtitle = "Cryptographically verified audit trail with offline SQLite persistence.",
            category = "Security",
            score = 94.1,
            isHighlighted = false
        ),
        HackathonItem(
            id = "mock_3",
            title = "Adaptive Multi-Device Canvas",
            subtitle = "Fluid UI adapting across Mobile, Foldable, Desktop, and Web Wasm.",
            category = "Cross-Platform",
            score = 99.0,
            isHighlighted = true
        ),
        HackathonItem(
            id = "mock_4",
            title = "Zero-Latency Stream Buffer",
            subtitle = "Reactive flow processing with coroutine backpressure management.",
            category = "Performance",
            score = 91.5,
            isHighlighted = false
        )
    )

    private val _items = MutableStateFlow(defaultSeedItems)

    override fun observeItems(): Flow<List<HackathonItem>> = _items.asStateFlow()

    override fun searchItems(query: String): Flow<List<HackathonItem>> {
        val trimmed = query.trim()
        val tokens = trimmed.split("\\s+".toRegex()).filter { it.isNotBlank() }

        return _items.map { list ->
            if (tokens.isEmpty()) {
                list
            } else {
                list.filter { item ->
                    tokens.all { token ->
                        item.title.contains(token, ignoreCase = true) ||
                        item.subtitle.contains(token, ignoreCase = true) ||
                        item.category.contains(token, ignoreCase = true)
                    }
                }
            }
        }
    }

    override suspend fun getItemById(id: String): HackathonItem? {
        checkErrorSimulation()
        if (simulateLatencyMs > 0) delay(simulateLatencyMs / 2)
        return _items.value.find { it.id == id }
    }

    override suspend fun createItem(title: String, subtitle: String, category: String): HackathonItem {
        checkErrorSimulation()
        require(title.isNotBlank()) { "Item title cannot be blank" }

        if (simulateLatencyMs > 0) delay(simulateLatencyMs)
        val newItem = HackathonItem(
            id = "mock_${Clock.System.now().toEpochMilliseconds()}_${++idCounter}",
            title = title.trim(),
            subtitle = subtitle.trim(),
            category = category.trim().ifBlank { "General" },
            score = 95.0,
            isHighlighted = false
        )
        _items.update { listOf(newItem) + it }
        return newItem
    }

    override suspend fun updateItem(
        id: String,
        title: String,
        subtitle: String,
        category: String
    ): HackathonItem? {
        checkErrorSimulation()
        require(title.isNotBlank()) { "Item title cannot be blank" }

        if (simulateLatencyMs > 0) delay(simulateLatencyMs)
        var updatedItem: HackathonItem? = null
        _items.update { list ->
            list.map { item ->
                if (item.id == id) {
                    val updated = item.copy(
                        title = title.trim(),
                        subtitle = subtitle.trim(),
                        category = category.trim().ifBlank { item.category }
                    )
                    updatedItem = updated
                    updated
                } else {
                    item
                }
            }
        }
        return updatedItem
    }

    override suspend fun deleteItem(id: String): Boolean {
        checkErrorSimulation()
        if (simulateLatencyMs > 0) delay(simulateLatencyMs / 2)
        val initialSize = _items.value.size
        _items.update { list -> list.filterNot { it.id == id } }
        return _items.value.size < initialSize
    }

    override suspend fun toggleHighlight(id: String): Boolean {
        checkErrorSimulation()
        if (simulateLatencyMs > 0) delay(simulateLatencyMs / 2)
        var updatedState = false
        _items.update { list ->
            list.map { item ->
                if (item.id == id) {
                    updatedState = !item.isHighlighted
                    item.copy(isHighlighted = updatedState)
                } else {
                    item
                }
            }
        }
        return updatedState
    }

    override fun toggleOfflineMode(): Boolean {
        val nextState = !_isOfflineMode.value
        _isOfflineMode.value = nextState
        return nextState
    }

    override fun setSimulateError(enable: Boolean) {
        _simulateError.value = enable
    }

    override fun resetToSeedData() {
        _items.value = defaultSeedItems
        _simulateError.value = false
    }

    private fun checkErrorSimulation() {
        if (_simulateError.value) {
            throw IllegalStateException("Simulated network timeout (Testing Error State UI)")
        }
    }
}
