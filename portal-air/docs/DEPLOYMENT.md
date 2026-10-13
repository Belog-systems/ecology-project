# Deployment boundary

There are deliberately no deployment instructions in this repository.

The included source reader has no HTTP listener or deployment configuration. Do
not infer a safe public route, TLS setup, reverse proxy, process manager,
filesystem layout, credential store, source origin, database layout or location
policy from this material.

A self-hosted or production deployment requires its own approved change set,
security review, rollback plan, backup/restore rehearsal and ordinary-browser
acceptance. It must use local secrets through a secure out-of-band mechanism and
must never commit them to this repository.
