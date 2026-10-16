# Portal Air

[Русский](README.md) | [English](README.en.md)

> **Public-repository status.** Portal Air is published here as a sanitized
> source reference and documentation set. It is not a ready-to-install package,
> an export of an operating infrastructure, or evidence of the current state of
> any external service. The immutable baseline tag is preserved separately;
> later documentation is published in successor commits and does not alter that
> tag.

## 1. What Portal Air is

Portal Air is an environmental-monitoring project that grew from the need to
receive and explain data from a real station reliably. Its concern is not only a
chart of concentrations, but also the provenance of every value, the difference
between measurement and server-receipt time, honest rendering of missing data,
and reviewable trust boundaries for external data.

The public repository preserves safely publishable source material and
engineering lessons. It deliberately does not reproduce the private working
environment, operational data, or deployment configuration.

## 2. What the system was created to do

The Portal Air method is intended for work that needs to:

- establish the physical device's actual protocol before designing an API;
- retain a safe raw record of receipt before normalizing data;
- normalize known measurements without losing partial or erroneous deliveries;
- distinguish source-observation time, receipt time, and other time facts;
- render missing data as a gap rather than an invented zero or an asserted
  failure cause;
- calculate event completeness against an explicit cadence and assess channel
  completeness separately;
- retain provenance for external WEATHER sources without representing a model,
  forecast, or remote observation as a local measurement;
- test transport, ordinary browser use, backup, and restore as separate evidence
  classes; and
- publish only material that has passed privacy and security review.

## 3. Which actual components exist

The safely published engineering history establishes that the project included a
real PM-measuring station, a bounded TLS ingress for embedded-client
compatibility, a private receipt/normalization lane, and read-only data
projections. WEATHER sources and the limits of their provenance were researched
separately.

The public repository itself contains only:

- a sanitized, read-only PM-source reader in `portal_air_v1/`;
- synthetic fixtures and local tests for that reader;
- the dependency-free `tools/publication_audit.py` and its tests; and
- technical documentation, FAQ, incident histories, and a guide for safe reuse.

It contains no live endpoint, ingest listener, database, dashboard, map runtime,
provider polling, gateway configuration, or station control.

## 4. Conceptual architecture of the operating project

The following is a conceptual boundary only, not a production topology, hostname,
address, or configuration:

```text
Physical station
    -> controlled TLS/HTTP boundary
        -> safe raw receipt evidence
            -> normalization of known measurements
                -> private Readings and analytical/read-only projections

External WEATHER sources
    -> isolated research / shadow qualification
        -> provenance and health facts
            -> separate decision about any later use
```

The WEATHER lane must not implicitly alter PM data. Moving from source research
to production use requires a separate review.

## 5. What was implemented in the private working system

The published histories describe approaches implemented in the private working
system: raw-first receipt, explicit parse outcomes, separate time fields,
repeated-delivery handling, event-cadence completeness, long-gap rendering, a
bounded transport adaptation for the embedded client, and separation of a
technical HTTP probe from ordinary-browser acceptance.

They also describe isolated research into external WEATHER sources and recovery
verification within bounded scopes. These facts are historical and
evidence-bounded: the public repository does not disclose the private runtime or
confirm its current availability, configuration, or recovery completeness.

## 6. What is available in public GitHub

Public GitHub provides a narrow reviewed reference tree for studying PM-source
reading semantics, time and privacy boundaries, safe local checks, and practical
engineering decisions. Full Russian and English project pages and two complete
FAQ editions are available.

It is useful material for reviewing and designing a similar system, but it is
not an independent service that can be installed without further work.

## 7. Which functions are excluded from the published reference version

The public version intentionally excludes:

- credentials, sessions, private configuration, hostnames, addresses, and exact
  or approximate location data;
- raw packets, observations, the production database, backup, evidence, and
  handoff artifacts;
- packet ingest, database writing, an API, dashboard, map, browser assets, and a
  station-control path;
- TLS-gateway, deployment, rollback, and production-monitoring configuration;
- provider registration, keys, live polling, and external WEATHER observations;
  and
- instructions sufficient to reproduce the private infrastructure.

These exclusions protect people, data, and the operating environment; they are
not missing files that a reader should guess or replace.

## 8. Where to find technical documentation

Start with the [documentation index](docs/INDEX.md). In particular, it includes
the [architecture boundary](docs/ARCHITECTURE.md),
[data and time semantics](docs/DATA_AND_TIME_SEMANTICS.md),
[limitations](docs/LIMITATIONS.md), [safe local checks](docs/TESTING.md),
[deployment boundary](docs/DEPLOYMENT.md),
[privacy and location boundary](docs/PRIVACY_AND_LOCATION.md), and the
[reuse guide](docs/REUSE_GUIDE.md).

The remaining technical documentation is preserved in English so that its
technical wording, filenames, and contracts remain unambiguous.

## 9. Where to read the FAQ

- [FAQ in Russian](docs/FAQ.ru.md)
- [FAQ in English](docs/FAQ.md)

Both editions contain all 17 complete questions and answers about protocol,
raw-first ingest, TLS, time, gaps, WEATHER provenance, browser acceptance,
security, recovery, and evidence boundaries.

## 10. Where to find engineering incidents and recommendations

[Incident histories and retained lessons](docs/INCIDENT_LESSONS.md) contains 16
sanitized engineering histories. For practical use of the method in another
project, use [REUSE_GUIDE.md](docs/REUSE_GUIDE.md). These documents explain what
was established, which options failed, and which boundaries remained unverified.

## 11. What is required for an independent deployment

An independent deployment requires a separate, purpose-built reviewed project:
a capture of the actual protocol for its device, a safe secret model, ingress and
TLS, a storage schema, privacy policy, monitoring, backup/restore rehearsal,
rollback plan, external-provider terms, and ordinary-browser acceptance. It must
also select a license and confirm rights for third-party data and components.

The published reference tree must not be treated as installation instructions or
as a sufficient set of files for a self-hosted deployment.

## 12. Current status and limitations

The immutable sanitized baseline is published under its existing tag. Successor
documentation, including this bilingual navigation, is published separately and
does not alter that source baseline. The public source reference does not prove
the current health of the private system, public-browser acceptance, provider
availability, disaster-recovery readiness, or readiness of an installable
package.

Every assertion in the documentation is limited to its evidence scope. A passing
local test, a technical HTTP probe, a historical observation, and full production
acceptance are different results.

## 13. Licensing information

No license has yet been selected for Portal Air source code or documentation.
Public availability of the repository does not itself grant reuse,
redistribution, or sublicensing rights. See [LICENSE_STATUS.md](LICENSE_STATUS.md).
Any future license choice or addition of third-party components requires a
separate decision and compliance with the applicable terms.
