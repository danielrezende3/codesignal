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
- Criação e modificações realizadas em ou antes de `at_timestamp`;
- Sobrescrita;
- Delete;
- TTL;
- Recriação posterior.
- Retorne `None` se o campo não existia ou estava expirado/removido naquele momento histórico.

Uma escrita já vale no seu timestamp; uma remoção já torna o campo inexistente
no timestamp da remoção. A expiração mantém o limite exclusivo do Level 3.
Considere a última versão escrita até o instante consultado: se ela foi removida
ou expirou, não retorne uma versão anterior. Consultar o passado não altera o
estado atual nem o histórico.
