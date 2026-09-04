# Integer Container

Implemente `IntegerContainer`, um contêiner em memória que armazena números inteiros.

## Level 1 - Operações básicas

### Assinaturas

```python
class IntegerContainer:
    def add(self, value: int) -> int: ...

    def delete(self, value: int) -> bool: ...
```

### Requisitos

`add(value)`:
- Adiciona uma ocorrência de `value` ao contêiner.
- Valores duplicados são permitidos.
- Retorna a quantidade total de números após a adição.

`delete(value)`:
- Remove uma única ocorrência de `value`.
- Retorna `True` quando uma ocorrência foi removida.
- Retorna `False` quando o valor não está presente.

---
> 💡 Quando passar nos testes deste nível (`uv run sim test integer_container`), use `uv run sim next integer_container` para desbloquear o Level 2.
