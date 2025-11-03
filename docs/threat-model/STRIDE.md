# STRIDE — Анализ угроз

## Легенда
- **F1-F5**: Потоки данных из DFD
- **NFR-***: Нефункциональные требования из P03

## Таблица STRIDE

| Элемент/Поток | Угроза (STRIDE) | Описание | Контроль | Связь (F/NFR) |
|---|---|---|---|---|
| F1: User → API | **S**poofing | Подделка идентичности пользователя | Аутентификация, JWT tokens | F1 / NFR-AUTH |
| F1: User → API | **T**ampering | Изменение данных в транзите | HTTPS/TLS, проверка целостности | F1 / NFR-ENC |
| F1: User → API | **R**epudiation | Отказ от действий голосования | Логирование, аудиторский след | F1 / NFR-LOG |
| API Process | **I**nformation Disclosure | Утечка данных фич и голосов | Валидация выходных данных, маскирование | F1,F5 / NFR-VALID |
| F1: User → API | **D**enial of Service | DoS атака на endpoint'ы | Rate limiting, мониторинг | F1 / NFR-PERF |
| API Process | **E**levation of Privilege | Несанкционированные действия | Авторизация, RBAC | F1 / NFR-AUTH |
| F2: API → DB | **T**ampering | SQL Injection атаки | ORM, параметризованные запросы | F2 / NFR-SEC |
| Data Store | **I**nformation Disclosure | Несанкционированный доступ к БД | Шифрование БД, доступ по принципу need-to-know | F2,F4 / NFR-ENC |
| F3: Admin → API | **S**poofing | Подделка админского доступа | Сильная аутентификация, 2FA | F3 / NFR-AUTH |
| F3: Admin → API | **E**levation of Privilege | Расширение привилегий админа | Принцип минимальных привилегий | F3 / NFR-AUTH |

## Детализация контролей

### Аутентификация (NFR-AUTH)
- JWT tokens для пользователей
- OAuth2 для интеграций
- 2FA для администраторов
- Валидация сессий и токенов

### Шифрование (NFR-ENC)
- TLS 1.3 для HTTPS трафика
- Шифрование данных в БД
- Хеширование паролей (bcrypt)
- Key management система

### Логирование (NFR-LOG)
- Structured logging всех операций
- Аудиторский след голосований
- Централизованное хранение логов
- Alerting на подозрительную активность

### Валидация (NFR-VALID)
- Pydantic схемы для входных данных
- Валидация бизнес-правил
- Санитизация пользовательского ввода
- Ограничение размеров запросов

### Производительность (NFR-PERF)
- Rate limiting по IP/пользователю
- Кэширование часто запрашиваемых данных
- Мониторинг метрик производительности
- Автоскейлинг инфраструктуры

### Безопасность (NFR-SEC)
- Защита от OWASP Top 10
- Регулярные penetration tests
- Security headers (CSP, HSTS)
- Dependency vulnerability scanning

### Бизнес-логика (NFR-BIZ)
- Юнит-тесты критической логики
- Code review бизнес-правил
- Мониторинг аномалий голосования
- Валидация consistency данных
