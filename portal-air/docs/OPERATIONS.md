# Operations boundary

This source is safe to inspect and test locally with synthetic fixtures. It is
not an operations runbook. In particular, it does not contain service units,
network listener configuration, host paths, backup destinations, log custody,
source endpoints, secrets, users, certificate configuration, or production
health evidence.

Before any real deployment, define a separate least-privilege operating model:
secret provisioning, source authorization, private configuration custody,
source read permissions, logging/redaction, monitoring, retention, backup and
restore rehearsal, update handling and an incident process.
