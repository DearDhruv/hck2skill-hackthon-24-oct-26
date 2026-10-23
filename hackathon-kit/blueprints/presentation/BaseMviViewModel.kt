package com.deardhruv.hackathon.presentation

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.CoroutineExceptionHandler
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.receiveAsFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

/**
 * Marker interface for all MVI UI states. State must be immutable data class.
 */
interface UiState

/**
 * Marker interface for all user intentions / actions.
 */
interface UiIntent

/**
 * Marker interface for one-off single-shot UI effects (e.g. Navigation, Snackbars, Dialogs).
 */
interface UiEffect

/**
 * Canonical MVI ViewModel base class for Clean Architecture in Compose Multiplatform.
 * Enforces Unidirectional Data Flow (UDF), thread-safe state mutation, and edge-case crash shielding.
 */
abstract class BaseMviViewModel<S : UiState, I : UiIntent, E : UiEffect>(
    initialState: S
) : ViewModel() {

    private val _uiState = MutableStateFlow(initialState)
    val uiState: StateFlow<S> = _uiState.asStateFlow()

    private val _uiEffect = Channel<E>(Channel.BUFFERED)
    val uiEffect = _uiEffect.receiveAsFlow()

    /**
     * Default coroutine exception handler preventing unhandled exceptions from crashing the app process.
     * Preserves structured cancellation by ignoring CancellationException.
     */
    protected val exceptionHandler = CoroutineExceptionHandler { _, throwable ->
        if (throwable is CancellationException) return@CoroutineExceptionHandler
        onUnhandledError(throwable)
    }

    /** Current immutable state snapshot */
    protected val currentState: S
        get() = _uiState.value

    /**
     * Entry point for all user interactions.
     */
    fun sendIntent(intent: I) {
        viewModelScope.launch(exceptionHandler) {
            handleIntent(intent)
        }
    }

    /**
     * Subclasses implement business logic handling for each incoming intent.
     */
    protected abstract suspend fun handleIntent(intent: I)

    /**
     * Safely executes an asynchronous coroutine block with automatic error handling.
     * Preserves structured concurrency cancellation while catching runtime failures.
     */
    protected fun safeLaunch(
        onError: ((Throwable) -> Unit)? = null,
        block: suspend CoroutineScope.() -> Unit
    ): Job {
        val customHandler = CoroutineExceptionHandler { _, throwable ->
            if (throwable is CancellationException) return@CoroutineExceptionHandler
            onError?.invoke(throwable) ?: onUnhandledError(throwable)
        }
        return viewModelScope.launch(customHandler) {
            try {
                block()
            } catch (ce: CancellationException) {
                // Always rethrow CancellationException to maintain coroutine structured cancellation
                throw ce
            } catch (t: Throwable) {
                onError?.invoke(t) ?: onUnhandledError(t)
            }
        }
    }

    /**
     * Safely executes an asynchronous operation with automatic loading indicator toggle and error capture.
     */
    protected fun safeLaunchWithLoading(
        setLoading: (Boolean) -> Unit,
        onError: ((Throwable) -> Unit)? = null,
        block: suspend CoroutineScope.() -> Unit
    ): Job {
        setLoading(true)
        return safeLaunch(
            onError = { throwable ->
                setLoading(false)
                onError?.invoke(throwable) ?: onUnhandledError(throwable)
            }
        ) {
            try {
                block()
            } finally {
                setLoading(false)
            }
        }
    }

    /**
     * Fallback handler for unhandled errors. Can be overridden to emit an Error UiEffect or update UiState.
     */
    protected open fun onUnhandledError(throwable: Throwable) {
        // Log or handle gracefully in subclass
    }

    /**
     * Atomically updates the current UI state.
     */
    protected fun updateState(reducer: (S) -> S) {
        _uiState.update(reducer)
    }

    /**
     * Idiomatic alias for updateState to match Compose conventions.
     */
    protected fun setState(reducer: (S) -> S) = updateState(reducer)

    /**
     * Emits a single-shot effect to the UI (e.g. show snackbar, navigate).
     */
    protected fun sendEffect(effect: E) {
        viewModelScope.launch(exceptionHandler) {
            _uiEffect.send(effect)
        }
    }
}
