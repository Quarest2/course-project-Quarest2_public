# STRIDE Analysis - Feature Votes API

## Анализ угроз по методике STRIDE

### Spoofing (Подмена идентичности)
| Угроза | Компонент | Митigations | Связанные NFR |
|--------|-----------|-------------|---------------|
| Подмена пользователя | Authentication | JWT токены, проверка подписи | NFR-004, NFR-005 |
| Подмена сервиса | API Gateway | mTLS, сертификаты | NFR-004 |

### Tampering (Изменение данных)
| Угроза | Компонент | Митigations | Связанные NFR |
|--------|-----------|-------------|---------------|
| Изменение голосов | Database | HMAC подписи, WAL | NFR-004, NFR-006 |
| Манипуляция результатами | Vote Service | Audit trails | NFR-006 |

### Repudiation (Отказ от действий)
| Угроза | Компонент | Митigations | Связанные NFR |
|--------|-----------|-------------|---------------|
| Отказ от голоса | Vote Service | Подписанные логи | NFR-006 |
| Отказ от операции | API Gateway | Correlation IDs | NFR-006 |

### Information Disclosure (Раскрытие информации)
| Угроза | Компонент | Митigations | Связанные NFR |
|--------|-----------|-------------|---------------|
| Утечка персональных данных | Database | Encryption at rest | NFR-004 |
| Раскрытие метрик | Monitoring | Access controls | NFR-006 |

### Denial of Service (Отказ в обслуживании)
| Угроза | Компонент | Митigations | Связанные NFR |
|--------|-----------|-------------|---------------|
| DDoS атака | API Gateway | Rate limiting, WAF | NFR-001, NFR-002 |
| Resource exhaustion | Vote Service | Quotas, monitoring | NFR-003 |

### Elevation of Privilege (Повышение привилегий)
| Угроза | Компонент | Митigations | Связанные NFR |
|--------|-----------|-------------|---------------|
| Неавторизованный доступ | Authentication | RBAC, принцип наименьших привилегий | NFR-004, NFR-005 |

## Ключевые выводы
- NFR-004 и NFR-005 критичны для защиты от Spoofing и Tampering
- NFR-006 обеспечивает non-repudiation через логирование
- NFR-001, NFR-002, NFR-003 защищают от DoS атак