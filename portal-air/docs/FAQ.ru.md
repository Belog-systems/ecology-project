# Практический FAQ и инженерные уроки

[Русский](FAQ.ru.md) | [English](FAQ.md)

> **Граница документа.** Этот документ — документационный преемник неизменяемой
> санитарно очищенной базовой версии Portal Air. Он сохраняет санитарно очищенные
> уроки из исторических инженерных случаев. Это не рабочая инструкция, не
> руководство по развёртыванию и не доказательство текущего состояния какой-либо
> внешней системы.

## Как читать ответы

- **Установленная причина** означает, что указанный вывод подтверждён
  зафиксированными доказательствами конкретного случая. Это не утверждение, что
  у каждого устройства, провайдера или развёртывания будет та же причина.
- **Не установлено** означает, что имеющиеся доказательства не позволяли сделать
  более конкретный вывод. Это намеренное ограничение, а не пропущенная
  диагностика.
- **Эталонное дерево** означает публичный санитарно очищенный исходный набор в
  этом репозитории. Он отличается от исторических случаев, из которых извлечены
  уроки.
- Исторические детали обобщены: credentials, raw observations, private topology,
  настоящая identity станции и точное location не воспроизводятся.

## 1. Является ли это пакетом для производственного развёртывания?

**Вопрос.** Можно ли развернуть этот репозиторий или считать его действующим
сервисом Portal Air?

**Контекст.** Опубликованная базовая версия — это отобранный эталонный набор
исходных материалов, созданный на безопасной для публикации границе. В нём
сохранены узкий PM-source reader и документация, а не развёртывание приложения
и не копия рабочих систем.

**Симптомы.** Читатель может увидеть исходный код, тесты и неизменяемый tag
базовой версии и решить, что сюда входят listener, database, dashboard, map,
provider collector или station configuration.

**Диагностика.** Проверьте tracked paths и индекс документации. В эталонном
наборе нет listener configuration, live endpoint, deployment inventory, database
dump, provider registration, browser application или device-control path.

**Неудачные варианты.** Считать рабочую копию исходных материалов, успешно
прошедший локальный тест или опубликованный Git tag доказательством
развёртывания означало бы смешать обзор исходных материалов с приёмкой runtime.

**Установленная причина.** Базовая версия была намеренно санитарно очищена,
чтобы удалить материалы операционного владения и сделать публичный обзор
возможным без раскрытия частной инфраструктуры или данных.

**Решение.** Используйте эталонный набор как учебный и обзорный артефакт уровня
исходных материалов. Любое производное развёртывание проектируйте отдельно,
включая secrets, ingress, source contracts, privacy, backup/restore, rollback,
monitoring и browser acceptance.

**Проверка.** Включённые checks используют synthetic fixtures и локальный
publication audit. Они подтверждают только документированное поведение локальных
исходных материалов.

**Текущий статус.** Неизменяемая опубликованная базовая версия остаётся
эталонным исходным набором. Эта последующая документация добавляет только
пояснения; она не добавляет разворачиваемый runtime и не изменяет какое-либо
развёртывание.

**Рекомендации.** Перед копированием любой идеи проекта начните с
[CURRENT_STATE.md](CURRENT_STATE.md), [LIMITATIONS.md](LIMITATIONS.md) и
[REUSE_GUIDE.md](REUSE_GUIDE.md).

**История.** Ранняя публичная документация описывала инженерные результаты более
прямо. Позднейшая санитарно очищенная базовая версия намеренно удалила рабочие
детали; этот FAQ восстанавливает уроки, не восстанавливая чувствительные
материалы.

## 2. Как следует устанавливать протокол станции?

**Вопрос.** Безопасно ли проектировать ingest API на основе старого backend или
device documentation?

**Контекст.** Историческая интеграция станции началась с неизвестного
фактического request, хотя старый backend уже содержал правдоподобный, но
неподтверждённый contract.

**Симптомы.** Server может выглядеть готовым, однако physical device способен
отправлять другой method, path, форму identity, структуру body или схему
authentication.

**Диагностика.** Получите один фактический request через узкий capture adapter,
независимый от предполагаемого parser. Зафиксируйте безопасные факты: method,
path, query, headers после redaction, body bytes после redaction и server receipt
time. Превратите безопасное представление в fixture для регрессии.

**Неудачные варианты.** Переиспользование старого endpoint contract,
предположение полей request или отношение к сгенерированному simulator JSON как
к доказательству wire bytes физического устройства были отклонёнными подходами.

**Установленная причина.** Существующий code и описание firmware не
устанавливали фактический wire contract физической станции. Это установил только
фактический capture.

**Решение.** Постройте raw-first adapter для наблюдаемого packet. Изменяйте
parser после fixture replay и повторяйте capture/replay при изменении поведения
firmware.

**Проверка.** Полезный fixture проверяет и structural interpretation, и, где
нужно, byte-sensitive properties, такие как body size и digest, не публикуя
исходный packet.

**Текущий статус.** Публичный эталонный набор сохраняет принцип, но не содержит
packet ingest endpoint или fixture реальной станции.

**Рекомендации.** Выполняйте capture до проектирования schema или
authentication. Неизвестные безопасные fields и partial packets сохраняйте как
evidence, а не отбрасывайте.

**История.** Исторический случай заменил предполагаемый legacy contract на
captured device contract и workflow регрессии.

## 3. Зачем хранить raw receipt evidence отдельно от нормализованных readings?

**Вопрос.** Почему не разобрать request сначала и не сохранить только итоговые
показания?

**Контекст.** Полевые устройства и внешние источники могут присылать неполные,
некорректные или расширенные сообщения. У parser также может быть defect.

**Симптомы.** Если normalisation сначала завершилась неудачей, может оказаться
невозможным узнать, пришло ли вообще что-то, что изменилось в более поздней
версии firmware или вызвала ли parser regression потерю.

**Диагностика.** Сопоставляйте evidence receipt, status parse, version parser и
normalised output. Убедитесь, что sensitive headers, credentials, cookies и
secret fields redact либо исключены до долгосрочного хранения.

**Неудачные варианты.** Удаление некорректного input, хранение authentication
material для удобства и приравнивание отсутствующей нормализованной row к
отсутствующей delivery были отклонены.

**Установленная причина.** Parsing и receipt — разные факты. Parser не может
восстановить input, который не был безопасно retained.

**Решение.** Сначала создавайте безопасную raw-запись факта получения, затем
пытайтесь нормализовать. Сохраняйте связь между raw record и любым normalised
observation; явно представляйте outcomes valid, partial, invalid и parse-error.

**Проверка.** Tests должны охватывать valid, partial, malformed, unknown и
requests с credential, включая доказательство отсутствия protected material в
retained records.

**Текущий статус.** Эталонный исходный набор документирует этот pattern, но не
имеет средства записи в database или live raw store.

**Рекомендации.** Считайте raw retention evidence custody: определите правила
redaction, retention, access и deletion до сбора live data.

**История.** Этот pattern сохранён, поскольку позволял позднее исследовать
parser и protocol, не стирая молча event delivery.

## 4. Почему HTTP redirect и identity станции рассматривались как две разные
проблемы?

**Вопрос.** Можно ли диагностировать failed embedded send как одну общую ошибку
authentication?

**Контекст.** Исторические случаи включали и path canonicalization до
application, и несовпадение identity после того, как authentication уже дошла до
backend.

**Симптомы.** Один случай дал HTTP redirect для ingest path без trailing slash.
Другой создал receipt record, но отклонил message, потому что поле protocol
identity не совпало с настроенным value.

**Диагностика.** Для поведения path проверяйте оба принятых variants path с
выключенными redirects и изучайте status и поведение `Location`. Для identity
сравнивайте только явно согласованные wire identity fields после authentication;
не подставляйте source address, browser-like user agent или визуально похожую
hardware label.

**Неудачные варианты.** Предполагать, что device следует redirects,
идентифицировать его по address, считать hardware identifier автоматически
взаимозаменяемым с wire identifier или винить password в каждом rejection были
отклонены.

**Установленная причина.** Redirect произошёл при path canonicalization до
application. Случай identity возник из-за несовпадения prefix/form между
настроенным identity и value on the wire, а не из-за password failure.

**Решение.** Нормализуйте accepted legacy path variants внутренне, не заставляя
device следовать redirect. Определяйте station identity по фактическим protocol
fields и храните complete protocol form, требуемую для comparison.

**Проверка.** Regression checks независимо покрывают оба paths без redirects и
каждое несовпадение identity field. Успешное normalised reading должно быть
связано с authenticated, valid receipt record.

**Текущий статус.** Публичное дерево не включает ни live route, ни identity
реальной станции. Это reusable diagnostic lessons, а не раскрываемые service
details.

**Рекомендации.** Диагностируйте по слоям: transport, HTTP path,
authentication, identity, parsing и normalisation. Изменяйте по одной переменной
за раз.

**История.** Разделение этих случаев позволило не менять authentication или
database code для request, который ещё не достиг соответствующего layer.

## 5. Почему обычный успех HTTPS не доказал совместимость с устройством ESP8266?

**Вопрос.** Если browser и command-line client могут достичь HTTPS, обязательно
ли с ним совместима embedded station?

**Контекст.** Ограниченный ESP8266-class client не прошёл этап до HTTP у одного
TLS frontend, тогда как ordinary desktop clients работали успешно.

**Симптомы.** Device сообщал о connection failure; не появлялось ни нового HTTP
receipt, ни application log entry. Изменение parser, authentication или database
code не могло повлиять на результат.

**Диагностика.** Отделяйте pre-HTTP TLS behavior от поведения application.
Исследуйте negotiated TLS version, certificate validation, maximum-fragment
negotiation и фактические границы incoming handshake-record. Сравните
acceptance физического устройства через controlled compatible gateway.

**Неудачные варианты.** Browser-only checks, успешный ordinary HTTP request,
предположение, что maximum-fragment extension сама по себе гарантирует record
sizing, и изменение backend logic до появления request были отклонены.

**Установленная причина.** Исторические evidence поддерживали
high-confidence проблему совместимости TLS до HTTP: direct frontend не
предоставлял поведение record, нужное ограниченному client. Device не выдавал
low-level failure code, поэтому вывод остаётся ограниченным evidence, а не
универсальным утверждением обо всех ESP8266 firmware.

**Решение.** Поместите controlled TLS gateway перед backend. Его accepted
configuration ограничивалась нужной TLS version, совместимым fragment/record
behavior, internal path handling, strict request guards и verified upstream TLS;
он не становился application parser или data queue.

**Проверка.** Historical acceptance требовал desktop TLS inspection,
измерение record на уровне packet и handshake физического устройства вместе с
response acknowledgement. Synthetic POST было недостаточно.

**Текущий статус.** Публичный эталонный набор не содержит gateway configuration
или live transport endpoint. В нём зафиксирован только метод решения и
ограничение, согласно которому desktop TLS нельзя считать evidence устройства.

**Рекомендации.** Повторяйте physical и packet-level checks после изменения
certificate, chain, TLS-library, proxy или gateway. Предпочитайте future device
firmware, которая validates server identity, вместо отключения такой validation.

**История.** Gateway был bounded transport adaptation для constrained client, а
не утверждением, что shared hosting, browsers или все ESP8266 deployments
дефектны.

## 6. Как следует представлять время, дубликаты, gaps и полноту?

**Вопрос.** Может ли receipt time заменять measurement time и объясняет ли
отсутствующая точка outage?

**Контекст.** Portal Air различает source observation time, server receipt или
fetch time и любое publication/model time. Попытки delivery и normalised
observations также различны.

**Симптомы.** Delayed или repeated delivery может создать вводящие в заблуждение
timestamps или duplicate rows. Chart может ложно нарисовать continuous line
через absence. Gap может соблазнить оператора вывести power, network, sensor или
server failure.

**Диагностика.** Сохраняйте каждое известное time field отдельно; используйте
`null`, когда истинное observation time неизвестно. Сохраняйте evidence delivery
и deterministic identity, чтобы repeated delivery была видна, но не превращалась
в неотличимое second observation. Вычисляйте полноту cadence отдельно от
availability endpoint и полноты channel.

**Неудачные варианты.** Заменять observation time receipt time, отображать
absence как zero, соединять long gaps в chart и приписывать cause только по gap
были отклонены.

**Установленная причина.** Timing, delivery, normalisation и provenance source
описывают разные факты. Data gap устанавливает только то, что expected data не
была получена или представлена в выбранной model; она не устанавливает почему.

**Решение.** Сохраняйте semantics time, явно моделируйте expected event cadence,
отображайте declared или достаточно длинные gaps как breaks и фиксируйте
source-specific status, такие как current, stale, no data, source unavailable и
error, не смешивая их.

**Проверка.** Тестируйте delayed delivery, duplicate identity, missing events,
partial channels, empty denominators, window boundaries и поведение chart gap.

**Текущий статус.** Эталонный reader ориентирован на receipt. Там, где он не
может знать source observation time, future public projection должна оставлять
`observed_at_utc` равным `null`, а не изобретать его.

**Рекомендации.** Зафиксируйте expected interval намеренно после observation и
запишите scope его calibration. Не переносите молча cadence или time semantics
одного device на другой source.

**История.** Project сохранил анализ event-cadence как model качества data, а не
как diagnosis physical cause каждого absence.

## 7. Как показывать внешние WEATHER-источники, не выдавая их за локальные
измерения?

**Вопрос.** Можно ли объединить в одно локальное значение погоды аэропортовое
наблюдение, crowdsourced sensor, aggregation service и forecast?

**Контекст.** В историческом исследовании и ограниченной работе с providers
наряду с PM data на месте рассматривались airport-METAR observation lane,
Meteostat, Narodmon и Open-Meteo.

**Симптомы.** Несколько providers могут предоставлять temperature или wind
fields, однако их location, экспозиция измерения, source time, правила revisions,
upstream и legal terms могут различаться. Два API также могут перераспределять
один и тот же upstream report.

**Диагностика.** Фиксируйте source class, identity provider/source, observation
time, receipt/fetch time, freshness, units полей, отсутствующие fields,
отношение к upstream и terms отображения/retention. Прежде чем считать
crowdsourced source надёжной точкой для сравнения, проведите его qualification.

**Неудачные варианты.** Считать аэропортовое наблюдение истиной для всего
города, переименовывать model или forecast в physical observation, объединять
wind speed одного источника с direction другого, повторять обращение к
policy-blocked provider route или предполагать, что видимый community sensor уже
qualified, были отклонены.

**Установленная причина.** Значения с одинаковой меткой могут представлять
разные физические и вычислительные явления. В одном историческом Meteostat
probe единственный HTTP 451 установил заявленный ответчиком outcome доступа/
compliance, но не независимую доказанную geographic, legal или infrastructure
root cause.

**Решение.** Сохраняйте airport-METAR lane как отдельный контекст external
observation; относите Open-Meteo к контексту `MODEL`/`FORECAST`; prospective
Narodmon data относите к `CROWDSOURCED_OBSERVATION` только после secure access,
terms и qualification; а live collection из policy-blocked Meteostat оставляйте
выключенным, пока законный, supported path не одобрен независимо.

**Проверка.** Provider нуждается в fixture tests, bounded request accounting,
safe raw/health retention, source-time validation и isolated shadow lane до
любого production use. Успешный request сам по себе не доказывает public display
rights или representativeness.

**Текущий статус.** Этот публичный эталонный исходный набор не реализует
provider, polling, weather store или map. В нём нет external observations.
Исторические provider cases сохранены только как lessons о provenance и control.

**Рекомендации.** Вводите каждого provider по последовательности: research,
offline fixture test, bounded live probe, shadow qualification, затем отдельное
production decision. Не используйте proxy или иной обход для уклонения от access
restriction.

**История.** Историческая запись включает ограниченный airport-observation lane,
отложенный Meteostat live route после HTTP 451, меняющиеся evidence access для
Narodmon, всё ещё требовавшие terms и authorization оператора/provider, и
classification Open-Meteo как model/forecast.

## 8. Почему Linux/systemd deployment может завершиться неудачей, даже если
code и unit syntax выглядят правильными?

**Вопрос.** Достаточны ли local test или успешная проверка syntax unit file,
чтобы доказать работу scheduled service в Linux?

**Контекст.** У private external-data worker произошли две отдельные
operational failures: одна была связана с transient runtime namespace, а другая
— с окончаниями строк в executable wrapper.

**Симптомы.** Один service прекращал работу до выполнения полезной задачи,
поскольку ожидал ненужный runtime path. Другой не запускался, хотя script
присутствовал и его unit syntax был valid.

**Диагностика.** Изучите service result class, bytes установленного file,
shebang, line endings, executable bit, ownership, sandbox paths и фактическое
scheduled execution. Тестируйте установленный artifact, а не только source tree.

**Неудачные варианты.** Рассматривать application code как единственную
возможную причину failure, полагаться только на unit syntax validation,
сохранять ненужную dependency от runtime directory или предполагать, что shell
script, отредактированный в Windows, executable в Linux, были отклонены.

**Установленная причина.** Первая failure была вызвана dependency от namespace/
path, не нужной worker. Вторая произошла из-за CRLF bytes в shell shebang,
которые изменили имя interpreter во время execution.

**Решение.** Уберите ненужную runtime dependency, обеспечьте LF packaging
checks, проверьте bytes установленного artifact и executable metadata и требуйте
одно реальное bounded service execution в дополнение к offline tests.

**Проверка.** Исправление namespace было проверено bounded no-network service
execution. Исправление expired-wrapper позднее было проверено через
installed-byte checks и реальное service execution. Provider work оставалась
изолированной; containers не были обязательным solution.

**Текущий статус.** В публичном эталонном наборе нет systemd unit, container
image или deployment artifact. Никакие evidence не устанавливают, что container
решил бы историческую packaging problem.

**Рекомендации.** Выбирайте container только после того, как он решает
конкретное operational requirement. Независимо от packaging style, тестируйте
final Linux artifact, его permissions, line endings, isolation и rollback
behavior.

**История.** Этот case сохранён, поскольку отделяет application logic от
failures packaging и service manager, не публикуя operational unit file.

## 9. Что фактически доказывает acceptance dashboard, API или map?

**Вопрос.** Устанавливает ли успешный HTTP probe, что публичное browser
application пригодно для использования?

**Контекст.** Исторические dashboard и map work отделяли server-to-server/API
checks от rendering, видимого пользователю, и защищали continuity ingest.

**Симптомы.** Route может вернуть technical success, тогда как browser получает
другое content, authentication challenge, blocked asset, stale data или
incomplete render. Chart также может неверно представить missing data.

**Диагностика.** Отдельно проверяйте data contract и same-origin API. Затем
используйте обычный установленный browser с fresh task-owned profile, без
user-agent override, injected cookies, task authentication headers, proxy или TLS
bypass. Подтвердите normal redirects, expected application content, critical
same-origin requests и rendering gaps.

**Неудачные варианты.** Считать command-line HTTP success, специальный test
user agent, fixture-only browser run или synthetic post public user acceptance
были отклонены.

**Установленная причина.** Technical transport success и browser acceptance,
видимая пользователю, проверяют разные layers и должны оставаться разными
evidence classes.

**Решение.** Держите browser clients на reviewed same-origin projections;
раскрывайте только data, требуемые UI; сохраняйте semantics provenance, time,
freshness и gaps; и принимайте public UI только после evidence ordinary browser.

**Проверка.** Historical UI work использовала раздельные API, privacy, browser и
post-change ingest-continuity gates. Каждый gate фиксировал, что он доказывает и
чего не доказывает.

**Текущий статус.** Публичный эталонный набор не включает HTTP application,
browser assets, map runtime, coordinates или public API. Он не может установить
browser acceptance.

**Рекомендации.** Не добавляйте frontend или map library лишь потому, что есть
data reader. Сначала определите public projection, privacy policy, terms,
security headers, browser acceptance и rollback boundary.

**История.** Это различие сохранено после cases, в которых technical probes и
поведение browser расходились.

## 10. Какие уроки security применимы к diagnostics и secrets?

**Вопрос.** Безопасно ли для troubleshooting inspect masked password field или
временно log secret?

**Контекст.** Engineering diagnostics могут пересекать ту же privacy boundary,
что и application.

**Симптомы.** Value может быть визуально masked в browser interface, но
automation или accessibility layer всё равно способны его прочитать. Raw request
captures также могут содержать authentication material.

**Диагностика.** Проверяйте наличие, schema, boolean state или protected digest
вместо secret value. Проверяйте reports, terminal output, fixtures, browser
profiles, screenshots, logs и paths raw retention на риск disclosure.

**Неудачные варианты.** Печатать credentials «только чтобы их проверить»,
сохранять authorization header в raw evidence, считать Base64 encryption или
предполагать, что visual password masking защищает debug APIs, были отклонены.

**Установленная причина.** Masking влияет на presentation, но не обязательно на
programmatic access. Если value credential раскрыто на неразрешённой diagnostic
surface, его необходимо считать disclosed.

**Решение.** Держите secrets вне Git и public documentation; выполняйте redaction
до retention; используйте least privilege; не помещайте provider secrets в URLs и
command lines; и rotate credential после фактического disclosure.

**Проверка.** Publication review сочетает automated scanning и manual
inspection. Чистый scan поддерживает review, но не может доказать, что вся
обработка secrets безопасна.

**Текущий статус.** Публичный исходный набор не содержит production access
material. Его publication-audit tool — defense-in-depth scanner, а не credential
management system.

**Рекомендации.** Проектируйте diagnostics так, чтобы они сообщали categories и
safe metadata, а не values. Сообщайте о suspected disclosure по private channel,
не копируя sensitive material в issue.

**История.** Diagnostic-accessibility lesson сохранён, поскольку он изменил
classification exposure credential, даже когда value не был committed.

## 11. Почему backup не эквивалентен disaster recovery?

**Вопрос.** Доказывает ли успешный dump или archive, что data можно restore?

**Контекст.** Historic recovery work различала creation backup artifact,
isolated import, logical comparison, off-host custody и bare-environment
recovery. На более раннем checkpoint restore database из fresh dump был отмечен
как `FAILED`: доступные isolated targets не устанавливали logical import. Более
поздние evidence установили отдельный isolated import и bounded comparison.

**Симптомы.** Dump может иметь правдоподобные size и digest, но не импортироваться,
восстанавливать только часть expected data, зависеть от unavailable tooling или
быть непригодным вне particular host/profile.

**Диагностика.** Выполняйте restore в новый disposable target. Проверяйте schema,
row-level или logical identity, representative data relationships,
indexes/constraints, time ranges, integrity и возможность использовать restored
result без обращения к production.

**Неудачные варианты.** Считать создание backup completed recovery test,
восстанавливать поверх production, принимать provider statement без evidence или
приравнивать same-host operational snapshot к full disaster recovery были
отклонены.

**Установленная причина.** Backup generation и recovery — отдельные capabilities.
Более ранний результат `FAILED` остаётся частью historical record. Он был
заменён только в отношении более позднего scope isolated database-import и
comparison; он не доказывал off-host custody, independent-machine recovery,
protected-secret recovery или full reprovisioning.

**Решение.** Держите bounded, isolated restore rehearsal в acceptance path и
указывайте его exact scope. Защищайте recovery material и избегайте destructive
operations во время verification.

**Проверка.** Meaningful rehearsal фиксирует identity source artifact, isolated
target, comparison method, result и то, что остаётся вне test.

**Текущий статус.** Этот публичный эталонный набор не содержит dump, restore
script или recovery artifact. Он не заявляет disaster-recovery readiness.

**Рекомендации.** Определите retention, encryption/key custody, off-host
handling, recovery objectives и recurring isolated restore/round-trip exercise
до объявления DR readiness.

**История.** Historic status менялся по мере появления более сильных evidence
restore. Сохранённый lesson — хранить и ранний outcome `FAILED`, и точный, более
узкий scope его позднейшего замещения.

## 12. Как безопасно переиспользовать или публиковать этот материал?

**Вопрос.** Что безопасно копировать в другой monitoring project и что должно
оставаться вне public history?

**Контекст.** Полезный результат Portal Air — прежде всего последовательность
engineering questions, границ failure и methods validation, а не универсальный
продукт для станции или готовый operations stack.

**Симптомы.** Копирование deployment recipe, production address, raw capture или
provider decision в новую environment может создать privacy, security или
correctness failure.

**Диагностика.** Относите каждый candidate artifact к public source, synthetic
fixture, private configuration, raw evidence, credential, deployment custody или
owner decision. Проверяйте, действительно ли для него предоставлены license и
redistribution status.

**Неудачные варианты.** Копировать internal Git history, считать old public claim
current fact, публиковать realistic substitute location, использовать provider
content без terms review или предполагать, что public availability даёт software
license, были отклонены.

**Установленная причина.** Публичная документация требует иной evidence и privacy
boundary, чем внутренняя operational history. Чистый публичный Git root не
заменяет review, но не даёт inherited private history молча попасть в source
snapshot.

**Решение.** Переиспользуйте method: capture фактического device contract,
постройте raw-first ingest, физически test constrained transport, держите source
provenance отдельно, вводите providers через shadow process, rehearse recovery и
публикуйте только sanitized reviewed artifacts.

**Проверка.** Перед распространением запустите publication audit и local tests,
вручную проверьте все configuration samples и documents, проверьте links и path
allowlists, а также изучите final staged diff, а не только working directory.

**Текущий статус.** Original immutable published tag остаётся неизменным. Эта
опубликованная последующая документация — дополнительный recovery document;
repository access не подразумевает license grant.

**Рекомендации.** Используйте [REUSE_GUIDE.md](REUSE_GUIDE.md) как practical
checklist. В новом project держите sources, evidence, secrets, licensing и
production decisions под собственным review process.

**История.** Первый публичный narrative содержал более широкие lessons, которые
были удалены при sanitization. Этот successor восстанавливает их subject matter,
сохраняя позднейшую privacy boundary.

## 13. Почему browser demonstration не доказывает, что полный Core готов для
browser?

**Вопрос.** Если browser может загрузить один module через test adapter,
доказывает ли это, что полная архитектура Foundation/Core готова работать в
browser?

**Контекст.** Датированное feasibility review отделяло copied browser-facing
reference module от более полного Core, который также зависел от Node-bound
filesystem, path, URL и работы configuration.

**Симптомы.** Небольшой module может загрузиться с copied reference data и
synthetic context, тогда как полный import graph не может загрузиться,
provision itself или завершить lifecycle в browser. Отдельно passing Node-side
tests могут скрыть эту boundary.

**Диагностика.** Определите exact module, import graph, data adapter,
configuration path и lifecycle, которые были exercised. Тестируйте browser
execution и Node execution как разные environments. Проверяйте declared schemas
и runtime validator независимо, прежде чем считать их единым contract.

**Неудачные варианты.** Называть synthetic adapter spike full Core integration,
приравнивать Node suite к browser readiness или считать один imported reference
module доказательством browser-safe provisioning были отклонены.

**Установленная причина.** Browser feasibility имеет scope. Copied module может
быть browser-feasible, тогда как полный Node-oriented Core остаётся не готовым
для browser. Ни один результат не следует продвигать за пределы exact topology,
которая была exercised.

**Решение.** Спроектируйте deliberate boundary между Node-side provisioning и
browser execution. Определите browser-safe descriptors, configuration, assets и
host authority до попытки полного lifecycle.

**Проверка.** Full browser readiness требует evidence от actual Core topology в
ordinary browser. Результаты module, fixture и synthetic-adapter остаются
полезными, но более узкими evidence classes.

**Текущий статус.** Этот публичный эталонный набор не включает ни Foundation
runtime, ни browser application. Он не делает claim о текущей browser
compatibility внешней системы.

**История.** Feasibility case оставался `PARTIAL` / `BLOCKED`, а не был повышен
от limited browser success до full-Core pass.

## 14. Почему nullable public field должно присутствовать как `null`, а не
отсутствовать?

**Вопрос.** Эквивалентно ли absent field полю, чьё известное value явно равно
`null`?

**Контекст.** Local contract guard первоначально считал absent observation-time
key таким же, как явно present value `null`. Связанные reviews также показали,
почему declared schema и runtime validator нуждаются в собственных evidence.

**Симптомы.** Positive fixture может пройти, даже если required public field
omitted, typed incorrectly или заменено unexpected container. Тогда consumers
получают ambiguous contract, хотя self-check выглядит green.

**Диагностика.** Раздельно test наличие key, allowed nullability, exact
scalar/container type и permitted field set. Включите negative fixtures для
absent key, explicit `null`, unexpected nested object и unknown field, когда
public contract его запрещает.

**Неудачные варианты.** Использовать lookup, чьё fallback value делает absent и
`null` indistinguishable, проверять только happy-path fixture или предполагать,
что schema declaration автоматически доказывает runtime validation, были
отклонены.

**Установленная причина.** Nullable означает, что present value может быть
`null`; это не делает field optional. Schema review, parser behavior,
serialization и consumer validation каждое нуждаются в explicit boundary.

**Решение.** Используйте exact public allowlist и fail closed для absent required
keys, invalid types или forbidden structure. Сохраняйте `null`, когда source не
предоставляет фактическое observation time, вместо его изобретения.

**Проверка.** Исправленный local fixture guard может защищать выбранный source
path. PHP endpoint, browser, deployment и production evidence остаются отдельными
scopes acceptance.

**Текущий статус.** Эталонный reader документирует receipt-oriented contract; он
не exposes public endpoint из этого tree.

**История.** Узкий diagnostic defect был corrected и independently reviewed
локально без превращения результата в runtime-health claim.

## 15. Почему anonymous serialization и честные time labels — одна проблема
public contract?

**Вопрос.** Может ли dashboard удалить очевидный identifier, но всё ещё
раскрывать stable identity или неверно представлять время measurement?

**Контекст.** Bounded source-contract review рассматривал public station и
cadence DTOs вместе с receipt-derived field «last received» и его формулировкой
UI.

**Симптомы.** Identity может сохраниться в nested metadata, cadence fields, raw
linkage, stable replacement values или error shape. Label вроде «last
measurement» также может превратить server receipt в выдуманное observation time.

**Диагностика.** Проверьте каждый short-window, long-window, cadence, error и
rendering path. Используйте exact public-field allowlist; попробуйте
identity-bearing values в direct и nested locations; и проследите каждую видимую
time label до source fact.

**Неудачные варианты.** Удалять только один visible identifier, заменять его
stable anonymous-looking token, доверять тому, что scalar field останется scalar,
или label receipt time как measurement time были отклонены.

**Установленная причина.** Privacy и time semantics — обе serialization
boundaries. Полезной public projection не нужны ни station identity, ни
вымышленный observation timestamp.

**Решение.** Выводите только generic display label и minimum reviewed status или
receipt fields. Проверяйте nested structures fail-closed, label receipt time как
receipt и оставляйте unavailable observation time явно unknown.

**Проверка.** Negative source и rendering fixtures могут проверять direct и
nested disclosure paths. Они не доказывают, что endpoint был deployed или что
ordinary browser сейчас serves reviewed DTO.

**Текущий статус.** Этот эталонный исходный набор не имеет dashboard endpoint
или browser assets. Lesson — это правило проектирования public contract, а не
report о live dashboard.

**История.** Связанная remediation была accepted только в bounded local
source/fixture scope.

## 16. Как WEATHER reader должен обрабатывать store drift и ненадёжную fixture
cleanup?

**Вопрос.** Может ли read-only weather projection предполагать, что private store
всегда будет иметь schema и timing behavior, ожидаемые его tests?

**Контекст.** Local WEATHER work выявила два независимых maintenance risks:
reader зависел от private normalized-store shape без explicit version handshake,
а fixture suite могла смешивать wall-clock completion time с fixed test time или
оставлять temporary store open после failure.

**Симптомы.** Reader может query old, future, incomplete или differently shaped
store. Test может pass или fail из-за timing coincidence, а temporary SQLite file
может оставаться locked во время cleanup. Ни один симптом не доказывает provider
или production failure.

**Диагностика.** Открывайте private store read-only; до query проверяйте его
supported version, required table и required projection fields; а при
incompatibility выводите только generic public source error. В tests отдельно
inject scheduler и completion clocks, block network access и close stores до
temporary-directory removal.

**Неудачные варианты.** Молча адаптировать unknown store, позволять private
schema или path details попасть в public error, считать local suite provider
health или менять runtime provider только для того, чтобы fixtures стали green,
были отклонены.

**Установленная причина.** Store compatibility и fixture determinism — разные
contracts. Надёжная local regression нуждается в explicit versioning, cleanup и
time ownership; она не устанавливает health live collector.

**Решение.** Fail closed для unsupported store shapes, сохраняйте reader как
read-only projection и делайте test clocks и порядок cleanup deliberate.

**Проверка.** Writer-shaped temporary stores и fail-closed fixtures могут
локально exercise boundary. Provider polling, deployed SQLite custody,
поведение Linux/service и ordinary-browser acceptance нуждаются в собственных
evidence.

**Текущий статус.** Публичный эталонный набор не реализует WEATHER provider,
polling, store или map runtime.

**История.** Reported repairs относились только к local source и fixtures; они не
были результатом состояния external service.

## 17. Чего bounded check не устанавливает о data, hosting или recovery?

**Вопрос.** Может ли source fixture, selected static-asset match, successful
public read или historical package check установить, что deployment, database,
ingest path или recovery plan healthy?

**Контекст.** Датированные reviews дали несколько разных evidence classes: local
source и PHP fixtures, limited served-public-projection observation, selected
static-asset comparisons, historical package с unreproducible canonical asset
manifest и unavailable current database read boundary.

**Симптомы.** Technical success можно описать как full deployment parity; одну
visible projection можно принять за natural authenticated ingest; или различие
line endings в working tree можно спутать с artifact-integrity defect. Historical
package может оставаться available даже после потери статуса reproducible
deployment authority.

**Диагностика.** Составьте claim-to-evidence matrix. Относите source tests к их
fixtures, selected asset equality к этим exact assets, а public read — к response,
observed в тот time. До таких claims отдельно получите authorized aggregate
database, natural-ingest, hosting/edge и isolated-restore evidence. Сравнивайте
canonical artifact bytes с его manifest, а не только checkout representation.

**Неудачные варианты.** Считать HTTP success доказательством database или ingest,
считать selected assets full deployment parity, repair old manifest bytes лишь
для того, чтобы check стал green, или называть inaccessible data boundary healthy
были отклонены.

**Установленная причина.** Evidence зависит от claim. Limited observation может
быть ценным, не доказывая окружающую system, а unreproducible historical package
следует сохранить как history, но вывести из роли future deployment authority.

**Решение.** Держите evidence labels узкими, fail closed там, где artifact или
access boundary не может поддержать intended claim, и используйте отдельно
reviewed successor для любого нового deployment или recovery exercise.

**Проверка.** Фиксируйте exact scope, date, inputs и exclusions для каждого
check. Не превращайте local fixture, browser harness, provider observation или
isolated restore в более широкий acceptance class.

**Текущий статус.** Этот эталонный набор не имеет database, ingest endpoint,
hosting configuration, asset package или recovery artifact. Он не делает claim о
текущем состоянии ни одного из них.

**История.** Сохранённые cases учат сохранять полезные limited evidence, не
скрывая всё ещё unverified boundaries вокруг них.
