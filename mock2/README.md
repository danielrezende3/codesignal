# Mock 2 --- Banking System

Implemente um banco em memória.

Todos os métodos recebem `timestamp`, e as chamadas serão fornecidas em **ordem estritamente crescente de timestamp**.

## Level 1 --- Contas

```python
create_account(timestamp: int, account_id: str) -> bool

deposit(
    timestamp: int,
    account_id: str,
    amount: int
) -> int | None

pay(
    timestamp: int,
    account_id: str,
    amount: int
) -> int | None
```

`create_account` cria conta com saldo `0` e não permite ID duplicado.

`deposit` retorna o novo saldo.

`pay` retira dinheiro:

- saldo nunca pode ficar negativo;
- retorna novo saldo;
- retorna `None` em caso de falha.

---

## Level 2 --- Ranking

Adicione:

```python
top_spenders(timestamp: int, n: int) -> list[str]
```

Defina `outgoing` como todo dinheiro que efetivamente saiu de uma conta por `pay`.

Retorne:

```text
"<account_id>(<outgoing>)"
```

Ordenação:

1. `outgoing` decrescente;
2. account ID lexicograficamente crescente.

---

## Level 3 --- Transferências pendentes

Adicione:

```python
transfer(
    timestamp: int,
    source: str,
    target: str,
    amount: int
) -> str | None

accept_transfer(
    timestamp: int,
    account_id: str,
    transfer_id: str
) -> bool
```

Uma transferência:

- retira imediatamente o dinheiro da origem;
- fica pendente por **24 horas**;
- use `86_400_000` unidades de timestamp como 24h;
- somente `target` pode aceitar.

IDs:

```text
transfer1
transfer2
transfer3
...
```

IDs são incrementados somente quando uma transferência é criada com sucesso.

Se expirar:

- dinheiro retorna para `source`;
- transferência não pode mais ser aceita.

Transferências só contam como `outgoing` depois de aceitas.

---

## Level 4 --- Merge de contas

Adicione:

```python
merge_accounts(
    timestamp: int,
    target: str,
    source: str
) -> bool
```

Faça merge de `source` em `target`.

Regras:

- ambas precisam existir;
- não podem ser a mesma conta;
- saldo de `source` é adicionado a `target`;
- `outgoing` de ambas é somado;
- `source` deixa de existir.

Transferências pendentes envolvendo `source` devem passar a referenciar `target`.

Se isso fizer origem e destino da transferência se tornarem iguais, cancele a transferência e devolva o valor à conta resultante.
