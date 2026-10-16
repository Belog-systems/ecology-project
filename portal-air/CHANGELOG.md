# Changelog

> **Classification:** `INTEGRATION_DOC_ADDENDUM`. This file was created in the
> umbrella repository during integration of the immutable sanitized r5 snapshot.
> It is not part of that immutable r5 source tree.

## 2026-10-17 — bilingual public documentation

> **Classification:** `SUCCESSOR_DOCUMENTATION_ADDENDUM`. This docs-only entry
> adds bilingual public navigation and does not modify the immutable baseline
> tag, source-reference behavior, deployment state, or production systems.

### Added

- A Russian-primary Portal Air project page and a content-equivalent English
  edition, with explicit relative language links.
- A full Russian edition of the 17-entry practical FAQ alongside the preserved
  English edition.

### Changed

- Added mutual language navigation to both FAQ editions and links to both
  editions from the documentation index.
- Corrected stale public wording that described already published successor
  documentation as local-only or unpublished.

### Not changed

- The immutable published baseline tag, executable source, `air-device/**`,
  production services, databases, station configuration, DNS, TLS, provider
  registration/polling, credentials, raw data, or deployment configuration.

## Published documentation recovery successor (post-baseline)

> **Classification:** `SUCCESSOR_DOCUMENTATION_ADDENDUM`. This entry documents
> published successor documentation after the immutable published baseline. It
> does not modify the existing tag, source-reference behavior, deployment state,
> or production systems.

### Added

- A thematic, evidence-bound public FAQ that separates historic cases from the
  public source-reference boundary.
- Detailed sanitized incident histories covering device protocol discovery,
  embedded TLS/MFLN compatibility, path and identity handling, raw-first ingest,
  time/gap/completeness semantics, external WEATHER provenance, Linux/service
  packaging, UI/browser acceptance, diagnostic secret safety, recovery, and
  publication hygiene.
- A reusable engineering checklist for new monitoring projects.
- Five additional FAQ entries and incident histories covering Core/browser scope,
  exact nullable-field validation, anonymous DTO/time-label boundaries, WEATHER
  compatibility and fixture cleanup, and evidence limits for assets, data,
  hosting, and recovery.

### Changed

- Corrected stale wording that described the already published immutable
  baseline as an unpublished or private-only candidate.
- Linked the restored engineering knowledge through the Portal Air README and
  documentation index without adding operational topology, data, secrets,
  location state, or deployment instructions.
- Clarified that a historical failed database-restore result remains part of the
  record even where later isolated import evidence superseded it only in its
  stated narrow scope.

### Fixed

- Restored access to accumulated public-safe engineering context that had been
  lost from the sanitized baseline's short FAQ and incident summary, while
  marking superseded or unproven conclusions explicitly.
- Distinguished source fixtures, selected asset comparisons, public technical
  observations, ordinary-browser acceptance, and recovery exercises so that one
  evidence class is not represented as another.

### Not changed

- The immutable published baseline tag and its source-derived content.
- `air-device/**`, production services, databases, station configuration, DNS,
  TLS, provider registration/polling, credentials, raw data, or deployment
  configuration.

## Unreleased — sanitized r5 integration

### Added

- A frozen, sanitized Portal Air V1 PM-source reference in `portal_air_v1/`,
  including synthetic local tests.
- A dependency-free publication-audit tool and its regression tests.
- Documentation for the source-reference boundary, privacy and location
  exclusions, time semantics, explicit missing-data behavior, safe local
  checks, and future-only workstreams.

### Changed

- Replaced the previous public `portal-air/**` narrative with the exact reviewed
  r5 source snapshot. The resulting tree is a curated reference and is not an
  installer, production topology, public listener, map application, or provider
  integration.
- Public documentation now directs readers to the r5 scope and limitations
  rather than claiming deployment or production acceptance from this tree.

### Fixed

- No production runtime defect or operational issue is claimed as fixed here.
  This integration changes only the public source and documentation tree.

### Documented

- The distinction between source observation time and server receipt time, and
  the requirement not to fabricate an observation timestamp.
- The requirement to render declared missing-receipt intervals as gaps rather
  than continuous fabricated data.
- The exclusion of credentials, private configuration, raw observations, exact
  or approximate location state, deployment custody, and internal evidence.

### Preserved and out of scope

- `air-device/**` is preserved unchanged from the public umbrella baseline.
- No Portal Air production service, database, device, DNS, TLS, provider
  registration, polling, deployment, or release remote was changed.
- No license selection is made by this integration; see
  [LICENSE_STATUS.md](LICENSE_STATUS.md).
