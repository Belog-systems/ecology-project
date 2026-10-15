# Reuse guide: apply the method, not a production environment

This guide turns the retained Portal Air lessons into a safe starting checklist
for another monitoring project. It is deliberately not an installer, a
deployment runbook, or permission to reuse live data, third-party content,
credentials, locations, or operational configuration.

## 1. Start with boundaries

Before copying code or architecture, write down:

- the physical device and the exact firmware build being evaluated;
- who owns each data source and whether it is on-site, external observation,
  crowdsourced observation, model, forecast, or reanalysis;
- what location precision, public display, retention, and export are allowed;
- who may operate secrets, infrastructure, backup, recovery, and incident
  response; and
- the difference between a local test, a technical probe, physical-device
  acceptance, ordinary-browser acceptance, and production acceptance.

Do not use this repository as evidence that the same decisions are correct for a
different device, jurisdiction, provider, or deployment.

## 2. Establish the device contract before implementation

- [ ] Capture a real request from the physical device through a narrow,
  credential-safe receiver.
- [ ] Record safe method/path/query/header/body facts and server receipt time.
- [ ] Preserve a sanitized canonical fixture for regression; do not publish raw
  credentials or device identity.
- [ ] Test byte-sensitive expectations separately from semantic JSON parsing
  when the physical sender requires it.
- [ ] Keep device clock/time-sync state explicit; an absent source observation
  time remains absent rather than being reconstructed from server receipt.
- [ ] Derive identity from the actual wire protocol rather than IP address,
  browser-like user agent, or a visually similar hardware label.
- [ ] Check real payload size, accepted HTTP statuses, and redirect behavior for
  the exact embedded client.

**Stop condition:** do not finalize an API contract because a legacy backend or
firmware prose appears plausible.

### Future firmware boundary

If the device does not provide a trustworthy measurement timestamp, verified
server identity, durable queue, deterministic replay identity, ordering, and
overflow behavior, record those as open requirements. A transport gateway can
solve a particular compatibility problem; it does not automatically add those
firmware capabilities.

## 3. Build ingest as evidence preservation first

- [ ] Record server receipt time at the start of processing.
- [ ] Safely retain raw receipt evidence before parsing.
- [ ] Redact or exclude credentials, authorization headers, cookies, secret
  query parameters, and sensitive configuration before storage.
- [ ] Give parsing explicit outcomes such as valid, partial, invalid, and
  parse-error rather than deleting difficult input.
- [ ] Keep known normalized fields nullable where a source may omit them.
- [ ] Preserve a relation from normalized data to the safe receipt record.
- [ ] Keep duplicate-delivery evidence distinct from normalized-observation
  identity.

**Stop condition:** a parser failure must not silently become “no request was
received.”

## 4. Preserve time, gaps, and completeness honestly

- [ ] Store source observation time separately from server receipt/fetch time.
- [ ] Leave an unknown true observation time unknown; do not fill it with receipt
  time.
- [ ] Record source report/publication/model-run time separately when relevant.
- [ ] Select and document an expected event cadence explicitly.
- [ ] Compute event completeness separately from endpoint uptime and from
  per-channel completeness.
- [ ] Preserve numeric zero as a real value rather than treating it as missing.
- [ ] Render declared or sufficiently long gaps as visual breaks.
- [ ] Describe a gap as “data did not arrive” unless independent diagnostics
  establish a specific cause.

**Stop condition:** never infer a power, network, device, or server failure from
one missing-data interval alone.

## 5. Test constrained TLS with the actual constrained client

- [ ] Verify the device's supported TLS version, certificate behavior, receive
  limits, and maximum-fragment/record requirements.
- [ ] Inspect actual handshake records; extension negotiation alone is not proof
  of compatible record serialization.
- [ ] Keep pre-HTTP failures separate from HTTP, authentication, parser, and
  database diagnoses.
- [ ] If an adaptation gateway is required, restrict it to transport and request
  boundary controls; do not turn it into an undocumented parser or queue.
- [ ] Verify upstream TLS normally and retain a rollback plan for gateway
  changes.
- [ ] Run a physical-device acceptance after certificate, chain, TLS library,
  proxy, or gateway changes.
- [ ] Plan a firmware improvement path for verified server identity rather than
  accepting insecure validation as a permanent design goal.

**Stop condition:** browser or command-line HTTPS success is not embedded-client
acceptance.

## 6. Introduce external sources one lane at a time

For every provider, document:

- [ ] source class (`OBSERVATION`, `AGGREGATED_OBSERVATION`,
  `CROWDSOURCED_OBSERVATION`, `MODEL`, `FORECAST`, `REANALYSIS`, or another
  reviewed class);
- [ ] provider/source/station/sensor identity and upstream relationship;
- [ ] observation, changed/revision, receipt/fetch, and publication/model time;
- [ ] units, missing-field rules, stale state, error state, and deduplication;
- [ ] retention, backup, attribution, display, export, and redistribution terms;
- [ ] provider access, quota, rate, and authentication requirements; and
- [ ] a source-specific quality/placement/representativeness qualification plan.

Use this staged flow:

```text
research
  -> offline fixture and parser test
  -> bounded live probe with explicit request budget
  -> isolated shadow qualification
  -> separately approved production decision
```

Never average or silently fuse values solely because they share a field label.
Airport, home-station, model, forecast, and on-site values can all be useful but
must keep their own provenance.

**Stop conditions:**

- An HTTP access/policy result is not proof of a provider's universal
  availability or of a particular geographic/legal cause.
- A public community device is not automatically qualified.
- Do not use a VPN, proxy, scraping, or a guessed endpoint to evade access or
  policy restrictions.
- Do not transmit an API key over a transport that the provider has not
  documented and authorized as secure.

## 7. Treat Linux packaging as a tested artifact

- [ ] Test the installed artifact, not only the source checkout.
- [ ] Verify LF line endings and shebang bytes for executable scripts.
- [ ] Verify executable bit, ownership, and least-privilege filesystem access.
- [ ] Verify service-manager sandbox/namespace paths actually match the
  application's needs.
- [ ] Exercise one bounded real service run, not only static unit syntax.
- [ ] Keep service-specific data and failure accounting isolated by provider or
  task where appropriate.
- [ ] Define rollback before enabling a timer or recurring collection.

Containers are neither required nor rejected by this guide. Choose them only for
a concrete requirement; still test image bytes, secret injection, permissions,
network policy, data retention, logs, backup, and restore in the final operating
environment.

## 8. Separate API acceptance from browser acceptance

- [ ] Define a minimal public projection; browsers must not receive upstream
  endpoints, database access, raw ingest, or server-side credentials.
- [ ] Keep same-origin and privacy/security-header behavior explicit.
- [ ] Test data contract, freshness, provenance, status, and gap semantics at
  the API boundary.
- [ ] Run ordinary-browser acceptance with an installed Chrome or Edge, a fresh
  task-owned profile, no user-agent override, no injected cookie/auth header,
  no proxy, and no TLS bypass.
- [ ] Confirm normal navigation, expected content, critical same-origin API
  success, controls, and error/missing-data presentation.
- [ ] Verify a read-path/UI deployment does not interrupt protected ingest.

**Stop condition:** a `curl` result, a special user agent, a test fixture, or a
synthetic POST does not satisfy public user-browser acceptance.

## 9. Make diagnostics secret-safe by design

- [ ] Keep credentials and private configuration outside Git and document roots.
- [ ] Do not print or retain secret values in reports, tests, logs, or command
  lines.
- [ ] Do not inspect password values through accessibility, debug, or browser
  automation APIs.
- [ ] Use safe presence/schema/boolean checks or protected digests instead.
- [ ] Redact before raw retention and verify redaction with tests.
- [ ] Treat actual disclosure as a rotation event, not merely a scanner finding.
- [ ] Use a private channel for suspected disclosures and omit the value itself.

## 10. Prove recovery, not merely backup creation

- [ ] Define backup scope, retention, encryption, key custody, and off-host
  storage before relying on the artifact.
- [ ] Record artifact identity safely (for example, size and digest).
- [ ] Restore to a new isolated disposable target, never over production.
- [ ] Compare expected schema, data relationships, integrity, and representative
  time/data coverage.
- [ ] Record precisely whether the exercise covers same-host recovery, off-host
  recovery, independent-machine recovery, secrets, and full reprovisioning.
- [ ] Keep unresolved recovery boundaries visible as `PARTIAL` or `OPEN`.

## 11. Publish only a purpose-built public subset

- [ ] Use an explicit reviewed path allowlist rather than copying an entire
  source tree or Git history.
- [ ] Exclude credentials, private configuration, raw packets/data, logs,
  backups, evidence archives, browser profiles, production paths, hostnames,
  addresses, and precise location material.
- [ ] Do not invent a realistic substitute location to fill an omitted marker.
- [ ] Scan for disclosures and manually review every advisory; scanners are not
  a replacement for human privacy/security review.
- [ ] Check links, staged diff scope, file types, and line endings in the final
  candidate tree.
- [ ] Preserve immutable public tags/releases and publish later improvements as
  successor commits rather than rewriting history.
- [ ] Confirm copyright and license status separately; public visibility alone
  is not a reuse grant.

## 12. Minimal acceptance matrix for a new project

| Claim | Minimum evidence |
| --- | --- |
| Device request shape | Real capture plus sanitized fixture replay |
| Embedded transport compatibility | Packet-level inspection and physical-device acceptance |
| Ingest persistence | Safe receipt plus linked normalized record where parsing permits |
| Completeness | Explicit cadence configuration/calibration and gap-aware result |
| External source suitability | Provenance/terms review, bounded probe, and shadow qualification |
| Linux execution | Final installed artifact plus bounded service execution |
| Browser usability | Ordinary browser with a fresh profile and normal same-origin behavior |
| Backup/recovery | Isolated restore and stated logical comparison scope |
| Public sharing | Reviewed allowlist, privacy/security scan, manual review, and final diff |

## Related documents

- [FAQ.md](FAQ.md) explains why the checklist exists.
- [INCIDENT_LESSONS.md](INCIDENT_LESSONS.md) gives the sanitized historic cases.
- [TESTING.md](TESTING.md) lists the safe local checks supplied by this source
  reference.
- [PRIVACY_AND_LOCATION.md](PRIVACY_AND_LOCATION.md) and
  [PUBLICATION_AUDIT.md](PUBLICATION_AUDIT.md) define public-sharing boundaries.
