
**Файл: `docs/threat-model/NFR_TRACEABILITY.md`**
```markdown
# Матрица трассировки NFR требований

| NFR | Компоненты системы | Стратегия проверки | Метрики |
|-----|-------------------|-------------------|----------|
| **NFR-001**<br>Производительность | - API routers<br>- Database layer | - Load testing<br>- Performance monitoring | - p95 latency ≤ 200ms |
| **NFR-002**<br>Пропускная способность | - Web server<br>- Application logic | - k6 load tests | - ≥ 1000 RPS<br>- Error rate < 1% |
| **NFR-003**<br>Доступность | - Infrastructure<br>- Health checks | - Uptime monitoring | - 99.9% uptime<br>- MTTR < 30min |
| **NFR-004**<br>Безопасность данных | - Input validation<br>- Database layer | - SAST/DAST scanning | - Zero critical vulnerabilities |
| **NFR-005**<br>Валидация данных | - Pydantic schemas<br>- API endpoints | - Unit tests | - 100% schema coverage |
| **NFR-006**<br>Логирование | - Logging middleware<br>- Application logs | - Log analysis | - Structured JSON logs |
| **NFR-007**<br>Масштабируемость | - Docker containers | - Scaling tests | - Horizontal scaling |
| **NFR-008**<br>Резервное копирование | - Database<br>- File storage | - Backup tests | - RTO < 1 hour |

## Связь с существующими threat model документами

- **MJ DFD.md**: Взаимосвязь с компонентами системы
- **MJ RISKS.md**: Дополнение рисков, связанных с NFR
- **MJ STRIDE.md**: Анализ угроз для нефункциональных требований