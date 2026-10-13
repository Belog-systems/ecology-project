# Portal Air V1 PM source reference

This directory contains the reviewed, read-only PM dashboard projection retained
in the frozen sanitized baseline. It is a source-level reference, not a
deployable application or a production configuration.

## Preserved behavior

- the source reader connects only to an explicitly configured address while TLS
  validates the configured hostname;
- a future public projection may retain only normalized PM, temperature,
  humidity and pressure fields;
- source station identity is structurally validated without embedding a real
  station identifier;
- PM data remains receipt-oriented: a receipt timestamp is not mislabelled as a
  source observation timestamp; and
- declared missing-receipt intervals remain explicit for clients to render as
  breaks rather than fabricated continuous data.

## Deliberately absent

- all production hostnames, addresses, identities, credentials, raw readings,
  deployment topology and operational paths;
- an HTTP server, browser UI, map, coordinates, persistent location state and
  map-provider runtime configuration;
- external WEATHER implementation, provider binding, polling, data store or
  API; and
- ingest, database writes, provider registration, station control and firmware
  behavior.

`config.example.json` is a structural, non-routable documentation example only;
it contains no live hostname, address, identity, credential or filesystem path.
The unit tests use only synthetic responses and documentation-network addresses.
