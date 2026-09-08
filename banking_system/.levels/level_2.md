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
Depósitos e pagamentos que falharam não aumentam esse total.

Retorne os `n` maiores pagadores no formato:
```text
"<account_id>(<outgoing>)"
```

Inclua contas com `outgoing == 0`. `n` é um inteiro não negativo; retorne no
máximo `n` contas existentes. Se houver menos contas, retorne todas. Retorne `[]`
se `n == 0` ou não houver contas.

Ordenação:
1. `outgoing` decrescente;
2. `account_id` lexicograficamente crescente.
