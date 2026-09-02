# 5. WEATHER-источники

WEATHER в Portal Air - отдельный private shadow контур. Его задача - сначала квалифицировать источники, и только потом решать, какие данные допустимо показывать рядом с собственными измерениями.

## AWC / UHHH

Статус: `OBSERVATION`, bounded live path verified.

Это реальные аэропортовые наблюдения, но они относятся к UHHH, а не к точке размещения Portal Air.

Практический вывод: хороший официальный источник не становится "истиной для всего города" только из-за статуса источника.

## Meteostat

Статус: offline runtime verified, live access deferred.

Единственный разрешённый запрос с текущего VPS дошёл до HTTP уровня, но получил `451`. Второй запрос не выполнялся и route restrictions не обходились.

Практический вывод: provider может быть технически подходящим по API, но географически/юридически недоступным с конкретной инфраструктуры. Это нужно выявлять до построения production dependency.

## Narodmon

Статус: research / not activated.

Публичная карта показала, что в Хабаровске есть по крайней мере локальные community sensors, включая кандидата со скоростью ветра, температурой, влажностью и давлением. Но crowdsourced station не получает статус "качественная" автоматически.

Будущая квалификация должна учитывать:

- uptime;
- cadence;
- stale/flatline;
- spikes;
- bias;
- placement;
- exposure;
- wind obstruction;
- согласованность с независимыми источниками;
- долгосрочный drift.

Если local wind speed и airport wind direction приходят из разных источников, они должны сохранять отдельный provenance и не изображаться как единый вектор одной станции.

## Open-Meteo

Статус: contextual candidate.

Класс: `MODEL/FORECAST`, не physical observation.

## SAME_UPSTREAM_REDUNDANCY

Если Narodmon, NOAA, Ogimet или другой API лишь перепубликует тот же UHHH METAR, это может повысить transport redundancy, но не создаёт второе независимое метеонаблюдение.

Это различие важно для статистики и validation.
