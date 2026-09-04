---

## Level 2 - Mediana

### Assinatura adicionada

```python
class IntegerContainer:
    def get_median(self) -> int | None: ...
```

### Requisitos

`get_median()`:
- Retorna `None` quando o contêiner está vazio.
- Caso contrário, considera os valores em ordem crescente.
- Com uma quantidade ímpar de valores, retorna o elemento central.
- Com uma quantidade par, retorna o menor dos dois elementos centrais.
- Não remove nem modifica valores do contêiner.
