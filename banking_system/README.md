# Banking System

Implemente um banco em memória.

Todos os métodos recebem `timestamp`, e as chamadas serão fornecidas em **ordem estritamente crescente de timestamp**.

A garantia é global por instância, incluindo chamadas que falham. Não é
necessário validar timestamps nem tratar operações fora de ordem.

## Level 1 - Contas

### Assinaturas
```python
class BankingSystem:
    def create_account(self, timestamp: int, account_id: str) -> bool:
        ...

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        ...

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        ...
```

### Requisitos

Os timestamps são inteiros não negativos, em ordem estritamente crescente entre
todas as chamadas, como indicado no cabeçalho. `amount` é sempre um inteiro
estritamente positivo; não é necessário tratar valores zero ou negativos.
Operações que falham não alteram contas ou saldos.

`create_account(timestamp, account_id)`:
- Cria conta com saldo `0`.
- Não permite ID duplicado (retorna `False` se já existir; caso contrário `True`).

`deposit(timestamp, account_id, amount)`:
- Adiciona `amount` ao saldo da conta.
- Retorna o novo saldo.
- Retorna `None` se a conta não existir.

`pay(timestamp, account_id, amount)`:
- Retira dinheiro da conta.
- Saldo nunca pode ficar negativo.
- Retorna o novo saldo em caso de sucesso.
- Retorna `None` se a conta não existir ou se não houver saldo suficiente.

---
> 💡 Quando passar nos testes deste nível (`uv run sim test banking_system`), use `uv run sim next banking_system` para desbloquear o Level 2.
