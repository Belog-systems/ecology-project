# Current state

The immutable sanitized Portal Air V1 baseline is published in this repository
under its existing immutable tag. Later successor documentation is also
published on the public branch, but is not included in that tag and does not
alter it.

The Portal Air content was curated from a clean public-safe source boundary and
is not an export of an internal repository. Neither the baseline nor its
successor documentation is a deployment, a runtime archive, or evidence of
current production health.

The reference preserves a narrow V1 PM-source-reader boundary: TLS hostname
validation over an explicitly configured address, normalized PM projection,
receipt-time semantics and explicit missing-data behavior. It intentionally
excludes every production identity, location, source address, operational path,
raw record, deployment artifact, browser application, map runtime and external
WEATHER integration.

Any future successor change needs independent review, a fresh final-tree
privacy/security check, link and local-test checks, and a new explicit release
decision. The existing baseline tag must remain unchanged. A project license
remains an owner decision.

For a future derivative, the reference does not establish device measurement
time, durable replay/queue behavior, complete device server-authentication
behavior, or full disaster-recovery readiness; those remain separate reviewed
workstreams.
