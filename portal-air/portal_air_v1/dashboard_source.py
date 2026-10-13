"""Read-only reader for a configured PM dashboard contract.

A future public consumer must never receive the configured source address or
call the upstream source directly. This sanitized reference contains no
production origin, IP address, station identifier, or deployment topology.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from http.client import HTTPException, HTTPResponse
from ipaddress import ip_address, ip_network
import json
from math import isfinite
import re
import socket
import ssl
from threading import Lock
from time import monotonic
from typing import Any, Callable, Mapping


DASHBOARD_SOURCE_SCHEMA = "portal-air-v1-dashboard-source/v1"
RAW_DASHBOARD_SCHEMA = "portal-air-visualization/v1"
AGGREGATE_DASHBOARD_SCHEMA = "portal-air-visualization-long-window/v1"
PERIODS = frozenset({"24h", "7d", "30d"})
_UTC_RFC3339_Z = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?Z$",
    re.ASCII,
)
_HOSTNAME = re.compile(
    r"(?=.{1,253}\Z)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}\Z",
    re.ASCII,
)
_GAP_KIND = re.compile(r"^[a-z_]{1,32}$", re.ASCII)
_DOCUMENTATION_NETWORKS = (
    ip_network("192.0.2.0/24"),
    ip_network("198.51.100.0/24"),
    ip_network("203.0.113.0/24"),
)
_RAW_FIELDS = ("timestamp", "PM2.5", "PM10", "temperature", "humidity", "pressure")
_CHANNEL_FIELDS = ("PM2.5", "PM10", "temperature", "humidity", "pressure")
_AGGREGATE_GAP_STATES = {
    "observed",
    "observed_with_missing_events",
    "missing_events",
    "no_observations",
}


class DashboardSourceFailure(RuntimeError):
    """Stable, non-secret source classification for the application boundary."""

    def __init__(self, code: str, public_status: str) -> None:
        super().__init__(code)
        self.code = code
        self.public_status = public_status


@dataclass(frozen=True)
class DashboardSourceConfig:
    """Non-secret private configuration for one reviewed dashboard origin."""

    origin_hostname: str
    connect_address: str
    timeout_seconds: float
    max_response_bytes: int
    cache_seconds: int

    def __post_init__(self) -> None:
        if not isinstance(self.origin_hostname, str) or _HOSTNAME.fullmatch(self.origin_hostname) is None:
            raise ValueError("dashboard source hostname is invalid")
        if self.origin_hostname.lower() != self.origin_hostname:
            raise ValueError("dashboard source hostname must be lowercase")
        if not isinstance(self.connect_address, str):
            raise ValueError("dashboard source address is invalid")
        try:
            address = ip_address(self.connect_address)
        except ValueError as exc:
            raise ValueError("dashboard source address is invalid") from exc
        if not address.is_global and not any(address in network for network in _DOCUMENTATION_NETWORKS):
            raise ValueError("dashboard source address must be global or a documentation address")
        if (
            isinstance(self.timeout_seconds, bool)
            or not isinstance(self.timeout_seconds, (int, float))
            or not isfinite(float(self.timeout_seconds))
            or not 1 <= float(self.timeout_seconds) <= 30
        ):
            raise ValueError("dashboard source timeout is invalid")
        if (
            isinstance(self.max_response_bytes, bool)
            or not isinstance(self.max_response_bytes, int)
            or not 16_384 <= self.max_response_bytes <= 4_000_000
        ):
            raise ValueError("dashboard source response limit is invalid")
        if (
            isinstance(self.cache_seconds, bool)
            or not isinstance(self.cache_seconds, int)
            or not 0 <= self.cache_seconds <= 300
        ):
            raise ValueError("dashboard source cache duration is invalid")

    @classmethod
    def from_document(cls, document: object) -> "DashboardSourceConfig":
        if not isinstance(document, Mapping) or document.get("schema_version") != DASHBOARD_SOURCE_SCHEMA:
            raise ValueError("dashboard source configuration is invalid")
        expected = {
            "schema_version",
            "origin_hostname",
            "connect_address",
            "timeout_seconds",
            "max_response_bytes",
            "cache_seconds",
        }
        if set(document) != expected:
            raise ValueError("dashboard source configuration has unknown fields")
        return cls(
            origin_hostname=document.get("origin_hostname"),  # type: ignore[arg-type]
            connect_address=document.get("connect_address"),  # type: ignore[arg-type]
            timeout_seconds=document.get("timeout_seconds"),  # type: ignore[arg-type]
            max_response_bytes=document.get("max_response_bytes"),  # type: ignore[arg-type]
            cache_seconds=document.get("cache_seconds"),  # type: ignore[arg-type]
        )


@dataclass(frozen=True)
class PMHistory:
    """Safe PM series before a future public projection serializes it."""

    period: str
    representation: str
    source_snapshot_at_utc: str
    series: tuple[dict[str, Any], ...]
    gaps: tuple[dict[str, str], ...]


@dataclass(frozen=True)
class _CacheEntry:
    expires_at: float
    value: PMHistory


def _utc(value: object, field: str) -> tuple[str, datetime]:
    if not isinstance(value, str) or _UTC_RFC3339_Z.fullmatch(value) is None:
        raise ValueError(f"{field} must be an RFC 3339 UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError(f"{field} must be an RFC 3339 UTC timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
        raise ValueError(f"{field} must be an RFC 3339 UTC timestamp")
    parsed = parsed.astimezone(timezone.utc)
    return parsed.isoformat().replace("+00:00", "Z"), parsed


def _number(value: object, field: str, *, minimum: float | None = None, maximum: float | None = None) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(float(value)):
        raise ValueError(f"{field} must be a finite number or null")
    number = float(value)
    if minimum is not None and number < minimum:
        raise ValueError(f"{field} is below its allowed range")
    if maximum is not None and number > maximum:
        raise ValueError(f"{field} is above its allowed range")
    return number


def _require_mapping(value: object, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return value


def _measurement_projection(values: Mapping[str, Any], *, prefix: str) -> dict[str, float | None]:
    for field in _RAW_FIELDS:
        if field not in values:
            raise ValueError(f"{prefix} is missing {field}")
    return {
        "pm25_ug_m3": _number(values["PM2.5"], f"{prefix}.PM2.5", minimum=0),
        "pm10_ug_m3": _number(values["PM10"], f"{prefix}.PM10", minimum=0),
        "temperature_c": _number(values["temperature"], f"{prefix}.temperature"),
        "humidity_percent": _number(values["humidity"], f"{prefix}.humidity", minimum=0, maximum=100),
        "pressure_hpa": _number(values["pressure"], f"{prefix}.pressure", minimum=0),
    }


def _gap(from_utc: str, to_utc: str) -> dict[str, str]:
    return {"from_utc": from_utc, "to_utc": to_utc, "kind": "MISSING_RECEIPTS"}


def _deduplicated_gaps(gaps: list[dict[str, str]]) -> tuple[dict[str, str], ...]:
    result: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for gap in sorted(gaps, key=lambda value: (value["from_utc"], value["to_utc"])):
        key = (gap["from_utc"], gap["to_utc"])
        if key not in seen:
            result.append(gap)
            seen.add(key)
    return tuple(result)


@dataclass
class DashboardPMSource:
    """Read the existing PM dashboard only over pinned, hostname-verified TLS."""

    config: DashboardSourceConfig
    socket_factory: Callable[..., socket.socket] = socket.create_connection
    ssl_context_factory: Callable[[], ssl.SSLContext] = ssl.create_default_context
    _cache: dict[str, _CacheEntry] = field(default_factory=dict, init=False, repr=False)
    _cache_lock: Lock = field(default_factory=Lock, init=False, repr=False)

    def _request_document(self, period: str) -> Mapping[str, Any]:
        request_path = f"/api/dashboard/v1/?period={period}"
        context = self.ssl_context_factory()
        raw_socket: socket.socket | None = None
        tls_socket: ssl.SSLSocket | None = None
        try:
            raw_socket = self.socket_factory(
                (self.config.connect_address, 443), timeout=float(self.config.timeout_seconds)
            )
            raw_socket.settimeout(float(self.config.timeout_seconds))
            tls_socket = context.wrap_socket(raw_socket, server_hostname=self.config.origin_hostname)
            tls_socket.settimeout(float(self.config.timeout_seconds))
            request_bytes = (
                f"GET {request_path} HTTP/1.1\r\n"
                f"Host: {self.config.origin_hostname}\r\n"
                "Accept: application/json\r\n"
                "Cache-Control: no-store\r\n"
                "Connection: close\r\n"
                "\r\n"
            ).encode("ascii")
            tls_socket.sendall(request_bytes)
            response = HTTPResponse(tls_socket)
            response.begin()
            if response.status != 200:
                if 500 <= response.status <= 599:
                    raise DashboardSourceFailure("DASHBOARD_HTTP_5XX", "SOURCE_UNAVAILABLE")
                raise DashboardSourceFailure("DASHBOARD_HTTP_FAILURE", "SOURCE_UNAVAILABLE")
            content_type = response.getheader("Content-Type", "")
            if content_type.split(";", 1)[0].strip().lower() != "application/json":
                raise DashboardSourceFailure("DASHBOARD_CONTENT_TYPE", "MALFORMED_SOURCE_DATA")
            content_length = response.getheader("Content-Length")
            if content_length is not None:
                try:
                    declared = int(content_length)
                except ValueError as exc:
                    raise DashboardSourceFailure("DASHBOARD_CONTENT_LENGTH", "MALFORMED_SOURCE_DATA") from exc
                if declared < 0 or declared > self.config.max_response_bytes:
                    raise DashboardSourceFailure("DASHBOARD_RESPONSE_TOO_LARGE", "MALFORMED_SOURCE_DATA")
            body = response.read(self.config.max_response_bytes + 1)
            if len(body) > self.config.max_response_bytes:
                raise DashboardSourceFailure("DASHBOARD_RESPONSE_TOO_LARGE", "MALFORMED_SOURCE_DATA")
        except DashboardSourceFailure:
            raise
        except ssl.SSLError as exc:
            raise DashboardSourceFailure("DASHBOARD_TLS_FAILURE", "SOURCE_UNAVAILABLE") from exc
        except (HTTPException, TimeoutError, socket.timeout) as exc:
            raise DashboardSourceFailure("DASHBOARD_TIMEOUT", "SOURCE_UNAVAILABLE") from exc
        except OSError as exc:
            raise DashboardSourceFailure("DASHBOARD_NETWORK_FAILURE", "SOURCE_UNAVAILABLE") from exc
        finally:
            if tls_socket is not None:
                tls_socket.close()
            elif raw_socket is not None:
                raw_socket.close()
        try:
            document = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise DashboardSourceFailure("DASHBOARD_JSON_FAILURE", "MALFORMED_SOURCE_DATA") from exc
        if not isinstance(document, Mapping):
            raise DashboardSourceFailure("DASHBOARD_SCHEMA_FAILURE", "MALFORMED_SOURCE_DATA")
        return document

    @staticmethod
    def _source_snapshot(document: Mapping[str, Any]) -> str:
        try:
            return _utc(document.get("generated_at_utc"), "dashboard.generated_at_utc")[0]
        except ValueError:
            # The production dashboard contract has historically used this
            # field. Treat its absence or malformed value as source-contract
            # drift rather than replacing it with local time.
            raise DashboardSourceFailure("DASHBOARD_SCHEMA_FAILURE", "MALFORMED_SOURCE_DATA") from None

    @staticmethod
    def _source_window(document: Mapping[str, Any], period: str) -> tuple[datetime, datetime]:
        try:
            window = _require_mapping(document.get("window"), "dashboard.window")
            if window.get("name") != period:
                raise ValueError("dashboard window period is invalid")
            _, start = _utc(window.get("start_utc"), "dashboard.window.start_utc")
            _, end = _utc(window.get("end_utc"), "dashboard.window.end_utc")
            if end < start:
                raise ValueError("dashboard window interval is invalid")
            return start, end
        except (KeyError, TypeError, ValueError):
            raise DashboardSourceFailure("DASHBOARD_SCHEMA_FAILURE", "MALFORMED_SOURCE_DATA") from None

    @staticmethod
    def _require_source_identity(document: Mapping[str, Any]) -> None:
        """Require a typed opaque source identity without retaining its value."""
        try:
            source = _require_mapping(document.get("station"), "dashboard.station")
            identity = _require_mapping(source.get("identity"), "dashboard.station.identity")
            value = identity.get("id")
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError("dashboard source identity is invalid")
        except (KeyError, TypeError, ValueError):
            raise DashboardSourceFailure("DASHBOARD_SOURCE_IDENTITY_INVALID", "MALFORMED_SOURCE_DATA") from None

    @staticmethod
    def _raw_history(document: Mapping[str, Any], period: str) -> PMHistory:
        if period != "24h" or document.get("schema_version") != RAW_DASHBOARD_SCHEMA:
            raise DashboardSourceFailure("DASHBOARD_SCHEMA_FAILURE", "MALFORMED_SOURCE_DATA")
        DashboardPMSource._require_source_identity(document)
        snapshot = DashboardPMSource._source_snapshot(document)
        window_start, window_end = DashboardPMSource._source_window(document, period)
        rows = document.get("readings")
        cycles = document.get("missing_cycles")
        if not isinstance(rows, list) or not isinstance(cycles, list):
            raise DashboardSourceFailure("DASHBOARD_SCHEMA_FAILURE", "MALFORMED_SOURCE_DATA")
        series: list[dict[str, Any]] = []
        previous: datetime | None = None
        try:
            for index, raw in enumerate(rows):
                row = _require_mapping(raw, f"dashboard.readings[{index}]")
                timestamp, parsed = _utc(row.get("timestamp"), f"dashboard.readings[{index}].timestamp")
                if parsed < window_start or parsed > window_end:
                    raise ValueError("dashboard raw reading is outside its window")
                if previous is not None and parsed < previous:
                    raise ValueError("dashboard raw readings are not ordered")
                previous = parsed
                series.append({
                    "timestamp_utc": timestamp,
                    "measurements": _measurement_projection(row, prefix=f"dashboard.readings[{index}]"),
                })
            gaps: list[dict[str, str]] = []
            for index, raw in enumerate(cycles):
                cycle = _require_mapping(raw, f"dashboard.missing_cycles[{index}]")
                timestamp, parsed = _utc(cycle.get("timestamp_utc"), f"dashboard.missing_cycles[{index}].timestamp_utc")
                if parsed < window_start or parsed > window_end:
                    raise ValueError("dashboard missing cycle is outside its window")
                kind = cycle.get("kind")
                if not isinstance(kind, str) or _GAP_KIND.fullmatch(kind) is None:
                    raise ValueError("dashboard missing-cycle kind is invalid")
                gaps.append(_gap(timestamp, timestamp))
        except (KeyError, TypeError, ValueError):
            raise DashboardSourceFailure("DASHBOARD_SCHEMA_FAILURE", "MALFORMED_SOURCE_DATA") from None
        return PMHistory(
            period=period,
            representation="RAW_RECEIPTS",
            source_snapshot_at_utc=snapshot,
            series=tuple(series),
            gaps=_deduplicated_gaps(gaps),
        )

    @staticmethod
    def _aggregate_measurements(
        channels: Mapping[str, Any],
        index: int,
        *,
        reading_count: int,
    ) -> dict[str, float | None]:
        result: dict[str, float | None] = {}
        for name in _CHANNEL_FIELDS:
            channel = _require_mapping(channels.get(name), f"dashboard.buckets[{index}].channels.{name}")
            count = channel.get("count")
            if isinstance(count, bool) or not isinstance(count, int) or not 0 <= count <= reading_count:
                raise ValueError("dashboard aggregate channel count is invalid")
            minimum = 0 if name in {"PM2.5", "PM10", "humidity", "pressure"} else None
            lowest = _number(channel.get("min"), f"dashboard aggregate {name}.min", minimum=minimum)
            average = _number(channel.get("avg"), f"dashboard aggregate {name}.avg", minimum=minimum)
            highest = _number(channel.get("max"), f"dashboard aggregate {name}.max", minimum=minimum)
            if count == 0 and any(value is not None for value in (lowest, average, highest)):
                raise ValueError("empty dashboard aggregate channel has statistics")
            if count > 0 and any(value is None for value in (lowest, average, highest)):
                raise ValueError("observed dashboard aggregate channel has incomplete statistics")
            if lowest is not None and average is not None and highest is not None and not lowest <= average <= highest:
                raise ValueError("dashboard aggregate channel statistics are inconsistent")
            target = {
                "PM2.5": "pm25_ug_m3",
                "PM10": "pm10_ug_m3",
                "temperature": "temperature_c",
                "humidity": "humidity_percent",
                "pressure": "pressure_hpa",
            }[name]
            result[target] = average
        return result

    @staticmethod
    def _aggregate_history(document: Mapping[str, Any], period: str) -> PMHistory:
        if period not in {"7d", "30d"} or document.get("schema_version") != AGGREGATE_DASHBOARD_SCHEMA:
            raise DashboardSourceFailure("DASHBOARD_SCHEMA_FAILURE", "MALFORMED_SOURCE_DATA")
        DashboardPMSource._require_source_identity(document)
        snapshot = DashboardPMSource._source_snapshot(document)
        window_start, window_end = DashboardPMSource._source_window(document, period)
        buckets = document.get("buckets")
        bands = document.get("gap_bands")
        if not isinstance(buckets, list) or not isinstance(bands, list):
            raise DashboardSourceFailure("DASHBOARD_SCHEMA_FAILURE", "MALFORMED_SOURCE_DATA")
        series: list[dict[str, Any]] = []
        derived_gaps: list[dict[str, str]] = []
        previous: datetime | None = None
        try:
            for index, raw in enumerate(buckets):
                bucket = _require_mapping(raw, f"dashboard.buckets[{index}]")
                _, grid_start_at = _utc(bucket.get("grid_start_utc"), f"dashboard.buckets[{index}].grid_start_utc")
                start, start_at = _utc(bucket.get("bucket_start_utc"), f"dashboard.buckets[{index}].bucket_start_utc")
                end, end_at = _utc(bucket.get("bucket_end_utc"), f"dashboard.buckets[{index}].bucket_end_utc")
                if end_at <= start_at or grid_start_at > start_at:
                    raise ValueError("dashboard aggregate bucket interval is invalid")
                if start_at < window_start or end_at > window_end:
                    raise ValueError("dashboard aggregate bucket is outside its window")
                if previous is not None and start_at < previous:
                    raise ValueError("dashboard aggregate buckets are not ordered")
                previous = end_at
                reading_count = bucket.get("reading_count")
                if isinstance(reading_count, bool) or not isinstance(reading_count, int) or reading_count < 0:
                    raise ValueError("dashboard aggregate reading count is invalid")
                missing_count = bucket.get("event_missing_count")
                if isinstance(missing_count, bool) or not isinstance(missing_count, int) or missing_count < 0:
                    raise ValueError("dashboard aggregate missing-event count is invalid")
                gap_state = bucket.get("gap_state")
                if gap_state not in _AGGREGATE_GAP_STATES:
                    raise ValueError("dashboard aggregate gap state is invalid")
                expected_gap_state = (
                    "observed_with_missing_events" if reading_count > 0 and missing_count > 0
                    else "observed" if reading_count > 0
                    else "missing_events" if missing_count > 0
                    else "no_observations"
                )
                if gap_state != expected_gap_state:
                    raise ValueError("dashboard aggregate gap state is inconsistent")
                series.append({
                    "timestamp_utc": end,
                    "bucket_start_utc": start,
                    "bucket_end_utc": end,
                    "reading_count": reading_count,
                    "gap_state": gap_state,
                    "measurements": DashboardPMSource._aggregate_measurements(
                        _require_mapping(bucket.get("channels"), f"dashboard.buckets[{index}].channels"),
                        index,
                        reading_count=reading_count,
                    ),
                })
                if gap_state in {"observed_with_missing_events", "missing_events"}:
                    derived_gaps.append(_gap(start, end))
            declared_gaps: list[dict[str, str]] = []
            for index, raw in enumerate(bands):
                band = _require_mapping(raw, f"dashboard.gap_bands[{index}]")
                start, start_at = _utc(band.get("from_utc"), f"dashboard.gap_bands[{index}].from_utc")
                end, end_at = _utc(band.get("to_utc"), f"dashboard.gap_bands[{index}].to_utc")
                if start_at < window_start or end_at > window_end:
                    raise ValueError("dashboard gap band is outside its window")
                if end_at < start_at:
                    raise ValueError("dashboard gap band interval is invalid")
                kind = band.get("kind")
                count = band.get("missing_cycle_count")
                if (
                    not isinstance(kind, str)
                    or _GAP_KIND.fullmatch(kind) is None
                    or isinstance(count, bool)
                    or not isinstance(count, int)
                    or count < 0
                ):
                    raise ValueError("dashboard gap band is invalid")
                declared_gaps.append(_gap(start, end))
        except (KeyError, TypeError, ValueError):
            raise DashboardSourceFailure("DASHBOARD_SCHEMA_FAILURE", "MALFORMED_SOURCE_DATA") from None
        # A declared band is more precise. Bucket-state gaps protect the chart
        # against a future source response that accidentally omits those bands.
        return PMHistory(
            period=period,
            representation="UTC_BUCKET_AVERAGES",
            source_snapshot_at_utc=snapshot,
            series=tuple(series),
            gaps=_deduplicated_gaps([*declared_gaps, *derived_gaps]),
        )

    def _load_history(self, period: str) -> PMHistory:
        document = self._request_document(period)
        return self._raw_history(document, period) if period == "24h" else self._aggregate_history(document, period)

    def history(self, period: str) -> PMHistory:
        if period not in PERIODS:
            raise ValueError("dashboard period is invalid")
        now = monotonic()
        with self._cache_lock:
            cached = self._cache.get(period)
            if cached is not None and cached.expires_at >= now:
                return cached.value
        result = self._load_history(period)
        if self.config.cache_seconds:
            with self._cache_lock:
                self._cache[period] = _CacheEntry(monotonic() + self.config.cache_seconds, result)
        return result

    def latest(self) -> dict[str, Any] | None:
        history = self.history("24h")
        return None if not history.series else dict(history.series[-1])
