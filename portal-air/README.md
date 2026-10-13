# Portal Air V1 frozen sanitized baseline

**Status:** locally curated sanitized baseline. This repository is private-only
if it is published. No public-release decision or license grant is made by this
baseline.

This is a newly curated reference tree, not an export of the internal Portal Air
repository. It preserves selected V1 PM-source-reading semantics and the
documentation needed to review those semantics without carrying production data,
operational evidence, internal Git history, credentials, exact coordinates, or
deployment/rollback custody.

## Scope

- `portal_air_v1/` contains a sanitized, read-only PM-source reference.
- `docs/` records scope, privacy, security, semantics, limitations, testing and
  future boundaries.
- `tools/publication_audit.py` is a dependency-free disclosure scanner and is
  included with tests.

The source is intentionally **not** an installer or a production-ready package.
Any deployment requires a separately authorized review of secrets, source
contracts, ingress, location privacy, backup/restore, monitoring and ordinary
browser acceptance. External WEATHER, map rendering and frontend work remain
future-only boundaries in this baseline.

## Safe local checks

```powershell
python -m unittest discover -s portal_air_v1/tests -v
python -m unittest tools/tests/test_publication_audit.py -v
python tools/publication_audit.py . --fail-on P1
```

See [docs/INDEX.md](docs/INDEX.md) before using this material.
