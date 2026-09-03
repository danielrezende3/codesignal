---

## Level 4 - Consultas históricas

### Assinaturas adicionadas
```python
class InMemoryDB:
    def get_at(self, timestamp: int, key: str, field: str, at_timestamp: int) -> int | None:
        ...
```

### Requisitos

> Qual era o valor desse campo em `at_timestamp`?

Considere:
- Criação e modificações anteriores a `at_timestamp`;
- Sobrescrita;
- Delete;
- TTL;
- Recriação posterior.
- Retorne `None` se o campo não existia ou estava expirado/removido naquele momento histórico.
