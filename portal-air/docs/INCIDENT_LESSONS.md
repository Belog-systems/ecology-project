# Incident histories and retained lessons

> **Purpose and boundary.** These are sanitized histories of real engineering
> cases that informed Portal Air. They preserve the observable symptom, the
> evidence-bound conclusion, and the safe remedy without reproducing production
> configuration, addresses, station identifiers, raw observations, credentials,
> or private evidence.
>
> A historic result is not a statement about the current health of an external
> service. The public reference tree itself contains no live ingest, provider,
> deployment, dashboard, map, or recovery runtime.

## Status vocabulary

| Status | Meaning in this document |
| --- | --- |
| `RESOLVED` | A historic case reached an evidence-backed remedy in its stated scope. |
| `PARTIAL` | A useful capability or conclusion exists, but a broader claim remains unproven. |
| `OPEN` | A required decision, evidence, or implementation is still absent. |
| `DEFERRED` | Work was intentionally not activated or pursued in that case. |
| `SUPERSEDED` | A dated conclusion was replaced by stronger later evidence; the older result remains historical. |

## INC-01 — Capture the physical protocol before designing the ingest contract

**Period:** early station integration
**Status:** `RESOLVED` for the historic device contract; `OPEN` for every new
device or firmware variant.

### What was observed

An older backend contract existed before the physical station had been captured.
It was plausible enough to invite reuse, but it was not evidence that the device
actually emitted that request shape.

### Investigation

A narrow HTTP capture accepted the real device request without depending on the
old application parser, database, or authentication model. The investigation
then separated safe protocol facts—method, path, header names, body structure,
and byte-sensitive fixture properties—from confidential values.

### Failed options

- Declare the old backend endpoint authoritative because code already existed.
- Design the parser from firmware prose alone.
- Generate new JSON in a simulator and call it byte-exact merely because it is
  structurally valid.

### Established cause

The old contract and the actual device wire contract were independent claims.
Only the capture established the latter.

### Remedy and verification

The accepted approach was a raw-first adapter plus a sanitized canonical fixture
used for replay and regression tests. The fixture preserved the distinction
between semantic JSON equivalence and the byte-sensitive form emitted by the
physical device.

### Remaining limit

The result cannot be generalized to another firmware build, station model, or
future protocol revision. Each one requires its own capture and replay evidence.

---

## INC-02 — A path redirect was a protocol failure for the embedded client

**Period:** early HTTP ingress integration
**Status:** `RESOLVED` for the historic route behavior

### What was observed

The station sent to a route whose canonical form differed only by a trailing
slash. A desktop user agent could follow the redirect, but the station did not
produce a usable ingest result.

### Investigation

The team checked the exact request path, status class, and redirect behavior
with redirects disabled. This isolated path canonicalization from Basic
authentication, parsing, database access, and TLS.

### Failed options

- Attribute every failed send to authentication.
- Assume all embedded HTTP clients will follow redirects as browsers do.
- Change parser or database code before proving that the request reached the
  application boundary.

### Established cause

Path canonicalization occurred before the intended application handling. The
device's request therefore did not reach the endpoint in the expected form.

### Remedy and verification

The gateway accepted the relevant path variants and normalized the legacy form
internally instead of asking the device to follow a redirect. Regression checks
validated non-redirect behavior for both variants without sending a real station
packet.

### Remaining limit

This does not license a general redirect policy. Any new client must be tested
against the exact paths it will use.

---

## INC-03 — Protocol identity was not the same as a similar hardware label

**Period:** station authentication and identity integration
**Status:** `RESOLVED` for the historic identity mismatch

### What was observed

Authentication could succeed and a safe receipt record could exist, while the
message still failed identity validation and no normalized reading was created.

### Investigation

The investigation compared only the explicitly agreed protocol identity fields.
It did not use network address, user agent, or a visually similar hardware label
as a substitute identity. One configured value lacked a protocol-specific
prefix/form that was present on the wire.

### Failed options

- Treat the rejection as proof of a wrong password.
- Use an address as the station identity.
- Make a user-agent string or software version an identity key without contract
  evidence.
- Strip or invent a prefix because the remaining characters looked familiar.

### Established cause

The configured identity and the wire identity differed in their required form.
This was a protocol-identity mismatch, not a password or parser failure.

### Remedy and verification

The stored comparison value was corrected to the complete protocol form. Tests
then checked each identity field independently and required a normalized reading
to remain linked to an authenticated, valid raw receipt.

### Remaining limit

Hardware identity can be retained as separate metadata when justified, but it
must not silently replace the identity used by the actual protocol.

---

## INC-04 — Desktop HTTPS success did not prove constrained-device TLS
compatibility

**Period:** direct embedded TLS investigation
**Status:** `RESOLVED` as a bounded transport workaround; `OPEN` for future
firmware authentication hardening.

### What was observed

Ordinary browser and command-line HTTPS checks succeeded against a frontend,
while the constrained station repeatedly failed before any application request
or access-log event appeared.

### Investigation

The evidence was ordered by layer:

1. prove that the expected network/frontend path existed for desktop checks;
2. show that application, authentication, parser, and database code could work
   through controlled synthetic tests;
3. inspect TLS version, maximum-fragment negotiation, certificate validation,
   and actual server-to-client handshake-record boundaries; and
4. compare a physical station handshake through a controlled gateway.

The constrained client had a small TLS receive buffer. The direct frontend's
handshake-record behavior was incompatible with that constraint before HTTP
could begin. The physical firmware did not emit a low-level error code for the
failed handshake, so the causal statement remained a high-confidence,
evidence-bounded engineering conclusion rather than a claim about all embedded
clients.

### Failed options

- Use a successful browser request as proof that the station can negotiate TLS.
- Treat maximum-fragment negotiation alone as proof of real record boundaries.
- Tune JSON size, PHP, database, or Basic authentication while the failure is
  still pre-HTTP.
- Call a synthetic HTTP POST physical-device acceptance.

### Remedy and verification

A dedicated gateway became the narrow ESP-facing TLS boundary. It controlled the
accepted TLS version and record behavior, normalized the known path internally,
limited request shape, and verified its upstream connection. It was not made a
parser, queue, or business-logic layer.

The historical acceptance required all of the following:

- desktop TLS inspection with normal certificate validation;
- packet-level verification of relevant handshake-record boundaries; and
- a physical station handshake, request, response, and acknowledgement.

### Remaining limit

The legacy firmware's server-authentication behavior remained a known security
limitation: channel encryption alone does not prove the device validates the
gateway's identity. A future firmware should use verified CA, hostname, or
appropriate pinned-identity validation. The public reference contains no
gateway configuration or live transport endpoint.

---

## INC-05 — Receipt, observation, repetition, and absence were separate facts

**Period:** ingest normalization and completeness work
**Status:** `PARTIAL` — the semantic model is established; device-side replay
remains a future requirement

### What was observed

A delivered message can have a source observation time, a server receipt time,
and a later publication or model time. Repeated delivery is useful transport
evidence but is not automatically a second physical observation. A missing point
in a chart is not zero and does not identify a physical cause.

### Investigation

The work separated:

- safely retained receipt evidence from normalized values;
- source observation time from receipt/fetch time;
- delivery attempts from deterministic normalized-observation identity;
- expected event cadence from endpoint availability; and
- event completeness from per-channel completeness.

### Failed options

- Substitute receipt time for a missing measurement time.
- Delete malformed or partial input before retaining a safe receipt record.
- Count a missing expected event as a missing value for every channel.
- Draw a continuous line through a declared or long absence.
- State that a gap proves a particular power, Wi-Fi, Internet, device, or server
  failure.

### Established cause

The same display symptom can arise at several layers. A gap establishes absence
under the selected cadence model, not a root cause. A receipt timestamp cannot
recover an unreported observation timestamp.

### Remedy and verification

The resulting pattern retained raw-first evidence, explicit parse outcomes,
nullable known measurements, deterministic duplicate handling, separate time
fields, and visible chart gaps. Tests exercised delayed/repeated delivery,
partial data, empty denominators, window edges, and gap rendering.

### Remaining limit

The current reference reader is receipt-oriented and does not implement ingest.
Store-and-forward, bounded queue behavior, replay identity, ordering, and
device diagnostics require a separate device/firmware design before they can
recover gaps.

---

## INC-06 — External WEATHER data had to remain provenance-aware

**Period:** external-weather research, shadow work, and access qualification
**Status:** `PARTIAL` / provider-specific

### What was observed

The project considered four distinctly different source types:

| Source or lane | Evidence-bound lesson | Public-reference status |
| --- | --- | --- |
| Airport-METAR lane | An airport report is an external physical observation, not a measurement at the Portal Air site. Missing source fields remain missing. | No provider code, data, or polling is in this reference. |
| Meteostat | A bounded request reached an HTTPS responder and received HTTP 451. This established the responder's stated access/compliance outcome, not an independently proven geographic or legal root cause. | Live use remains deferred pending a lawful supported path. |
| Narodmon | Community data needs a secure provider contract, an application/access decision, retention/display terms, and later source qualification. Documentation status changed over time; no candidate device was inferred. | No account, key, request, or provider runtime is present here. |
| Open-Meteo | Model/forecast values are context, not a physical-station observation. | No model integration is present here. |

### Investigation

The weather lane stored provider/source class, source observation time, receipt
time, missing fields, freshness, response/health outcome, and provenance. It
kept source lanes independent and treated shared upstream data as redundancy,
not independent corroboration.

### Failed options

- Present an airport observation as citywide or on-site truth.
- Mix wind speed from one source with direction from another and label the
  result as one instrument's wind vector.
- Relabel forecast/model data as `OBSERVATION`.
- Retry or evade a provider's policy/access restriction.
- Assume that public visibility of a community sensor proves accuracy, outdoor
  placement, continuity, retention rights, or public-display permission.

### Established cause

Similar field names do not make data comparable without source class, location,
time, exposure, upstream, and terms. Provider transport/access status is not a
quality verdict on the underlying phenomenon.

### Remedy and verification

The reusable process is: research, offline fixtures, a bounded live probe with
request accounting, isolated shadow qualification, then a separately reviewed
production decision. Each source keeps independent provenance and failure state.

### Remaining limit

The public reference contains no external WEATHER integration and makes no claim
about current provider availability, source quality, public display rights, or
representativeness. Historic private-lane outcomes must not be copied into a
new project as operating permission.

---

## INC-07 — A Linux service failure was packaging and isolation, not application
logic

**Period:** private scheduled-worker deployment
**Status:** `RESOLVED` for the documented service defects; no container conclusion

### What was observed

One scheduled worker failed because of an unnecessary dependency on a transient
runtime namespace/path. A separate executable wrapper existed and passed
unit-file syntax checks but could not be executed on Linux.

### Investigation

The team inspected actual service results, installed bytes, shebang bytes, line
endings, executable metadata, sandbox paths, and a real bounded service run.
The second wrapper had CRLF line endings, which changed the interpreter path
seen by the operating system.

### Failed options

- Blame application logic without checking the service-manager result.
- Treat static unit syntax validation as execution proof.
- Keep a runtime directory dependency that the worker did not need.
- Assume Windows-edited shell scripts are executable on Linux.

### Established cause

The first defect was a needless namespace/path dependency; the second was CRLF
in the shebang. They were independent operational failures.

### Remedy and verification

The unnecessary path dependency was removed and a bounded no-network execution
verified that correction. The separate executable-wrapper defect was then
corrected through LF packaging checks, installed-byte/shebang and executable
metadata verification, and a real bounded service execution. The service
behavior remained within the intended isolation boundary.

### Remaining limit

No container image or container runtime was part of this case. There is no
evidence that containerization would have been the correct fix. A container is
an implementation choice only when it solves a concrete, separately reviewed
requirement; it does not eliminate the need to test final bytes, permissions,
networking, secrets, and recovery.

---

## INC-08 — API success and ordinary-browser acceptance were different gates

**Period:** dashboard and map work
**Status:** `RESOLVED` as an acceptance method; public-reference UI is absent

### What was observed

A technical HTTP/API result could demonstrate a route or data contract without
demonstrating that an ordinary user browser received the intended page, assets,
same-origin requests, controls, and gap presentation.

### Investigation

The acceptance model separated server/API checks, privacy checks, browser
rendering, and post-change ingest continuity. Browser work used an installed
ordinary browser with a fresh profile and without user-agent override, injected
cookies, special authentication headers, proxy behavior, or TLS bypass.

### Failed options

- Call a command-line HTTP result public-browser acceptance.
- Let a special project user agent or a test-only authentication identity stand
  in for a normal user.
- Treat fixture-only UI tests as live public acceptance.
- Join missing periods visually in a chart because neighboring values exist.

### Established cause

Transport, authorization, assets, rendering, browser policy, and human-visible
semantics are distinct layers. A technical probe cannot exercise all of them.

### Remedy and verification

The reusable acceptance sequence verifies a reviewed same-origin data projection
and then checks normal browser navigation, expected content, critical same-origin
API/render behavior, controls, and explicit gap semantics. It separately
requires evidence that the read path did not break protected ingest continuity.

### Remaining limit

This public source has no browser application, map, coordinates, or HTTP API.
It cannot claim browser acceptance or provide a frontend to deploy.

---

## INC-09 — Diagnostics could disclose the secret they were meant to test

**Period:** credential-safety review
**Status:** `RESOLVED` as a security handling rule

### What was observed

An automation/accessibility surface could expose the value of a field that was
visually masked as a password. Raw request material could also include
authorization data if retained carelessly.

### Investigation

The review distinguished visual masking from programmatic disclosure and looked
for sensitive material in terminal output, reports, fixtures, logs, browser
profiles, screenshots, and raw-retention paths.

### Failed options

- Print a credential temporarily for confirmation.
- Read a password field through debugging/accessibility tooling because it is
  masked in the visible interface.
- Store authorization headers in raw evidence.
- Treat Base64 encoding as secret protection.

### Established cause

Presentation-layer masking does not guarantee that diagnostic interfaces cannot
read the underlying value. Once exposed to an unapproved surface, a credential
must be handled as disclosed.

### Remedy and verification

Diagnostics report safe categories, booleans, schemas, or protected digests
instead of secret values. Sensitive headers are redacted/excluded before
retention; actual disclosure triggers rotation rather than a scanner-only
response.

### Remaining limit

Automated scanning is defense in depth, not a substitute for access control,
manual review, or secret rotation after disclosure.

---

## INC-10 — Backup creation was not restore acceptance

**Period:** backup and recovery verification
**Status:** `SUPERSEDED` for an earlier incomplete restore conclusion; overall DR
remains `PARTIAL`

### What was observed

An earlier fresh backup had artifact-level checks but did not initially produce
enough independent restore evidence to establish logical recovery. This was
recorded as a limitation rather than explained away.

### Investigation

Recovery work distinguished backup creation, artifact identity, provider import,
isolated restore, schema/data comparison, off-host custody, and bare-environment
recovery. The later verification used a new isolated target and bounded,
read-only comparison evidence; production data was not used as a restore target.

### Failed options

- Equate a dump's existence, size, or digest with a successful recovery.
- Restore over production during a test.
- Treat a provider statement as independently verified data.
- Call a same-host operational snapshot complete disaster recovery.

### Established cause

Backup and restore are different capabilities. The earlier incomplete conclusion
was correctly superseded only after stronger isolated restore evidence was
available.

### Remedy and verification

The reusable standard is an isolated restore with explicit comparison of schema,
data relationships, integrity, and the scope of what was exercised. The result
must say whether off-host transfer, independent-machine recovery, secret/key
custody, and full reprovisioning are included or still excluded.

### Remaining limit

The public reference includes no database dump, recovery tooling, or restore
evidence. It therefore makes no operational DR-readiness claim. A future
deployment needs its own protected backup and restore rehearsal.

---

## INC-11 — Publishing engineering lessons required a separate privacy boundary

**Period:** public documentation and source sanitization
**Status:** `RESOLVED` for the immutable baseline; successor documentation is
pending its own review/publication.

### What was observed

Earlier public documentation contained useful technical history alongside detail
that could not safely travel into a long-lived public source tree. A sanitized
reference baseline intentionally removed production data, operational paths,
identities, raw evidence, deployment custody, and inherited private Git history.

### Investigation

The publication workflow used an explicit path allowlist, clean Git history,
synthetic tests, static scanning, manual review, link checking, and inspection
of the final staged tree. It also treated an immutable published tag as a fixed
baseline rather than a document to rewrite retroactively.

### Failed options

- Copy a whole source worktree or Git history into a public repository.
- Publish a raw capture, realistic substitute location, provider secret, or
  internal evidence to make a lesson easier to explain.
- Treat a clean scanner result as the only privacy review.
- Rewrite an immutable historical release to add later documentation.

### Established cause

Public knowledge and internal operational evidence have different audiences,
retention needs, and disclosure risk. Engineering history can be useful without
making an operational environment reproducible to an untrusted reader.

### Remedy and verification

The immutable baseline was preserved. This successor documentation recovers
themes through sanitized, evidence-bound prose and links, while its publication
requires a new diff review, privacy/security scan, link check, and independent
review of the resulting successor commit.

### Remaining limit

Publication does not select a software license or grant rights to third-party
datasets. It also does not turn historic results into a current deployment claim.

## See also

- [FAQ.md](FAQ.md) — structured questions, causes, solutions, and limitations.
- [REUSE_GUIDE.md](REUSE_GUIDE.md) — practical checklist for a different project.
- [PRIVACY_AND_LOCATION.md](PRIVACY_AND_LOCATION.md) — location/data exclusion
  boundary.
- [BACKUP_AND_RESTORE.md](BACKUP_AND_RESTORE.md) — source-reference recovery
  boundary.
