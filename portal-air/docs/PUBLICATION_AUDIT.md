# Publication audit

Before sharing a tree or creating its first Git commit:

1. Confirm there is no inherited `.git` directory, submodule or remote.
2. Run the scanner:
   ```powershell
   python tools/publication_audit.py . --fail-on P1
   python -m unittest tools/tests/test_publication_audit.py -v
   ```
3. Manually review configuration samples, location-sensitive logic, host/path
   references, documentation claims, third-party notices and generated files.
4. Require `P0=0` and `P1=0`; a clean scanner is not a replacement for review.
5. Initialize a new repository only after the candidate is approved. Inspect
   `git status --ignored`, `git ls-files`, `git log --all` and `git remote -v`.

The generated `docs/review/CANDIDATE_MANIFEST.md` lists the reviewed final path
set and SHA-256 snapshot after the LF checkout policy is enforced. It
intentionally does not hash itself, because a file cannot contain a stable hash
of its own final bytes. The clean commit/tag and `git ls-files` are the
authoritative integrity boundary, and a fresh clone reruns the safe checks.
The candidate manifest must not name a source-project commit, repository path,
remote or operator identity: those audit facts remain outside this candidate.

Never print matched values in a report. Record only paths, rule categories,
severity counts and remediation decisions.
