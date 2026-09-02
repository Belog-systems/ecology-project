# Public publication boundary

Этот public tree формируется по whitelist, а не по принципу «опубликовать всё, что есть в internal repository».

Допустимы только явно reviewed public materials. Не переносить автоматически:

- `coordination/`;
- `evidence/`;
- backup/DR artifacts;
- handoff/checkpoint working files;
- credentials, sessions, cookies, private keys, private configuration;
- operator-specific paths, host data и диагностические артефакты.

Internal canonical/evidence/checkpoint документы остаются source of truth и не заменяются этой публичной редакцией.
