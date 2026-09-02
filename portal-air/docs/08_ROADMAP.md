# 8. Roadmap

Roadmap описывает направления, а не обещанные сроки.

## Ближайшее

1. Закрыть fresh DB restore verification.
2. Пересчитать DR readiness.
3. После закрытия checkpoint продолжить lawful Narodmon integration.
4. Квалифицировать local crowdsourced weather sources.

## Среднесрочно

- собственная weather station;
- local wind speed/direction;
- qualification score для external stations;
- расширенная provenance-aware визуализация;
- controlled historical export;
- более полноценный store-and-forward;
- диагностические события устройства.

## Долгосрочно

- собственная firmware;
- versioned sensor abstraction;
- robust UTC/time state;
- bounded persistent queue;
- replay;
- self-diagnostics;
- modular support PM/weather/gas/noise/other sensors;
- complete disaster recovery и bare-machine reprovision rehearsal.

## Принцип развития

Новый источник или subsystem сначала проходит:

```text
RESEARCH
→ OFFLINE/FIXTURE TEST
→ BOUNDED LIVE PROBE
→ SHADOW TRIAL
→ QUALIFICATION
→ отдельный PRODUCTION APPLY
```

Исследовательский успех не считается production activation.
