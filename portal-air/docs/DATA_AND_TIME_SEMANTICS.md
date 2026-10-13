# Data and time semantics

## PM

The retained reader keeps the source dashboard receipt timestamp as
`timestamp_utc`. A future public API may project it as `received_at_utc`, but it
does **not** invent a measurement timestamp. When the true source observation
time is not known, that future API's `observed_at_utc` must be `null`.

## External WEATHER

External WEATHER work is not implemented or configured here. If a future
separately authorized integration is introduced, it must retain a true source
`observed_at_utc` separately from any `received_at_utc`; the latter must not be
substituted for the former. It must remain separate from on-site PM data.

## History and missing data

PM history can include explicit missing-receipt intervals. Any future client
must render a break for explicit gaps and sufficiently long intervals; it must
not interpolate values or draw a continuous line through absence of data.

## Status

A future public application must keep `CURRENT`, `STALE`, `NO_DATA`,
`SOURCE_UNAVAILABLE`, and `ERROR` distinct. The source reader does not itself
emit a public status document. A lack of data does not establish a cause such as
network, power, hardware or server failure.
