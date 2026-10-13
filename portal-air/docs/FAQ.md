# FAQ

## Is this the production repository?

No. It is a curated sanitized reference with new clean history.

## Why are there no coordinates or map markers?

Location privacy is protected. This baseline omits the map and location runtime
rather than carrying a real point or inventing a substitute.

## Why must a future PM API use `observed_at_utc: null`?

The retained reader does not assume a true measurement time when only receipt
time is available. A future API must preserve that distinction rather than
fabricating a timestamp.

## Can I deploy it as-is?

No. Deployment is a separate reviewed task and this repository intentionally
omits the necessary infrastructure and custody decisions.

## Is external WEATHER a local PM measurement?

No. It is future-only in this candidate. Any later integration must preserve its
separate provenance and freshness semantics.
