# Security policy

## Reporting a disclosure

Do not publish credentials, raw data, exact coordinates, private configuration,
or a proof containing sensitive values. Use the repository host's private
security-report mechanism or a pre-agreed private owner channel.

State only the affected file/path, rule/category, impact and safe reproduction
steps. Redact all secret and location values.

## Scope boundary

This sanitized baseline contains no production access material and cannot
authorize access to a Portal Air environment. It must not be used to target an
unknown endpoint, host, account, service, or station.

## Verification before sharing

Run `python tools/publication_audit.py . --fail-on P1`, inspect the resulting
path/rule summary, review all configuration samples manually, and confirm the
tree contains no inherited `.git` history before first initialization.
