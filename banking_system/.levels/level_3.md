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

`transfer(timestamp, source, target, amount)`:
- `amount` é sempre um inteiro estritamente positivo, como nos pagamentos e depósitos.
- Retorna `None` se alguma conta não existir, se `source == target` ou se a origem
  não tiver saldo suficiente. A tentativa não cria transferência nem altera saldos.
- Em caso de sucesso, retira imediatamente `amount` do saldo disponível de `source`
  e mantém esse dinheiro reservado na transferência pendente; `target` ainda não recebe nada.
- Retorna o ID da transferência criada.
- O prazo é de **24 horas** (`86_400_000` unidades de timestamp, em milissegundos),
  com a regra de limite inclusivo descrita abaixo.

IDs gerados:
```text
transfer1
transfer2
transfer3
...
```
IDs são incrementados sequencialmente somente quando uma transferência é criada com sucesso.
O contador é global por instância do banco, compartilhado por todas as contas,
começa em `1` e não reutiliza IDs de transferências concluídas ou expiradas.

`accept_transfer(timestamp, account_id, transfer_id)`:
- Retorna `False` se a conta ou transferência não existir, se a conta não for o
  destinatário ou se a transferência já estiver aceita ou expirada.
- Em caso de sucesso, credita `amount` no destinatário e marca a transferência como
  aceita, retornando `True`. A origem não é debitada novamente.
- Uma tentativa por uma conta incorreta não consome a transferência nem impede
  uma aceitação válida posterior dentro do prazo.

Se expirar (`timestamp > transfer_timestamp + 86_400_000`):
- O dinheiro retorna automaticamente para `source`;
- A transferência não pode mais ser aceita.

A aceitação em `timestamp == transfer_timestamp + 86_400_000` ainda é válida.
Antes de **qualquer método** chamado com um timestamp, processe todas as
transferências pendentes já expiradas. O saldo devolvido deve estar disponível
para a própria operação solicitada, sem depender de uma tentativa de aceitação.
Esse processamento ocorre mesmo quando a operação solicitada falha; a falha
não desfaz os estornos automáticos nem causa outras alterações de saldo.
Cada transferência é devolvida no máximo uma vez. Transferências aceitas nunca
são devolvidas por expiração.

Transferências só contam como `outgoing` da conta de origem depois de aceitas.
O destinatário não acumula `outgoing` por recebê-las. Transferências pendentes
ou expiradas não contam; pagamentos bem-sucedidos continuam contando.
