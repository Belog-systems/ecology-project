# Future-only boundaries

## Self-hosted deployment

Future-only. It requires an explicit decision on operating system support,
secret custody, retention, monitoring, upgrades, rollback and restore rehearsal.
This baseline supplies no installer, infrastructure template or approval.

## Map rendering and provider replacement

Map rendering is not included in this source baseline. The accepted production
policy remains outside this candidate; it includes no map library, tile URL,
coordinate, marker or runtime configuration. A future map implementation or
provider replacement requires separate review of terms, attribution,
privacy/referrer behavior, traffic, availability, caching, browser acceptance
and rollback.

## Module API

Future-only. A generic API must first define versioning, authentication,
authorization, provenance, pagination, rate limits, privacy projection, errors
and deprecation. Current V1 read APIs are not silently a Module API.

## Separate frontend/layout

Future-only. A separate frontend must consume an accepted data contract and
preserve time, gap, provenance and location semantics. It needs its own browser
acceptance.

## Store-and-forward/replay

Future architectural requirement only. Any implementation must first define
packet identity, idempotency, station time versus receipt time, buffering,
ordering, authentication and diagnostics.

## External WEATHER work

Future provider work requires explicit provenance, source observation time,
availability/failure semantics, terms and retention. This baseline performs no
provider registration, polling or production write.
