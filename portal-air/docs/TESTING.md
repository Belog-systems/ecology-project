# Testing

Run from the repository root with Python available:

```powershell
python -m unittest discover -s portal_air_v1/tests -v
python -m unittest tools/tests/test_publication_audit.py -v
python tools/publication_audit.py . --fail-on P1
```

The Python tests use synthetic source responses and documentation-network
addresses only. They do not require a source endpoint, credentials, browser,
production database, or station traffic.

These checks establish local source-reader behavior only. They are not
deployment, production, external-provider, public-browser or physical-device
acceptance.
