# 9. Инженерные уроки и реальные проблемы разработки

Этот документ намеренно фиксирует не только удачные решения, но и тупики. Именно такие сведения обычно теряются после запуска проекта, хотя они часто наиболее полезны следующей команде.

## 1. Сначала снять реальный protocol

### Ошибка, которой удалось избежать

Считать старый backend или документацию прошивки точным contract устройства.

### Что сделали

Сняли фактический HTTP request физической станции и только после этого зафиксировали method, path, headers, identity и JSON fields.

### Практический эффект

Backend строился под реальный packet, а не под предположение.

---

## 2. Browser HTTPS success не доказывает embedded HTTPS compatibility

Физическая ESP8266 не могла успешно подключиться к shared-hosting HTTPS, хотя browser/curl работали.

Исследование показало transport-level проблему вокруг constrained TLS buffer/MFLN и размера server handshake records.

### Решение

Контролируемый VPS TLS gateway между embedded station и WebHOST.

### Универсальный урок

При работе со старыми ESP8266/embedded TLS stacks проверяйте:

- TLS version;
- certificate chain;
- MFLN;
- record fragmentation;
- handshake sizes;
- actual device capture.

Не начинайте менять PHP/backend, если HTTP request вообще не дошёл до сервера.

---

## 3. Redirect может быть критичен для устройства

Разница `/api/push` и `/api/push/` для браузера почти незаметна. Для embedded client redirect может оказаться нежелательным или неподдерживаемым.

Gateway нормализует path до backend без необходимости заставлять устройство следовать redirect.

---

## 4. Похожий идентификатор не обязательно тот же identity

Hardware MAC и protocol `X-MAC-ID` отличались форматом.

Вывод: identity contract должен выводиться из wire protocol и проверяться явно.

---

## 5. Raw-first сохраняет возможность разобраться позже

Если parsing производится до сохранения исходного запроса, malformed/new-version payload может исчезнуть без доказательств.

Raw evidence с redaction позволяет:

- воспроизвести parser;
- сравнить версии;
- расследовать malformed packet;
- доказать, что request действительно пришёл.

---

## 6. Gap не сообщает причину

Отсутствие точки на графике не говорит, пропало ли питание, Wi-Fi, Internet, устройство или сервер.

Система должна сначала фиксировать наблюдаемый факт - gap - и только затем связывать его с независимой диагностикой.

---

## 7. systemd может ломаться не из-за приложения

В WEATHER shadow были реальные operational failures:

- `226/NAMESPACE` из-за зависимости от transient runtime namespace/path;
- `203/EXEC` из-за CRLF в Linux shell script/shebang.

### Что изменили

- отказались от хрупкой зависимости на transient shared runtime path;
- ввели LF packaging checks;
- проверку installed bytes/shebang;
- archive regression tests.

### Универсальный урок

"Код работает локально" не означает, что deployment artifact исполним на Linux. Проверяйте line endings, executable bit, installed bytes и unit sandbox/namespace.

---

## 8. Один provider ≠ один источник истины

AWC UHHH - реальное observation, но аэропорт удалён от городской точки.

Narodmon local station может быть ближе, но требует qualification.

Open-Meteo даёт model/forecast context.

Meteostat может агрегировать observations, но конкретная API route оказалась недоступна с VPS.

Вывод: качество определяется не названием API, а provenance, location, timing и подтверждённым behavior.

---

## 9. Два API могут быть одним upstream

Если разные сервисы публикуют UHHH METAR, статистически это не две независимые станции.

Такой источник полезен как transport redundancy, но должен быть помечен `SAME_UPSTREAM_REDUNDANCY`.

---

## 10. API может оказаться недоступным после всей offline разработки

Meteostat adapter и runtime были подготовлены и проверены offline, но единственный live request вернул HTTP 451.

### Урок

До глубокой зависимости от provider нужно отдельно проверять:

- region/location restrictions;
- legal terms;
- authentication;
- quota;
- machine-to-machine policy;
- retention/display rights.

---

## 11. Backup нельзя объявлять готовым без restore

Проект создал свежий SQL dump с hash/size, но isolated restore текущего checkpoint не подтвердился.

Поэтому статус остаётся:

```text
DATABASE_RESTORE = FAILED
FULL_DR_READINESS = PARTIAL
```

Это принципиальная дисциплина: backup - это не наличие файла, а доказанная способность восстановить данные.

---

## 12. Recovery artifact тоже имеет ограничения

Protected recovery bundle может быть криптографически корректным, но привязанным к конкретному OS/user profile.

Это лучше отсутствия backup, но не равно bare-machine disaster recovery.

---

## 13. Автоматизация диагностики может раскрыть секрет

Accessibility/debug tooling способно прочитать password value, даже когда UI показывает маску.

После такого disclosure пароль должен быть заменён независимо от того, попал ли он в Git.

---

## 14. Shadow architecture экономит риск

Новые WEATHER adapters можно исследовать, тестировать и ломать независимо от production PM data.

Это позволяет собирать evidence до решения "пускать ли источник в продукт".

---

## 15. Нельзя смешивать измерения разных источников без явного provenance

Если local crowdsourced station даёт скорость ветра, а аэропорт - направление, эти два числа можно показать рядом только с отдельными source/timestamp.

Их нельзя молча превратить в единый "ветер 5.7 м/с, 120°", будто это одно физическое наблюдение.
