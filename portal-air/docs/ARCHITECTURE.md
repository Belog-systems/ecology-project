# Sanitized reference architecture

```text
future application boundary
  -> optional same-origin read API
      -> retained PM dashboard reader (read only)
```

The diagram is a logical reference boundary, not production topology. It omits
all hostnames, addresses, ingress details, service accounts, source identities,
deployment paths and credentials.

The retained reader has no public HTTP listener or browser asset. A future
browser application must receive only a reviewed public projection; it must not
receive upstream addresses, source configuration, raw provider responses,
credentials or location state. This baseline contains no packet ingest, database
write, provider polling, station control, WEATHER source store or map runtime.

The source reader validates its source contract and pinned transport structure.
Any public listener, ingress, map provider, WEATHER source binding or deployment
configuration is outside this tree.
