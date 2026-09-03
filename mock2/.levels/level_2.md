---

## Level 2 - Ranking

### Assinaturas adicionadas
```python
class BankingSystem:
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        ...
```

### Requisitos

Defina `outgoing` como todo dinheiro que efetivamente saiu de uma conta por `pay`.

Retorne os `n` maiores pagadores no formato:
```text
"<account_id>(<outgoing>)"
```

Ordenação:
1. `outgoing` decrescente;
2. `account_id` lexicograficamente crescente.
