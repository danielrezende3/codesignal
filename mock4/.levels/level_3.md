---

## Level 3 - Transferências pendentes

### Assinaturas adicionadas
```python
class BankingSystem:
    def transfer(self, timestamp: int, source: str, target: str, amount: int) -> str | None:
        ...

    def accept_transfer(self, timestamp: int, account_id: str, transfer_id: str) -> bool:
        ...
```

### Requisitos

Uma transferência:
- Retira imediatamente o dinheiro da conta de origem (`source`);
- Fica pendente por **24 horas** (`86_400_000` unidades de timestamp);
- Somente `target` pode aceitar (`account_id` deve ser igual a `target`).

IDs gerados:
```text
transfer1
transfer2
transfer3
...
```
IDs são incrementados sequencialmente somente quando uma transferência é criada com sucesso.

Se expirar (`timestamp > transfer_timestamp + 86_400_000`):
- O dinheiro retorna automaticamente para `source`;
- A transferência não pode mais ser aceita.

Transferências só contam como `outgoing` da conta de origem depois de aceitas.
