# Safe local troubleshooting

## A Python test fails

Use a supported Python version, run from the repository root, and ensure no
local file shadows the `portal_air_v1` package. The tests use synthetic source
documents and make no network request.

## The Node test fails

There is intentionally no frontend test in this source-only baseline. A future
frontend must add its own reviewed test and ordinary-browser acceptance.

## The publication scanner reports a finding

Treat P0/P1 as a publication stop. Remove or replace the material from the
candidate, then rerun the scanner and manual review. Do not paste a secret,
coordinate, raw data or protected path into a ticket to explain the finding.

## A derivative cannot start

This source-only baseline contains no listener or deployable server. Do not
troubleshoot a derivative by probing an unknown or live upstream source; first
establish a separately reviewed configuration and deployment boundary.
