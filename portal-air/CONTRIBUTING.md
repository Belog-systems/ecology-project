# Contributing

This is a frozen sanitized baseline, not an invitation to change a production
system. Contributions must preserve the following boundaries:

1. Do not add credentials, production configuration, raw observations, exact or
   approximate location data, personal data, screenshots, browser profiles,
   backup archives, deployment evidence, or internal Git metadata.
2. Do not represent receipt time as source observation time. If no true source
   observation time exists, keep `observed_at_utc` as `null`.
3. Do not add an external WEATHER integration, provider binding, source store or
   polling behavior under this frozen baseline.
4. Preserve explicit missing-data semantics; a future client must not bridge
   long or declared missing-data periods in a chart.
5. Run the documented tests and publication audit before proposing a change.
6. New providers, schema/ingest changes, a Module API, a frontend redesign,
   location handling, deployment automation, map-provider replacement, replay,
   firmware work, or public release need a separate reviewed decision.

Report potential disclosure privately as described in `SECURITY.md`; do not add
the suspected data to an issue or commit.
