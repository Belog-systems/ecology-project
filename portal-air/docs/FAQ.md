# Practical FAQ and engineering lessons

> **Scope.** This document is a documentation-recovery successor to the
> immutable sanitized Portal Air baseline. It retains sanitized lessons from
> historical engineering cases. It is not an operating runbook, a deployment
> guide, or proof of the present health of any external system.

## How to read the answers

- **Established cause** means the stated conclusion was supported by the
  recorded case evidence. It is not a claim that every device, provider, or
  deployment has the same cause.
- **Not established** means the available evidence did not justify a more
  specific conclusion. This is intentional, not a missing diagnosis.
- **Reference tree** means the public sanitized source in this repository. It
  is distinct from historic cases that informed the lessons.
- Historical details are generalized: no credentials, raw observations,
  private topology, real station identity, or precise location are reproduced.

## 1. Is this a production deployment package?

**Question.** Can this repository be deployed or treated as a live Portal Air
service?

**Context.** The published baseline is a curated source reference produced from
a public-safe source boundary. It retains a narrow PM-source reader and
documentation, not an application deployment or a copy of operational systems.

**Symptoms.** A reader may find source code, tests, and an immutable baseline
tag and conclude that a listener, database, dashboard, map, provider collector,
or station configuration is included.

**Diagnostics.** Inspect the tracked paths and the documentation index. The
reference contains no listener configuration, live endpoint, deployment
inventory, database dump, provider registration, browser application, or device
control path.

**Failed options.** Treating a source checkout, a passing local test, or a
published Git tag as deployment evidence would conflate source review with
runtime acceptance.

**Established cause.** The baseline was deliberately sanitized to remove
operational custody material and to make public review possible without exposing
private infrastructure or data.

**Solution.** Keep the reference as a source-level teaching and review artifact.
Design any derivative deployment separately, including secrets, ingress, source
contracts, privacy, backup/restore, rollback, monitoring, and browser
acceptance.

**Verification.** The included checks use synthetic fixtures and a local
publication audit. They establish only the documented local source behavior.

**Current status.** The immutable published baseline remains a source reference.
This documentation successor adds explanation only; it does not add a deployable
runtime or change any deployment.

**Recommendations.** Start with [CURRENT_STATE.md](CURRENT_STATE.md),
[LIMITATIONS.md](LIMITATIONS.md), and [REUSE_GUIDE.md](REUSE_GUIDE.md) before
copying any design idea.

**History.** The early public documentation described engineering outcomes more
directly. The later sanitized baseline intentionally removed operational detail;
this FAQ restores the lessons without restoring sensitive material.

## 2. How should a station protocol be established?

**Question.** Is it safe to design an ingest API from an old backend or device
documentation?

**Context.** A historic station integration began with an unknown real request,
while an older backend already had a tempting but unverified contract.

**Symptoms.** A server can appear ready, yet a physical device may send a
different method, path, identity form, body structure, or authentication scheme.

**Diagnostics.** Receive one real request with a narrow capture adapter that is
independent of the intended parser. Record the safe facts: method, path, query,
headers after redaction, body bytes after redaction, and server receipt time.
Turn the safe representation into a regression fixture.

**Failed options.** Reusing an old endpoint contract, guessing request fields,
or treating a simulator's newly generated JSON as proof of the physical device's
wire bytes were rejected approaches.

**Established cause.** Existing code and firmware prose did not establish the
physical station's actual wire contract. Only a real capture did.

**Solution.** Build a raw-first adapter to the observed packet. Make parser
changes after fixture replay, and repeat capture/replay when firmware behavior
changes.

**Verification.** A useful fixture checks both structural interpretation and,
where required, byte-sensitive properties such as body size and digest without
publishing the original packet.

**Current status.** The public reference retains the principle but does not
include a packet ingest endpoint or a real station fixture.

**Recommendations.** Capture before designing schema or authentication. Keep
unknown safe fields and partial packets as evidence rather than discarding them.

**History.** The historic case replaced an assumed legacy contract with a
captured device contract and a regression workflow.

## 3. Why keep raw receipt evidence separate from normalized readings?

**Question.** Why not parse a request first and save only the final values?

**Context.** Field devices and external sources can send incomplete, malformed,
or newly extended messages. A parser can also have a defect.

**Symptoms.** If normalization fails first, it may become impossible to tell
whether anything arrived, what changed in a later firmware version, or whether a
parser regression caused the loss.

**Diagnostics.** Compare receipt evidence, parse status, parser version, and
normalized output. Ensure sensitive headers, credentials, cookies, and secret
fields are redacted or excluded before long-term storage.

**Failed options.** Deleting malformed input, storing authentication material for
convenience, and equating an absent normalized row with an absent delivery were
rejected.

**Established cause.** Parsing and receipt are different facts. A parser cannot
reconstruct an input that was never retained safely.

**Solution.** Create a safe raw receipt record first, then attempt
normalization. Preserve the relationship between the raw record and any
normalized observation; represent partial, invalid, and parse-error outcomes
explicitly.

**Verification.** Tests should cover valid, partial, malformed, unknown, and
credential-bearing requests, including proof that protected material is absent
from retained records.

**Current status.** The source reference documents this pattern but has no
database writer or live raw store.

**Recommendations.** Treat raw retention as evidence custody: define redaction,
retention, access, and deletion rules before collecting live data.

**History.** This pattern was retained because it made later parser and protocol
investigation possible without silently erasing a delivery event.

## 4. Why were an HTTP redirect and a station identity treated as separate
problems?

**Question.** Can a failed embedded send be diagnosed as one generic
authentication error?

**Context.** Historical cases included both path canonicalization before the
application and an identity mismatch after authentication reached the backend.

**Symptoms.** One case produced an HTTP redirect for a no-slash ingest path.
Another created a receipt record but rejected the message because a protocol
identity field did not match the configured value.

**Diagnostics.** For path behavior, check both accepted path variants with
redirects disabled and inspect status and `Location` behavior. For identity,
compare only the explicitly agreed wire identity fields after authentication;
do not substitute a source address, browser-like user agent, or a visually
similar hardware label.

**Failed options.** Assuming a device follows redirects, identifying it by
address, treating a hardware identifier as automatically interchangeable with a
wire identifier, or blaming the password for every rejection were rejected.

**Established cause.** The redirect occurred at path canonicalization before the
application. The identity case came from a prefix/form mismatch between the
configured identity and the value on the wire, not from a password failure.

**Solution.** Normalize accepted legacy path variants internally without making
the device follow a redirect. Define station identity from the actual protocol
fields and store the complete protocol form required for comparison.

**Verification.** Regression checks cover both paths without redirects and each
identity-field mismatch independently. A successful normalized reading must be
linked to an authenticated, valid receipt record.

**Current status.** The public tree includes neither a live route nor a real
station identity. These are reusable diagnostic lessons, not exposed service
details.

**Recommendations.** Diagnose by layer: transport, HTTP path, authentication,
identity, parsing, and normalization. Change one variable at a time.

**History.** Separating these cases avoided changing authentication or database
code for a request that had not yet reached the relevant layer.

## 5. Why did ordinary HTTPS success not prove compatibility with an ESP8266?

**Question.** If a browser and a command-line client can reach HTTPS, is an
embedded station necessarily compatible?

**Context.** A constrained ESP8266-class client failed before HTTP against one
TLS frontend while ordinary desktop clients succeeded.

**Symptoms.** The device reported a connection failure; no new HTTP receipt or
application log entry appeared. Changing parser, authentication, or database
code could not affect the outcome.

**Diagnostics.** Separate pre-HTTP TLS behavior from application behavior.
Inspect the negotiated TLS version, certificate validation, maximum-fragment
negotiation, and actual incoming handshake-record boundaries. Compare a physical
device acceptance through a controlled compatible gateway.

**Failed options.** Browser-only checks, a successful ordinary HTTP request,
assuming that the maximum-fragment extension alone guarantees record sizing, and
changing backend logic before a request exists were rejected.

**Established cause.** The historic evidence supported a high-confidence
pre-HTTP TLS compatibility problem: the direct frontend did not provide the
record behavior required by the constrained client. The device did not expose a
low-level failure code, so the conclusion remains evidence-bounded rather than a
universal claim about all ESP8266 firmware.

**Solution.** Place a controlled TLS gateway in front of the backend. Its
accepted configuration was limited to the needed TLS version, compatible
fragment/record behavior, internal path handling, strict request guards, and
verified upstream TLS; it did not become an application parser or data queue.

**Verification.** The historical acceptance required desktop TLS inspection,
packet-level record measurement, and a physical device handshake plus response
acknowledgement. A synthetic POST alone was insufficient.

**Current status.** The public reference contains no gateway configuration or
live transport endpoint. It records only the decision method and the limitation
of treating desktop TLS as device evidence.

**Recommendations.** Re-run the physical and packet-level checks after a
certificate, chain, TLS-library, proxy, or gateway change. Prefer future device
firmware that validates server identity rather than disabling that validation.

**History.** The gateway was a bounded transport adaptation for a constrained
client, not a claim that shared hosting, browsers, or all ESP8266 deployments
are defective.

## 6. How should time, duplicates, gaps, and completeness be represented?

**Question.** Can receipt time stand in for measurement time, and does a missing
point explain an outage?

**Context.** Portal Air distinguishes a source observation time, server receipt
or fetch time, and any publication/model time. Delivery attempts and normalized
observations are also distinct.

**Symptoms.** Delayed or repeated delivery can create misleading timestamps or
duplicate rows. A chart can falsely draw a continuous line across an absence.
A gap can tempt an operator to infer power, network, sensor, or server failure.

**Diagnostics.** Preserve each known time field separately; use `null` when a
true observation time is unknown. Retain delivery evidence and deterministic
identity so repeated delivery is visible without becoming an indistinguishable
second observation. Compute cadence completeness separately from endpoint
availability and channel completeness.

**Failed options.** Replacing observation time with receipt time, rendering an
absence as zero, bridging long gaps in a chart, and assigning a cause from the
gap alone were rejected.

**Established cause.** Timing, delivery, normalization, and source provenance
describe different facts. A data gap establishes only that expected data was not
received or represented in the chosen model; it does not establish why.

**Solution.** Preserve timing semantics, model expected event cadence explicitly,
render declared or sufficiently long gaps as breaks, and record source-specific
status such as current, stale, no data, source unavailable, and error without
collapsing them.

**Verification.** Test delayed delivery, duplicate identity, missing events,
partial channels, empty denominators, window boundaries, and chart gap behavior.

**Current status.** The reference reader is receipt-oriented. Where it cannot
know a source observation time, a future public projection must leave
`observed_at_utc` as `null` rather than invent one.

**Recommendations.** Fix the expected interval deliberately after observation
and record its calibration scope. Do not silently carry one device's cadence or
time semantics to another source.

**History.** The project retained event-cadence analysis as a data-quality model,
not as a diagnosis of the physical cause of every absence.

## 7. How can external WEATHER sources be shown without pretending they are
local measurements?

**Question.** Can an airport report, a crowdsourced sensor, an aggregation
service, and a forecast be merged into one local weather value?

**Context.** Historical research and bounded provider work considered an
airport-METAR observation lane, Meteostat, Narodmon, and Open-Meteo alongside
on-site PM data.

**Symptoms.** Multiple providers may all expose temperature or wind fields, but
their location, measurement exposure, source time, revision rules, upstream, and
legal terms can differ. Two APIs can also redistribute the same upstream report.

**Diagnostics.** Record source class, provider/source identity, observation
time, receipt/fetch time, freshness, field units, missing fields, upstream
relationship, and display/retention terms. Qualify a crowdsourced source before
treating it as a dependable comparison point.

**Failed options.** Calling an airport observation citywide truth, relabelling a
model or forecast as a physical observation, fusing wind speed from one source
with direction from another, retrying a policy-blocked provider route, or
assuming that a visible community sensor is qualified were rejected.

**Established cause.** Values with the same label can represent different
physical and computational phenomena. In one historic Meteostat probe, a single
HTTP 451 response established the responder's stated access/compliance outcome,
not an independently proven geographic, legal, or infrastructure root cause.

**Solution.** Keep the airport-METAR lane as a separate external-observation
context; keep Open-Meteo in a `MODEL`/`FORECAST` context; keep prospective
Narodmon data as `CROWDSOURCED_OBSERVATION` only after secure access, terms, and
qualification; and keep policy-blocked Meteostat live collection disabled until
a lawful, supported path is independently approved.

**Verification.** A provider needs fixture tests, bounded request accounting,
safe raw/health retention, source-time validation, and an isolated shadow lane
before any production use. A successful request does not itself prove public
display rights or representativeness.

**Current status.** This public source reference implements no provider,
polling, weather store, or map. It carries no external observations. Historical
provider cases are retained as provenance and control lessons only.

**Recommendations.** Introduce every provider through the sequence: research,
offline fixture test, bounded live probe, shadow qualification, then a separate
production decision. Do not use a proxy or other circumvention to evade an
access restriction.

**History.** The historical record includes a bounded airport-observation lane,
a deferred Meteostat live route after HTTP 451, changing Narodmon access evidence
that still required operator/provider terms and authorization, and an Open-Meteo
model/forecast classification.

## 8. Why can Linux/systemd deployment fail even when code and unit syntax look
correct?

**Question.** Is a local test or a successful unit-file syntax check enough to
prove a scheduled service works on Linux?

**Context.** A private external-data worker had two separate operational
failures: one around a transient runtime namespace and another caused by line
endings in an executable wrapper.

**Symptoms.** One service failed before useful work because it expected an
unnecessary runtime path. Another failed to execute even though the script was
present and its unit syntax was valid.

**Diagnostics.** Inspect the service result class, installed file bytes,
shebang, line endings, executable bit, ownership, sandbox paths, and actual
scheduled execution. Test the installed artifact rather than only the source
tree.

**Failed options.** Treating application code as the only possible failure,
relying only on unit syntax validation, retaining an unnecessary runtime
directory dependency, or assuming a Windows-edited shell script is executable
on Linux were rejected.

**Established cause.** The first failure came from a namespace/path dependency
not needed by the worker. The second came from CRLF bytes in a shell shebang,
which changed the interpreter name at execution time.

**Solution.** Remove the unnecessary runtime dependency, enforce LF packaging
checks, verify installed bytes and executable metadata, and require one real
bounded service execution in addition to offline tests.

**Verification.** The namespace correction was verified by a bounded no-network
service execution. The expired-wrapper correction was later verified through
installed-byte checks and real service execution. Provider work stayed isolated;
containers were not a required solution.

**Current status.** The public reference has no systemd unit, container image,
or deployment artifact. No evidence establishes that a container would solve the
historical packaging problem.

**Recommendations.** Choose a container only after it solves a concrete
operational requirement. Regardless of packaging style, test the final Linux
artifact, its permissions, line endings, isolation, and rollback behavior.

**History.** The case is retained because it distinguishes application logic
from packaging and service-manager failures without publishing an operational
unit file.

## 9. What does a dashboard, API, or map acceptance actually prove?

**Question.** Does a successful HTTP probe establish that a public browser
application is usable?

**Context.** Historical dashboard and map work separated server-to-server/API
checks from user-visible rendering and protected ingest continuity.

**Symptoms.** A route can return a technical success while a browser receives
different content, an authentication challenge, a blocked asset, stale data, or
an incomplete render. A chart can also misrepresent missing data.

**Diagnostics.** Verify the data contract and same-origin API separately. Then
use an ordinary installed browser with a fresh task-owned profile, no user-agent
override, injected cookies, task authentication headers, proxy, or TLS bypass.
Confirm normal redirects, expected application content, critical same-origin
requests, and gap rendering.

**Failed options.** Treating a command-line HTTP success, a special test user
agent, a fixture-only browser run, or a synthetic post as public user acceptance
were rejected.

**Established cause.** Technical transport success and user-visible browser
acceptance exercise different layers and must remain separate evidence classes.

**Solution.** Keep browser clients on reviewed same-origin projections; expose
only the data needed by the UI; preserve provenance, time, freshness, and gap
semantics; and accept a public UI only after ordinary-browser evidence.

**Verification.** Historical UI work used separate API, privacy, browser, and
post-change ingest-continuity gates. Each gate recorded what it did and did not
prove.

**Current status.** The public reference includes no HTTP application, browser
assets, map runtime, coordinates, or public API. It cannot establish browser
acceptance.

**Recommendations.** Do not add a frontend or map library merely because a data
reader exists. Define the public projection, privacy policy, terms, security
headers, browser acceptance, and rollback boundary first.

**History.** The distinction was preserved after cases in which technical probes
and browser behavior diverged.

## 10. What security lessons apply to diagnostics and secrets?

**Question.** Is it safe to inspect a masked password field or log a secret
temporarily for troubleshooting?

**Context.** Engineering diagnostics can cross the same privacy boundary as the
application itself.

**Symptoms.** A value may be visually masked in a browser interface while an
automation or accessibility layer can still read it. Raw request captures can
also contain authentication material.

**Diagnostics.** Check presence, schema, boolean state, or a protected digest
instead of a secret value. Review reports, terminal output, fixtures, browser
profiles, screenshots, logs, and raw retention paths for disclosure risk.

**Failed options.** Printing credentials "just to verify them", storing an
authorization header in raw evidence, treating Base64 as encryption, or assuming
that visual password masking protects debug APIs were rejected.

**Established cause.** Masking affects presentation, not necessarily programmatic
access. If a credential value is exposed to an unapproved diagnostic surface, it
must be treated as disclosed.

**Solution.** Keep secrets outside Git and public documentation; redact before
retention; use least privilege; keep provider secrets out of URLs and command
lines; and rotate a credential after actual disclosure.

**Verification.** Publication review combines automated scanning with manual
inspection. A clean scan supports review but cannot prove that all secret
handling is safe.

**Current status.** The public source contains no production access material.
Its publication-audit tool is a defense-in-depth scanner, not a credential
management system.

**Recommendations.** Design diagnostics to report categories and safe metadata,
not values. Report a suspected disclosure through a private channel without
copying the sensitive material into an issue.

**History.** A diagnostic-accessibility lesson was retained because it changed
how credential exposure is classified even when a value was not committed.

## 11. Why is a backup not equivalent to disaster recovery?

**Question.** Does a successful dump or archive prove that data can be restored?

**Context.** Historic recovery work distinguished creation of a backup artifact,
an isolated import, logical comparison, off-host custody, and bare-environment
recovery. At an earlier checkpoint, a fresh-dump database restore was recorded
as `FAILED`: the available isolated targets did not establish a logical import.
Later evidence established a separate isolated import and bounded comparison.

**Symptoms.** A dump can have a plausible size and digest yet fail to import,
restore only part of the expected data, depend on unavailable tooling, or be
unusable outside a particular host/profile.

**Diagnostics.** Restore into a new disposable target. Check schema, row-level
or logical identity, representative data relationships, indexes/constraints,
time ranges, integrity, and the ability to use the restored result without
touching production.

**Failed options.** Calling backup creation a completed recovery test, restoring
over production, accepting a provider statement without evidence, or equating a
same-host operational snapshot with full disaster recovery were rejected.

**Established cause.** Backup generation and recovery are separate capabilities.
The earlier `FAILED` result remains part of the historical record. It was
superseded only for the later isolated database-import and comparison scope; it
did not prove off-host custody, independent-machine recovery, protected-secret
recovery, or full reprovisioning.

**Solution.** Keep a bounded, isolated restore rehearsal in the acceptance path
and state its exact scope. Protect recovery material and avoid destructive
operations during verification.

**Verification.** A meaningful rehearsal records the source artifact identity,
isolated target, comparison method, result, and what remains outside the test.

**Current status.** This public reference carries no dump, restore script, or
recovery artifact. It makes no disaster-recovery readiness claim.

**Recommendations.** Define retention, encryption/key custody, off-host
handling, recovery objectives, and a recurring isolated restore/round-trip
exercise before declaring DR readiness.

**History.** The historic status changed as stronger restore evidence arrived.
The retained lesson is to preserve both the earlier `FAILED` outcome and the
precise, narrower scope of its later supersession.

## 12. How should this material be reused or published safely?

**Question.** What is safe to copy into another monitoring project, and what
must remain outside public history?

**Context.** Portal Air's useful output is primarily a sequence of engineering
questions, failure boundaries, and validation methods—not a universal station
product or a ready-made operations stack.

**Symptoms.** Copying a deployment recipe, a production address, a raw capture,
or a provider decision into a new environment can create a privacy, security,
or correctness failure.

**Diagnostics.** Classify every candidate artifact as public source, synthetic
fixture, private configuration, raw evidence, credential, deployment custody,
or owner decision. Check whether its license and redistribution status are
actually granted.

**Failed options.** Copying internal Git history, treating an old public claim
as current fact, publishing a realistic substitute location, using provider
content without terms review, or assuming that public availability grants a
software license were rejected.

**Established cause.** Public documentation needs a different evidence and
privacy boundary from internal operational history. A clean public Git root is
not a substitute for review, but it prevents inherited private history from
silently travelling with a source snapshot.

**Solution.** Reuse the method: capture the real device contract, build
raw-first ingest, test constrained transport physically, keep source provenance
separate, introduce providers through a shadow process, rehearse recovery, and
publish only sanitized reviewed artifacts.

**Verification.** Before sharing, run the publication audit and local tests,
review all configuration samples and documents manually, check links and path
allowlists, and inspect the final staged diff rather than a working directory
alone.

**Current status.** The original immutable published tag remains unchanged.
This successor documentation is an additive recovery candidate until separately
reviewed and published; no license grant is implied by repository access.

**Recommendations.** Use [REUSE_GUIDE.md](REUSE_GUIDE.md) as the practical
checklist. Keep a new project's sources, evidence, secrets, licensing, and
production decisions under its own review process.

**History.** The first public narrative contained broader lessons that were
removed during sanitization. This successor restores their subject matter while
preserving the later privacy boundary.

## 13. Why is a browser demonstration not proof that a full Core is
browser-ready?

**Question.** If a browser can load one module through a test adapter, does that
prove that the complete Foundation/Core architecture is ready to run in a
browser?

**Context.** A dated feasibility review separated a copied browser-facing
reference module from a fuller Core that also depended on Node-bound filesystem,
path, URL, and configuration work.

**Symptoms.** A small module can load with copied reference data and a synthetic
context while the full import graph cannot load, provision itself, or complete a
lifecycle in a browser. Separately passing Node-side tests can obscure that
boundary.

**Diagnostics.** Identify the exact module, import graph, data adapter,
configuration path, and lifecycle that were exercised. Test browser execution
and Node execution as different environments. Check declared schemas and the
runtime validator independently before treating them as one contract.

**Failed options.** Calling a synthetic adapter spike a full Core integration,
equating a Node suite with browser readiness, or treating one imported reference
module as proof of browser-safe provisioning were rejected.

**Established cause.** Browser feasibility has a scope. A copied module can be
browser-feasible while a full Node-oriented Core remains not browser-ready.
Neither result should be promoted beyond the exact topology exercised.

**Solution.** Design a deliberate boundary between Node-side provisioning and
browser execution. Define browser-safe descriptors, configuration, assets, and
host authority before attempting a full lifecycle.

**Verification.** Full browser readiness requires evidence from the actual Core
topology in an ordinary browser. Module, fixture, and synthetic-adapter results
remain useful but narrower evidence classes.

**Current status.** This public reference includes neither a Foundation runtime
nor a browser application. It makes no claim about current browser compatibility
of an external system.

**History.** The feasibility case remained `PARTIAL` / `BLOCKED`, rather than
being promoted from a limited browser success to a full-Core pass.

## 14. Why must a nullable public field be present as `null` rather than absent?

**Question.** Is a missing field equivalent to a field whose known value is
explicitly `null`?

**Context.** A local contract guard initially treated an absent observation-time
key like an explicitly present `null` value. Related reviews also showed why a
declared schema and a runtime validator need their own evidence.

**Symptoms.** A positive fixture can pass even when a required public field was
omitted, typed incorrectly, or replaced with an unexpected container. Consumers
then receive an ambiguous contract while a self-check appears green.

**Diagnostics.** Test key presence, allowed nullability, exact scalar/container
type, and permitted field set separately. Include negative fixtures for an
absent key, explicit `null`, unexpected nested object, and unknown field where
the public contract forbids it.

**Failed options.** Using a lookup whose fallback value makes absent and `null`
indistinguishable, checking only the happy-path fixture, or assuming that a
schema declaration automatically proves runtime validation were rejected.

**Established cause.** Nullable means that a present value may be `null`; it
does not make the field optional. Schema review, parser behavior, serialization,
and consumer validation each need an explicit boundary.

**Solution.** Use an exact public allowlist and fail closed on absent required
keys, invalid types, or forbidden structure. Preserve `null` where the source
does not provide a real observation time instead of inventing one.

**Verification.** A corrected local fixture guard can protect its selected
source path. PHP endpoint, browser, deployment, and production evidence remain
separate acceptance scopes.

**Current status.** The reference reader documents a receipt-oriented contract;
it exposes no public endpoint from this tree.

**History.** The narrow diagnostic defect was corrected and independently
reviewed locally without turning that outcome into a runtime-health claim.

## 15. Why are anonymous serialization and honest time labels one public
contract problem?

**Question.** Can a dashboard remove an obvious identifier yet still disclose a
stable identity or misrepresent when a measurement occurred?

**Context.** A bounded source-contract review considered public station and
cadence DTOs together with a receipt-derived “last received” field and its UI
wording.

**Symptoms.** Identity can survive in nested metadata, cadence fields, raw
linkage, stable replacement values, or an error shape. A label such as “last
measurement” can also turn a server receipt into an invented observation time.

**Diagnostics.** Review every short-window, long-window, cadence, error, and
rendering path. Use an exact public-field allowlist; try identity-bearing values
in direct and nested locations; and trace every visible time label back to its
source fact.

**Failed options.** Removing only one visible identifier, replacing it with a
stable anonymous-looking token, trusting a scalar field to stay scalar, or
labelling receipt time as measurement time were rejected.

**Established cause.** Privacy and time semantics are both serialization
boundaries. A useful public projection needs neither a station identity nor a
fictional observation timestamp.

**Solution.** Emit only a generic display label and the minimum reviewed status
or receipt fields. Validate nested structures fail-closed, label receipt time as
receipt, and leave an unavailable observation time explicitly unknown.

**Verification.** Negative source and rendering fixtures can check direct and
nested disclosure paths. They do not prove that an endpoint was deployed or that
an ordinary browser currently serves the reviewed DTO.

**Current status.** This source reference has no dashboard endpoint or browser
assets. The lesson is a public-contract design rule, not a report about a live
dashboard.

**History.** The associated remediation was accepted only at bounded local
source/fixture scope.

## 16. How should a WEATHER reader handle store drift and unreliable fixture
cleanup?

**Question.** Can a read-only weather projection assume that a private store
will always have the schema and timing behavior expected by its tests?

**Context.** Local WEATHER work found two independent maintenance risks: a
reader depended on a private normalized-store shape without an explicit version
handshake, and a fixture suite could mix wall-clock completion time with fixed
test time or leave a temporary store open after a failure.

**Symptoms.** A reader can query an old, future, incomplete, or differently
shaped store. A test can pass or fail according to timing coincidence, and a
temporary SQLite file can remain locked during cleanup. Neither symptom proves a
provider or production failure.

**Diagnostics.** Open the private store read-only; verify its supported version,
required table, and required projection fields before querying; and expose only
a generic public source error on incompatibility. In tests, inject the scheduler
and completion clocks separately, block network access, and close stores before
temporary-directory removal.

**Failed options.** Silently adapting an unknown store, letting private schema
or path details reach a public error, treating a local suite as provider health,
or changing a runtime provider merely to make fixtures green were rejected.

**Established cause.** Store compatibility and fixture determinism are distinct
contracts. A reliable local regression needs explicit versioning, cleanup, and
time ownership; it does not establish the health of a live collector.

**Solution.** Fail closed on unsupported store shapes, preserve the reader as a
read-only projection, and make test clocks and cleanup order deliberate.

**Verification.** Writer-shaped temporary stores and fail-closed fixtures can
exercise the boundary locally. Provider polling, deployed SQLite custody,
Linux/service behavior, and ordinary-browser acceptance need their own evidence.

**Current status.** The public reference implements no WEATHER provider,
polling, store, or map runtime.

**History.** The reported repairs concerned local source and fixtures only; they
were not an external-service health result.

## 17. What does a bounded check not establish about data, hosting, or
recovery?

**Question.** Can a source fixture, selected static-asset match, successful
public read, or historical package check establish that a deployment, database,
ingest path, or recovery plan is healthy?

**Context.** Dated reviews produced several different evidence classes: local
source and PHP fixtures, a limited served-public-projection observation, selected
static-asset comparisons, a historical package with an unreproducible canonical
asset manifest, and an unavailable current database read boundary.

**Symptoms.** A technical success can be described as full deployment parity;
one visible projection can be mistaken for natural authenticated ingest; or a
working-tree line-ending difference can be confused with an artifact-integrity
defect. A historical package can remain available even after it is no longer a
reproducible deployment authority.

**Diagnostics.** Write a claim-to-evidence matrix. Attribute source tests to
their fixtures, selected asset equality to those exact assets, and a public read
to the response observed at that time. Obtain separately authorized aggregate
database, natural-ingest, hosting/edge, and isolated-restore evidence before
making those claims. Compare canonical artifact bytes with their manifest rather
than only a checkout representation.

**Failed options.** Treating an HTTP success as database or ingest proof,
treating selected assets as full deployment parity, repairing old manifest bytes
merely to force a check green, or calling an inaccessible data boundary healthy
were rejected.

**Established cause.** Evidence is claim-specific. A limited observation can be
valuable without proving the surrounding system, and an unreproducible
historical package should be retained as history but retired as a future
deployment authority.

**Solution.** Keep evidence labels narrow, fail closed where an artifact or
access boundary cannot support the intended claim, and use a separately reviewed
successor for any new deployment or recovery exercise.

**Verification.** Record the exact scope, date, inputs, and exclusions for each
check. Do not turn a local fixture, browser harness, provider observation, or
isolated restore into a broader acceptance class.

**Current status.** This reference has no database, ingest endpoint, hosting
configuration, asset package, or recovery artifact. It makes no current health
claim about any of them.

**History.** The retained cases teach how to preserve useful limited evidence
without concealing the still-unverified boundaries around it.
