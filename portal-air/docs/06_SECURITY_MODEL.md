# 6. Модель безопасности

Этот документ намеренно описывает принципы, а не конкретные секреты и инфраструктурные детали.

## Основные правила

- TLS на внешних границах.
- Минимально необходимые privileges.
- Provider/API credentials вне Git.
- Secrets не попадают в SQLite/raw evidence/public docs.
- Authorization и чувствительные headers redacted до долговременного хранения.
- Private shadow integrations отделены от production.
- External probes имеют bounded scope, timeout и request budget.
- Любой production APPLY выполняется отдельным явным Gate.

## Важный практический вывод

Диагностический инструмент сам может стать источником утечки.

В ходе проекта было подтверждено, что автоматизация браузера/accessibility layer способна раскрыть значение, которое визуально отображается как password field. После этого credential должен рассматриваться как раскрытый и быть заменён.

Поэтому:

- не читать password fields через accessibility/debug APIs;
- не выводить secrets "для проверки";
- presence/length/schema проверять без значения;
- временные diagnostic artifacts удалять;
- secret scan не заменяет credential rotation при фактическом disclosure.

## Provider restrictions

Проект не рассматривает VPN/proxy/scraping как автоматический способ обойти ограничения внешнего сервиса. Если API недоступен по policy/location/access rules, источник переводится в `DEFERRED/BLOCKED` до законного способа доступа.
