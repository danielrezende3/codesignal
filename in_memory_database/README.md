# In-Memory Database

Todos os métodos recebem um `timestamp` inteiro não negativo. As chamadas são
fornecidas em ordem **não decrescente de timestamp**, globalmente por instância:
uma chamada nunca tem timestamp menor que a anterior. Timestamps iguais são
permitidos; nesse caso, as operações são aplicadas na ordem das chamadas.
Não é necessário validar essa garantia nem tratar escritas fora de ordem.

## Level 1 - CRUD

Armazene dados no formato:
```text
record -> field -> value
```

### Assinaturas
```python
class InMemoryDB:
    def set(self, timestamp: int, key: str, field: str, value: int) -> None:
        ...

    def get(self, timestamp: int, key: str, field: str) -> int | None:
        ...

    def delete(self, timestamp: int, key: str, field: str) -> bool:
        ...
```

### Requisitos

`set(timestamp, key, field, value)`:
- Define ou atualiza o valor do campo `field` no registro `key`.

`get(timestamp, key, field)`:
- Retorna o valor de `field` no registro `key`.
- Retorna `None` se o registro ou o campo não existirem.

`delete(timestamp, key, field)`:
- Remove o campo `field` do registro `key`.
- Retorna `True` se o campo existia e foi removido.
- Retorna `False` se o registro ou o campo não existiam.

---
> 💡 Quando passar nos testes deste nível (`uv run sim test in_memory_database`), use `uv run sim next in_memory_database` para desbloquear o Level 2.
