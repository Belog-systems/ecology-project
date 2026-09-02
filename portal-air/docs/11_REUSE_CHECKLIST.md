# 11. Checklist для разработки сходной системы

## Device / protocol

- [ ] Снят реальный request физического устройства.
- [ ] Сохранён canonical fixture.
- [ ] Зафиксированы method/path/headers/body.
- [ ] Identity определена по фактическому protocol.
- [ ] Проверены реальные payload sizes.
- [ ] Проверена TLS совместимость именно физического устройства.

## Ingest

- [ ] Raw record создаётся до parsing.
- [ ] Credentials/redacted fields не сохраняются.
- [ ] Unknown/malformed payload не уничтожает evidence.
- [ ] Normalized fields nullable там, где sensor может не прислать значение.
- [ ] Duplicate identity детерминирована.

## Time

- [ ] Observation time отделено от receipt time.
- [ ] Replay не переписывает исходное время.
- [ ] Time synchronization state известен или ambiguity явно сохраняется.

## Reliability

- [ ] Gap не заменяется нулём.
- [ ] Причина gap не угадывается.
- [ ] Cadence completeness измеряется отдельно от HTTP uptime.
- [ ] Retry policy bounded.
- [ ] Queue overflow policy явная.

## External providers

- [ ] Source class определён.
- [ ] Upstream provenance проверен.
- [ ] Same-upstream duplicates не считаются независимыми.
- [ ] Terms/quota/retention/public display проверены.
- [ ] Первый live probe ограничен.
- [ ] Shadow integration не пишет в production.

## Linux deployment

- [ ] LF line endings.
- [ ] Executable bits.
- [ ] Shebang bytes.
- [ ] systemd unit sandbox/namespace.
- [ ] Installed artifact сравнивается с build artifact.

## Security

- [ ] Secrets вне Git.
- [ ] Secrets не выводятся диагностикой.
- [ ] Password fields не инспектируются accessibility tooling.
- [ ] Provider key не передаётся по plaintext HTTP.
- [ ] Secret exposure вызывает rotation.

## Backup / DR

- [ ] DB dump создан.
- [ ] Hash/size записаны.
- [ ] Restore выполнен в isolated target.
- [ ] Row/schema/fingerprint comparison PASS.
- [ ] Git backup независимо читается/clones.
- [ ] Runtime/config recovery artifact существует.
- [ ] Secret recovery tested.
- [ ] Bare-machine limitations явно записаны.

## Documentation

- [ ] README объясняет проблему до деталей реализации.
- [ ] Current / shadow / planned разделены.
- [ ] Failure cases задокументированы.
- [ ] Отрицательные результаты сохранены.
- [ ] Public docs не содержат operator-specific evidence и secrets.
