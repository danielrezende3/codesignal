---

## Level 4 - Merge de contas

### Assinaturas adicionadas
```python
class BankingSystem:
    def merge_accounts(self, timestamp: int, target: str, source: str) -> bool:
        ...
```

### Requisitos

Faça o merge de `source` em `target`.

Regras:
- Ambas as contas precisam existir;
- Não podem ser a mesma conta;
- O saldo de `source` é adicionado a `target`;
- O `outgoing` de ambas é somado em `target`;
- `source` deixa de existir.

Transferências pendentes envolvendo `source` devem passar a referenciar `target`.

Se isso fizer origem e destino da transferência se tornarem iguais, cancele a transferência e devolva o valor à conta resultante (`target`).
