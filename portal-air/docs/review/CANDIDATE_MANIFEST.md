# Candidate manifest

```text
MANIFEST_SCHEMA=portal-air-v1-candidate-manifest/v2
ASSEMBLY_MODE=EXPLICIT_REVIEWED_PATH_COPY_PLUS_REVIEWED_LF_POLICY
SOURCE_REVIEW=LOCAL_CURATED_STAGING_TREE_PLUS_REVIEWED_LF_POLICY
FINALIZED_AT_UTC=2026-10-12T04:51:29Z
GIT_HISTORY=NEW_CLEAN_HISTORY_ONLY
LINE_ENDINGS=LF_ENFORCED_BY_GITATTRIBUTES
HASHED_FILE_COUNT=33
HASHED_TREE_SHA256=3f1c8973a6fe18942fe31e2b23619814bcdba91f3ffe4a39578860afc9e49581
SELF_HASH=OMITTED_TO_AVOID_CIRCULAR_MANIFEST
REMOTE=NONE
LICENSE_STATUS=OWNER_DECISION_REQUIRED
PRODUCTION_MUTATION=NOT_RUN
```

## Inclusion rule

Every file listed below is in the reviewed final candidate. The source files
were copied through an explicit reviewed-path list, not a directory copy. The
small `.gitattributes` LF policy was then added and reviewed locally to make
fresh-clone content deterministic. The initial assembly had no inherited
`.git` directory; this candidate now has its own new clean Git history only.

The `.gitattributes` entry is part of this snapshot and enforces LF checkout
content. This avoids platform-specific line-ending drift during fresh-clone
verification.

## Exclusion classes

- Git history, remotes and configuration from the source project; no inherited
  `.git` tree.
- Credentials, private configuration, environment files, certificates, keys,
  cookies, authorization material, runtime databases, logs and archives.
- Production hostnames, addresses, accounts, topology, service files, backup
  paths, deployment/rollback/recovery custody and raw evidence.
- Exact or approximate coordinate/location state, station identity values, raw
  observations, browser profiles, screenshots, caches and temporary artifacts.
- Browser UI, map/tile dependencies, external WEATHER implementation and
  provider polling; they remain future-only boundaries.

## SHA-256 file list

| Path | SHA-256 |
|---|---|
| `.gitattributes` | `7a96c7563464d054bfcfea76330676ceb6517272d20adff983ce64af49bca553` |
| `.gitignore` | `94d25c33d409b3ba5d84513ac64ab81e44ff239fab485952d69692c4c61b0baa` |
| `CONTRIBUTING.md` | `71bbf0385c683d371448aa468d76411a8bcb7694e70b12606b9140678f5e64ff` |
| `LICENSE_STATUS.md` | `219a7490863178a84aa2f00898892ffb3ebde70bea68f6e5e514f3d9d5c612d6` |
| `PRIVACY.md` | `0b0f3efb8fa7b78f06b636381fa858e8037a5ab48ca04810c1f012143f883b5d` |
| `README.md` | `dac85b7b93586156fded1ada5b90f555a7ea797482ff0850cfcd7ad69227ff33` |
| `SECURITY.md` | `7df00843946acb268e5d08748240073cf078644fddfdcafdb0d82a06fa077e12` |
| `docs/ARCHITECTURE.md` | `19df7b7944f099a306d07c4a711aa65218ec152319e5dd8287550fddcb2ef35c` |
| `docs/BACKUP_AND_RESTORE.md` | `97a98257ab25005fa763d6e535a4a1de9f41c691f77fd8c4ef766e07dd0dfbd8` |
| `docs/CHANGE_REVERSAL_AND_RECOVERY_BOUNDARY.md` | `b51744065e6055424ed1ae5eeb5ac23374623ee5789cbef911ae6f65592a0003` |
| `docs/CURRENT_STATE.md` | `8d471471268309266d1c2400ee12b5db5c422225892b9512ceca4e58b669269d` |
| `docs/DATA_AND_TIME_SEMANTICS.md` | `e61b3fdc970ea113e8b3f85bdc2e5b7d7113d250cc2820105ca8ea947e0f2811` |
| `docs/DEPLOYMENT.md` | `3b47fd446e7b5c1f828dbf95bc4a37801a90aafb40ae14dc6a689454b629a262` |
| `docs/FAQ.md` | `5a9d7df39be83efdcf4b901f7a46aa26559d341f5cf4fe281c177f7a6ee859b4` |
| `docs/FUTURE_BOUNDARIES.md` | `31637d2792a677918a1e2f58fcb483bc55561f8560bc1a8f8e0f1fd399a9b90b` |
| `docs/INCIDENT_LESSONS.md` | `dc6fa24ed7faaa4b64f254a07221714ad00445d37fa99f7864ce35e3908c0f3a` |
| `docs/INDEX.md` | `6ab64fe362fed444493ba47bbf48336372af07640a0a86e2b65a24aca7144196` |
| `docs/LIMITATIONS.md` | `04f6a5cdf0bd7a7d3d81990be6e033568bc77eaebb82801be6428a84618ff458` |
| `docs/OPERATIONS.md` | `bfdd408c04b2e3dfc79bd9477e777e48eeb3c2c058513eb54dfdd283f51faa3f` |
| `docs/PRIVACY_AND_LOCATION.md` | `8b5404096af0fe843a3d760b7b92aa5ab42c9c851794c45d6e8f1cfbcd0bd0ad` |
| `docs/PUBLICATION_AUDIT.md` | `c3d8d044d26da17d287d4f03d92d0de66cd7cd617b01a7c053e56a76420d0de6` |
| `docs/ROADMAP.md` | `09a1a230c5b946d6688b586de96ee1f2b2d45f10cdb0a10c669254241f31abb8` |
| `docs/TESTING.md` | `b5eeb2ffb165fecba10362e3c0056c97c3eaf841b5a854aa764c8d205d955518` |
| `docs/TROUBLESHOOTING.md` | `c4979c79b75befbabceae0a1b9b6f42cce29795491e92e91111f66ed546e4929` |
| `docs/WORKTREE_RECOVERY.md` | `95fd53fb9738e53b85a019b41652c01860adb9f8096974b40773fd9362104023` |
| `portal_air_v1/README.md` | `c0ff63d7d6e2d1317b73a2e0a70d69b426dd4350cf0c9a4a636cc20dfb217557` |
| `portal_air_v1/__init__.py` | `b2cc3dd397244cab2defaa56ce2ee7e93446e81ea64cccf08f39d49b0b1ee2bc` |
| `portal_air_v1/config.example.json` | `ab3c5eea72c4806a4ae5309bd2a768f7f401164a0e9d2f93225df1da0c933caa` |
| `portal_air_v1/dashboard_source.py` | `cf804911bed0e6e232d54da0c0f8930392b5444e2d5438bdf849bb1548143c05` |
| `portal_air_v1/tests/__init__.py` | `92ef4904a1622f50a31db56e69c37b0bdcd128060979a1ffcad5a8924680f2cf` |
| `portal_air_v1/tests/test_dashboard_source.py` | `67c8fb10dc06860cfb5e3a6bfdca1b3120f6cf25d0047936889151824a7c1145` |
| `tools/publication_audit.py` | `98d596898316b7f0a8186a1b5f8bfc61a7fd8d9aa719dc623d8f800055578e25` |
| `tools/tests/test_publication_audit.py` | `b783bbb568389bb620920e0638a8a6faa775bb0d580ed1696a8babed2283ce81` |

The `HASHED_TREE_SHA256` value is SHA-256 of the UTF-8 concatenation of the
sorted lines `<file-sha256><two spaces><path><LF>` for the table entries only.
This manifest itself is intentionally excluded from that digest. Its final
bytes are covered by the clean Git commit/tag; fresh-clone checks validate the
tracked path set, object integrity, scanner and test suite.
