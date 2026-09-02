# 7. Текущий публичный статус

Дата актуализации публичной редакции: 2026-09-01.

Этот статус сверен с authoritative checkpoint Portal Air, evidence которого завершено через `2026-09-01T06:52:34Z`. Публичный статус не заменяет internal checkpoint/evidence.

## Production - работает

- Физическая NRZ-станция передаёт данные через защищённый VPS TLS ingress/HAProxy.
- WebHOST PHP/MySQL принимает и хранит `RawIngest` + `Reading`.
- Read-only dashboard работает; long-window dashboard принят.
- Production completeness использует `event-cadence/v1`: gaps показываются как отсутствие поступивших данных, а не как автоматически установленная причина отказа.

Checkpoint remediation не изменяла production database/schema/data, ingest, dashboard, DNS, TLS, station, VPS runtime или provider settings.

## WEATHER - реализовано как private shadow и выключено

- Provider-aware WEATHER runtime установлен в private shadow-контуре.
- WEATHER providers и timers выключены; WEATHER services неактивны.
- Recurring polling не работает.
- Пути записи WEATHER в production PM-данные нет.
- AWC UHHH: ранее проверен ограниченный bounded external observation path; после проверки выключен.
- Meteostat: offline runtime проверен; единственный разрешённый запрос с текущего VPS вернул HTTP `451`; обход ограничения не выполнялся.
- Narodmon: только research/access-ready; account/app/key/API request/provider discovery/recurring polling не выполнялись.
- Open-Meteo: только `MODEL/FORECAST` context, не physical observation.

## Backup / DR

- Git recovery backup: `VERIFIED`.
- WebHOST private recovery checkpoint: `VERIFIED`.
- VPS off-host runtime checkpoint: `VERIFIED WITH DOCUMENTED RECOVERY LIMIT`.
- Fresh database dump: создан и имеет credential-free source fingerprint.
- Fresh restore этого dump: `FAILED`. Две новые изолированные попытки восстановления завершились существенно неполным результатом; логическая эквивалентность ожидаемому трёхтабличному dataset не доказана.
- Independent-machine recovery для DPAPI-защищённых recovery artifacts не доказан.
- Full rotation/reprovision rehearsal и bare-environment reprovision не выполнены.
- Формальная retention policy пока отсутствует.

Итог:

```text
DATABASE_RESTORE = FAILED
FULL_DR_READINESS = PARTIAL
PROJECT_CHECKPOINT = INCOMPLETE
```

`PROJECT_CHECKPOINT = INCOMPLETE` не означает, что production Portal Air не работает. Текущий основной blocker - свежий database restore и независимая logical equivalence verification.

## Следующий Gate

Единственный приоритетный Gate:

```text
DATABASE RESTORE FAILURE DIAGNOSIS
/ SUPPORTED IMPORT PATH OR PROVIDER-SIDE RESTORE
/ NEW FRESH ISOLATED TARGET
/ INDEPENDENT LOGICAL COMPARISON
```

Следующая попытка должна использовать новую disposable database и доказать ожидаемый table set, row counts, timestamp ranges, logical fingerprints, indexes/UNIQUE/FKs, charset/collation, AUTO_INCREMENT и representative `RawIngest`/`Reading` integrity.

Narodmon и другое feature development остаются остановлены до `DATABASE_RESTORE = VERIFIED` и повторного расчёта project checkpoint.
