from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from portal_air_v1.dashboard_source import (
    AGGREGATE_DASHBOARD_SCHEMA,
    DASHBOARD_SOURCE_SCHEMA,
    RAW_DASHBOARD_SCHEMA,
    DashboardPMSource,
    DashboardSourceConfig,
    DashboardSourceFailure,
)


def config_document(**overrides: object) -> dict[str, object]:
    return {
        "schema_version": DASHBOARD_SOURCE_SCHEMA,
        "origin_hostname": "pm-source.example.invalid",
        "connect_address": "192.0.2.10",
        "timeout_seconds": 10,
        "max_response_bytes": 200_000,
        "cache_seconds": 0,
        **overrides,
    }


def raw_document() -> dict[str, object]:
    return {
        "schema_version": RAW_DASHBOARD_SCHEMA,
        "generated_at_utc": "2026-01-01T01:00:00Z",
        "station": {"identity": {"id": 1}},
        "window": {"name": "24h", "start_utc": "2025-12-31T01:00:00Z", "end_utc": "2026-01-01T01:00:00Z"},
        "readings": [{"timestamp": "2026-01-01T00:59:00Z", "PM2.5": 7.2, "PM10": 12.3, "temperature": 18.4, "humidity": 61.0, "pressure": 1007.8, "upstream_record_id": 42}],
        "missing_cycles": [{"timestamp_utc": "2026-01-01T00:30:00Z", "kind": "internal"}],
    }


def aggregate_document(period: str = "7d") -> dict[str, object]:
    return {
        "schema_version": AGGREGATE_DASHBOARD_SCHEMA,
        "generated_at_utc": "2026-01-01T01:00:00Z",
        "station": {"identity": {"id": 1}},
        "window": {"name": period, "start_utc": "2025-12-25T01:00:00Z", "end_utc": "2026-01-01T01:00:00Z"},
        "buckets": [
            {"grid_start_utc": "2026-01-01T00:00:00Z", "bucket_start_utc": "2026-01-01T00:00:00Z", "bucket_end_utc": "2026-01-01T00:30:00Z", "reading_count": 1, "event_missing_count": 0, "gap_state": "observed", "channels": {name: {"count": 1, "avg": value, "min": value, "max": value} for name, value in (("PM2.5", 7.2), ("PM10", 12.3), ("temperature", 18.4), ("humidity", 61.0), ("pressure", 1007.8))}},
            {"grid_start_utc": "2026-01-01T00:30:00Z", "bucket_start_utc": "2026-01-01T00:30:00Z", "bucket_end_utc": "2026-01-01T01:00:00Z", "reading_count": 0, "event_missing_count": 1, "gap_state": "missing_events", "channels": {name: {"count": 0, "avg": None, "min": None, "max": None} for name in ("PM2.5", "PM10", "temperature", "humidity", "pressure")}},
        ],
        "gap_bands": [{"from_utc": "2026-01-01T00:30:00Z", "to_utc": "2026-01-01T01:00:00Z", "kind": "internal", "missing_cycle_count": 1}],
    }


class DashboardSourceTests(unittest.TestCase):
    def source(self) -> DashboardPMSource:
        return DashboardPMSource(DashboardSourceConfig.from_document(config_document()))

    def test_config_validates_safe_structural_values(self) -> None:
        config = DashboardSourceConfig.from_document(config_document())
        self.assertEqual(config.origin_hostname, "pm-source.example.invalid")
        with self.assertRaises(ValueError):
            DashboardSourceConfig.from_document(config_document(connect_address="0.0.0.0"))
        with self.assertRaises(ValueError):
            DashboardSourceConfig.from_document(config_document(connect_address="127.0.0.1"))
        with self.assertRaises(ValueError):
            DashboardSourceConfig.from_document(config_document(extra="unexpected"))

    def test_documentation_config_example_is_structurally_valid(self) -> None:
        path = Path(__file__).parents[1] / "config.example.json"
        config = DashboardSourceConfig.from_document(json.loads(path.read_text(encoding="utf-8")))
        self.assertEqual(config.origin_hostname, "pm-source.example.invalid")
        self.assertEqual(config.connect_address, "192.0.2.10")

    def test_raw_history_projects_only_allowlisted_measurements(self) -> None:
        result = self.source()._raw_history(raw_document(), "24h")
        self.assertEqual(result.representation, "RAW_RECEIPTS")
        self.assertEqual(set(result.series[0]["measurements"]), {"pm25_ug_m3", "pm10_ug_m3", "temperature_c", "humidity_percent", "pressure_hpa"})
        self.assertNotIn("upstream_record_id", json.dumps(result.series))
        self.assertEqual(result.gaps[0]["kind"], "MISSING_RECEIPTS")

    def test_source_identity_requires_a_positive_integer_without_fixed_identity(self) -> None:
        document = raw_document()
        document["station"]["identity"]["id"] = 0  # type: ignore[index]
        with self.assertRaises(DashboardSourceFailure):
            self.source()._raw_history(document, "24h")

    def test_aggregate_history_preserves_gap_state(self) -> None:
        result = self.source()._aggregate_history(aggregate_document(), "7d")
        self.assertEqual(result.representation, "UTC_BUCKET_AVERAGES")
        self.assertIsNone(result.series[1]["measurements"]["pm25_ug_m3"])
        self.assertEqual(result.gaps[0]["kind"], "MISSING_RECEIPTS")

    def test_pinned_transport_still_uses_the_configured_hostname_for_tls(self) -> None:
        observed: dict[str, object] = {}

        class Socket:
            def settimeout(self, _value: float) -> None: pass
            def close(self) -> None: pass

        class TLS:
            def settimeout(self, _value: float) -> None: pass
            def sendall(self, request: bytes) -> None: observed["request"] = request.decode("ascii")
            def close(self) -> None: pass

        class Context:
            def wrap_socket(self, _raw: Socket, *, server_hostname: str) -> TLS:
                observed["server_hostname"] = server_hostname
                return TLS()

        source = DashboardPMSource(
            DashboardSourceConfig.from_document(config_document()),
            socket_factory=lambda address, timeout: observed.update(address=address, timeout=timeout) or Socket(),  # type: ignore[arg-type]
            ssl_context_factory=lambda: Context(),  # type: ignore[arg-type]
        )
        with patch("portal_air_v1.dashboard_source.HTTPResponse") as response_type:
            response = response_type.return_value
            response.status = 200
            response.getheader.side_effect = lambda name, default=None: "application/json" if name == "Content-Type" else None
            response.read.return_value = json.dumps(raw_document()).encode("utf-8")
            self.assertEqual(len(source.history("24h").series), 1)
        self.assertEqual(observed["address"], ("192.0.2.10", 443))
        self.assertEqual(observed["server_hostname"], "pm-source.example.invalid")
