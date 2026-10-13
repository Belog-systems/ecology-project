# Local worktree recovery

This document concerns only a local sanitized candidate. It does not authorize
changes to any deployment or internal evidence.

If the candidate worktree becomes unclear:

1. Stop before deleting, resetting or overwriting files.
2. Record `git status --short --branch`, `git log --oneline --decorate -n 5`,
   `git remote -v`, and `git ls-files` without exposing credentials.
3. Compare the tracked file list with `docs/review/CANDIDATE_MANIFEST.md`.
4. Re-run the audit and local tests.
5. If the tree may contain sensitive material, do not push it; rebuild a fresh
   candidate by copying only reviewed files.

Do not use internal history rewriting or force-push as a recovery technique.
