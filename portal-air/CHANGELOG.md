# Changelog

> **Classification:** `INTEGRATION_DOC_ADDENDUM`. This file was created in the
> umbrella repository during integration of the immutable sanitized r5 snapshot.
> It is not part of that immutable r5 source tree.

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
