# BDD сценарии для NFR требований

## NFR-001: Производительность
```gherkin```
Scenario: API response time meets performance requirements
  Given система находится под нагрузкой 500 RPS
  When выполняется 1000 запросов к эндпоинту /api/v1/users
  Then 95% запросов должны завершиться за ≤ 200ms
  And p99 latency должен быть ≤ 500ms

## NFR-002: Пропускная способность
```gherkin```
Scenario: System handles target RPS
  Given система развернута в production среде
  When выполняется нагрузочное тестирование с 1000 RPS
  Then система должна обрабатывать все запросы без ошибок 5xx
  And error rate должен быть < 1%