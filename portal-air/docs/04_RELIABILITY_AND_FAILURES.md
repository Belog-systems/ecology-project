# 4. Надёжность и модель отказов

## Основной принцип

Система должна сохранять наблюдаемую реальность отказа, а не придумывать объяснение.

| Ситуация | Что допустимо утверждать |
|---|---|
| Нет события в ожидаемый момент | Есть gap. |
| DNS не разрешился | Зафиксирован DNS failure. |
| TLS handshake завершился ошибкой | Зафиксирован TLS failure. |
| HTTP 451 | Provider/route вернул HTTP 451. |
| Parser не распознал payload | Получение может быть доказано, нормализация - нет. |
| Device не отвечает | Устройство недоступно по проверенному каналу. |

Нельзя из одного gap автоматически заключить "пропал свет" или "сломался датчик".

## Урок: availability и data completeness - разные метрики

HTTP endpoint может быть доступен, но полезных measurement events может не быть. И наоборот, временная transport проблема может закончиться replay сохранённых наблюдений.

Поэтому Portal Air отдельно рассматривает:

- endpoint health;
- delivery attempts;
- event cadence;
- normalized measurement completeness.

## Store-and-forward

Будущий устойчивый контур должен сохранять исходное observation time и sequence/identity при временном отсутствии Internet/server.

Требования к replay:

- не заменять timestamp временем повторной отправки;
- не создавать дубли;
- учитывать attempt count;
- иметь bounded queue;
- иметь диагностируемую overflow policy;
- не удалять очередь после одной неудачной попытки.

## Backup ≠ Recovery

Один из практических выводов проекта: наличие SQL dump не доказывает возможность восстановления.

Для checkpoint требуется:

1. создать backup;
2. проверить hash/size;
3. восстановить в отдельную disposable database;
4. сравнить schema и данные;
5. только после этого считать restore verified.

На текущем checkpoint свежий dump существует, но fresh restore пока не подтверждён, поэтому `FULL_DR_READINESS = PARTIAL`.
