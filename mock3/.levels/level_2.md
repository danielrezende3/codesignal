---

## Level 2 - Scan

### Assinaturas adicionadas
```python
class InMemoryDB:
    def scan(self, timestamp: int, key: str) -> list[str]:
        ...

    def scan_by_prefix(self, timestamp: int, key: str, prefix: str) -> list[str]:
        ...
```

### Requisitos

`scan(timestamp, key)`:
- Retorna todos os campos do registro `key`.

`scan_by_prefix(timestamp, key, prefix)`:
- Retorna todos os campos do registro `key` cujo nome comece com `prefix`.

Formato de retorno:
```text
"<field>(<value>)"
```

Ordenação:
- Sempre ordene os resultados lexicograficamente por `field`.
- Se o registro não existir ou não contiver campos correspondentes, retorne lista vazia `[]`.
