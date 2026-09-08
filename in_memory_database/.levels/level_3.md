---

## Level 3 - TTL

### Assinaturas adicionadas
```python
class InMemoryDB:
    def set_with_ttl(self, timestamp: int, key: str, field: str, value: int, ttl: int) -> None:
        ...
```

### Requisitos

Define um valor com tempo de vida (TTL):
- O valor existe no intervalo semiaberto:
```text
timestamp <= t < timestamp + ttl
```
- Portanto, em `t >= timestamp + ttl`, o valor é considerado expirado.
- `get()`, `scan()` e `scan_by_prefix()` não podem retornar valores expirados.
- `delete()` trata um campo expirado como inexistente e retorna `False`.
- Um novo `set()` ou `set_with_ttl()` sobrescreve o valor anterior e sua regra de expiração.
- `set()` torna o novo valor permanente. A expiração de uma versão mais recente
  nunca faz uma versão anterior reaparecer.
