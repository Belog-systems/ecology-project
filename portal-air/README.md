# Portal Air V1 sanitized reference

**Status:** published, immutable sanitized baseline plus an untagged
documentation-recovery successor candidate. The baseline is a public source
reference, not a production deployment package. Publication does not select a
software license or grant reuse rights beyond those explicitly stated in
[`LICENSE_STATUS.md`](LICENSE_STATUS.md).

This is a curated reference tree, not an export of the internal Portal Air
repository. It preserves selected V1 PM-source-reading semantics and the
documentation needed to review those semantics without carrying production data,
operational evidence, internal Git history, credentials, exact coordinates, or
deployment/rollback custody.

The immutable baseline tag remains unchanged. Later documentation may explain
sanitized historic engineering lessons, but it must not be read as a change to
the tagged baseline, evidence of a current runtime, or a substitute for a
separately reviewed deployment.

## Scope

- `portal_air_v1/` contains a sanitized, read-only PM-source reference.
- `docs/` records scope, privacy, security, semantics, limitations, testing and
  future boundaries.
- `tools/publication_audit.py` is a dependency-free disclosure scanner and is
  included with tests.

The source is intentionally **not** an installer or a production-ready package.
Any deployment requires a separately authorized review of secrets, source
contracts, ingress, location privacy, backup/restore, monitoring and ordinary
browser acceptance. This reference implements no external WEATHER provider,
map runtime, frontend, packet ingest, database writer, or station control.

## Safe local checks

```powershell
python -m unittest discover -s portal_air_v1/tests -v
python -m unittest tools/tests/test_publication_audit.py -v
python tools/publication_audit.py . --fail-on P1
```

See [docs/INDEX.md](docs/INDEX.md) before using this material. For the restored
sanitized engineering history, read [docs/FAQ.md](docs/FAQ.md),
[docs/INCIDENT_LESSONS.md](docs/INCIDENT_LESSONS.md), and
[docs/REUSE_GUIDE.md](docs/REUSE_GUIDE.md).
