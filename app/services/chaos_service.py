import threading
import time
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List


class FaultType(str, Enum):
    INTERNAL_ERROR_500 = "500_INTERNAL_ERROR"
    NETWORK_TIMEOUT = "NETWORK_TIMEOUT"
    RATE_LIMIT_429 = "RATE_LIMIT_429"
    CORRUPTED_PAYLOAD = "CORRUPTED_PAYLOAD"
    JURISDICTION_UNRESOLVED = "JURISDICTION_UNRESOLVED"
    CORRUPTED_IMAGE_UPLOAD = "CORRUPTED_IMAGE_UPLOAD"


FAULT_METADATA: Dict[FaultType, Dict[str, Any]] = {
    FaultType.INTERNAL_ERROR_500: {
        "name": "500 Municipal Database Crash",
        "category": "Server & Municipal Database Crash",
        "description": "Simulates complete municipal database connection pool exhaustion and critical 500 error.",
        "subsystem": "amc_database_pool",
        "http_code": 500,
        "suggested_recovery": "Verify municipal database connection pool health or reset active mock state."
    },
    FaultType.NETWORK_TIMEOUT: {
        "name": "Network Timeout (>5s)",
        "category": "Gateway Latency / Packet Loss",
        "description": "Simulates lagging municipal gateway hanging >5.0s, triggering gateway timeout.",
        "subsystem": "amc_gateway_proxy",
        "http_code": 504,
        "suggested_recovery": "Check upstream network connectivity and AMC GIS proxy status."
    },
    FaultType.RATE_LIMIT_429: {
        "name": "429 Rate Limit Exceeded",
        "category": "API Quota Throttling",
        "description": "Simulates AMC central server returning HTTP 429: Max 10 requests/minute per ward sector.",
        "subsystem": "amc_api_ratelimiter",
        "http_code": 429,
        "suggested_recovery": "Apply exponential backoff or disable chaos mode to restore unlimited quota."
    },
    FaultType.CORRUPTED_PAYLOAD: {
        "name": "Corrupted Response Payload",
        "category": "Data Serialization / Wire Corruption",
        "description": "Simulates malformed non-JSON binary byte sequence from legacy AMC server.",
        "subsystem": "amc_legacy_serializer",
        "http_code": 200,
        "suggested_recovery": "Sanitize API payload schema and reject non-JSON byte responses."
    },
    FaultType.JURISDICTION_UNRESOLVED: {
        "name": "Jurisdiction Unresolved (Ward Dispute)",
        "category": "Municipal Boundary Dispute",
        "description": "Simulates GIS border conflict where location coordinates fall in disputed buffer zone between W12 and W27.",
        "subsystem": "amc_gis_boundary_resolver",
        "http_code": 422,
        "suggested_recovery": "Dispatch manual field surveyor or request citizen landmark clarification."
    },
    FaultType.CORRUPTED_IMAGE_UPLOAD: {
        "name": "Corrupted Image Upload Buffer",
        "category": "Vision Input Stream Failure",
        "description": "Simulates unreadable or truncated image buffer with corrupt JPEG magic header.",
        "subsystem": "vision_preprocessor",
        "http_code": 400,
        "suggested_recovery": "Prompt citizen to re-take photo with clear daylight and steady framing."
    },
}


class ChaosException(Exception):
    """Base exception for all injected chaos faults."""
    fault_type: str = "GENERIC_CHAOS"
    http_status: int = 500
    subsystem: str = "amc_municipal_core"

    def __init__(self, message: str, subsystem: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        if subsystem:
            self.subsystem = subsystem
        self.details = details or {}


class MunicipalDatabaseCrashError(ChaosException):
    fault_type = FaultType.INTERNAL_ERROR_500.value
    http_status = 500
    subsystem = "amc_database_pool"


class NetworkTimeoutError(ChaosException):
    fault_type = FaultType.NETWORK_TIMEOUT.value
    http_status = 504
    subsystem = "amc_gateway_proxy"


class RateLimitExceededError(ChaosException):
    fault_type = FaultType.RATE_LIMIT_429.value
    http_status = 429
    subsystem = "amc_api_ratelimiter"


class CorruptedPayloadError(ChaosException):
    fault_type = FaultType.CORRUPTED_PAYLOAD.value
    http_status = 200
    subsystem = "amc_legacy_serializer"


class JurisdictionUnresolvedError(ChaosException):
    fault_type = FaultType.JURISDICTION_UNRESOLVED.value
    http_status = 422
    subsystem = "amc_gis_boundary_resolver"


class CorruptedImageBufferError(ChaosException):
    fault_type = FaultType.CORRUPTED_IMAGE_UPLOAD.value
    http_status = 400
    subsystem = "vision_preprocessor"


class ChaosService:
    """
    Fault Injection & Chaos Testing Engine for NagrikAMC.
    Simulates real-world municipal infrastructure failures (crashes, timeouts,
    throttling, boundary conflicts, corrupted packets) for robust judge demos (INV-MOCK-01).
    """
    _instance: Optional["ChaosService"] = None
    _lock = threading.RLock()

    def __init__(self):
        self.enabled: bool = False
        self.active_fault: FaultType = FaultType.INTERNAL_ERROR_500
        self.timeout_seconds: float = 5.2
        self.fault_counter: int = 0
        self.last_triggered_at: Optional[str] = None
        self.last_fault_details: Optional[Dict[str, Any]] = None

    @classmethod
    def get_instance(cls) -> "ChaosService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def set_fault(self, fault: str) -> FaultType:
        with self._lock:
            for f in FaultType:
                if f.value.upper() == fault.upper() or f.name.upper() == fault.upper():
                    self.active_fault = f
                    return f
            raise ValueError(f"Unknown fault type: '{fault}'. Valid options: {[f.value for f in FaultType]}")

    def toggle(
        self,
        enabled: Optional[bool] = None,
        fault_type: Optional[str] = None,
        timeout_seconds: Optional[float] = None
    ) -> Dict[str, Any]:
        with self._lock:
            if enabled is not None:
                self.enabled = bool(enabled)
            elif fault_type is None and timeout_seconds is None:
                self.enabled = not self.enabled

            if fault_type:
                self.set_fault(fault_type)

            if timeout_seconds is not None:
                self.timeout_seconds = max(0.01, float(timeout_seconds))

            return self.get_status()

    def enable(self, fault_type: Optional[str] = None, timeout_seconds: Optional[float] = None) -> Dict[str, Any]:
        return self.toggle(enabled=True, fault_type=fault_type, timeout_seconds=timeout_seconds)

    def disable(self) -> Dict[str, Any]:
        return self.toggle(enabled=False)

    def record_fault(self, fault_type: FaultType, details: Optional[Dict[str, Any]] = None):
        with self._lock:
            self.fault_counter += 1
            self.last_triggered_at = datetime.now().isoformat(timespec="seconds")
            self.last_fault_details = details or {}

    def simulate_timeout(self, seconds: Optional[float] = None):
        dur = seconds if seconds is not None else self.timeout_seconds
        time.sleep(dur)

    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            meta = FAULT_METADATA.get(self.active_fault, {})
            return {
                "enabled": self.enabled,
                "activeFault": self.active_fault.value,
                "faultName": meta.get("name", self.active_fault.value),
                "category": meta.get("category", "General"),
                "description": meta.get("description", ""),
                "subsystem": meta.get("subsystem", ""),
                "httpCode": meta.get("http_code", 500),
                "suggestedRecovery": meta.get("suggested_recovery", ""),
                "timeoutSeconds": self.timeout_seconds,
                "faultCounter": self.fault_counter,
                "lastTriggeredAt": self.last_triggered_at,
                "availableFaults": [
                    {
                        "id": f.value,
                        "name": FAULT_METADATA[f]["name"],
                        "category": FAULT_METADATA[f]["category"],
                        "description": FAULT_METADATA[f]["description"],
                        "httpCode": FAULT_METADATA[f]["http_code"],
                        "suggestedRecovery": FAULT_METADATA[f]["suggested_recovery"]
                    }
                    for f in FaultType
                ]
            }

    def check_and_raise(self, subsystem: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        """
        If chaos mode is enabled, raises the appropriate ChaosException with metadata.
        """
        if not self.enabled:
            return

        with self._lock:
            fault = self.active_fault
            sub = subsystem or FAULT_METADATA[fault]["subsystem"]
            details = {"subsystem": sub, "fault": fault.value, "context": context or {}}
            self.record_fault(fault, details)

            if fault == FaultType.INTERNAL_ERROR_500:
                raise MunicipalDatabaseCrashError(
                    "[CHAOS FAULT: 500_INTERNAL_ERROR] Simulated AMC Municipal Database Crash: "
                    "Connection pool deadlock. Host postgresql-master-w12.amc.gov.in unreachable.",
                    subsystem=sub,
                    details=details
                )

            elif fault == FaultType.NETWORK_TIMEOUT:
                self.simulate_timeout()
                raise NetworkTimeoutError(
                    f"[CHAOS FAULT: NETWORK_TIMEOUT] Municipal Gateway Timeout: "
                    f"AMC core ingress failed to reply within {self.timeout_seconds}s (simulated network hang).",
                    subsystem=sub,
                    details=details
                )

            elif fault == FaultType.RATE_LIMIT_429:
                raise RateLimitExceededError(
                    "[CHAOS FAULT: RATE_LIMIT_429] AMC Municipal API Rate Limit Exceeded: "
                    "HTTP 429 Too Many Requests (Threshold: 10 requests/min per ward sector). Retry after 60s.",
                    subsystem=sub,
                    details=details
                )

            elif fault == FaultType.CORRUPTED_PAYLOAD:
                raise CorruptedPayloadError(
                    "[CHAOS FAULT: CORRUPTED_PAYLOAD] Corrupted legacy AMC municipal packet: "
                    "Byte sequence contains malformed non-JSON data stream.",
                    subsystem=sub,
                    details=details
                )

            elif fault == FaultType.JURISDICTION_UNRESOLVED:
                raise JurisdictionUnresolvedError(
                    "[CHAOS FAULT: JURISDICTION_UNRESOLVED] Municipal GIS Boundary Discrepancy: "
                    "Location falls into disputed buffer zone between Ward W12 (Navrangpura) and Ward W27 (Maninagar). Ward unassigned.",
                    subsystem=sub,
                    details=details
                )

            elif fault == FaultType.CORRUPTED_IMAGE_UPLOAD:
                raise CorruptedImageBufferError(
                    "[CHAOS FAULT: CORRUPTED_IMAGE_UPLOAD] Corrupted Image Upload: "
                    "JPEG SOI marker (0xFFD8) missing or truncated citizen photo buffer.",
                    subsystem=sub,
                    details=details
                )
