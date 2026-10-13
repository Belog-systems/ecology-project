# Privacy boundary

This baseline deliberately excludes exact own-station coordinates, persistent
approximation state, external-marker coordinates, raw station packets, live
measurements, production responses, browser profiles, account data and private
operational topology.

The source reference carries no location projection, map or own-station marker.
It does not recreate, approximate, infer, or substitute a production point. A
future deployment must define and independently review its own location-
projection policy before rendering any map marker.

PM receipt time is not an observation time. When a future public API has no true
source observation time, its `observed_at_utc` must remain `null`; its
`received_at_utc` describes only receipt.
