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

Retorne `True` em caso de sucesso. Retorne `False` se alguma conta não existir
ou se os IDs forem iguais, sem realizar o merge. Como nos demais métodos,
processe primeiro as expirações pendentes usando o timestamp da chamada.

Regras:
- Ambas as contas precisam existir;
- Não podem ser a mesma conta;
- O saldo de `source` é adicionado a `target`;
- O `outgoing` de ambas é somado em `target`;
- `source` deixa de existir e não aparece mais em `top_spenders()`.
  Operações com esse ID passam a falhar como para qualquer conta inexistente.

Transferências pendentes envolvendo `source` devem passar a referenciar `target`.
Isso vale tanto para a origem quanto para o destinatário das transferências.
Preserve ID, valor e timestamp de criação: o prazo de expiração não reinicia.
Uma aceitação futura usa o destinatário atualizado e contabiliza `outgoing` na
origem atualizada; uma expiração futura devolve o dinheiro à origem atualizada.
Transferências pendentes que não envolvem `source` continuam como estavam.

Se isso fizer origem e destino da transferência se tornarem iguais, cancele a transferência e devolva o valor à conta resultante (`target`).
Esse cancelamento não aumenta `outgoing`; a transferência não pode ser aceita
nem devolvida novamente por expiração. Transferências já aceitas não são desfeitas.

Merges podem ser encadeados, aplicando as mesmas regras a cada chamada.
É permitido recriar posteriormente o ID removido com `create_account()`: será
uma conta nova, com saldo e `outgoing` em zero. Transferências redirecionadas no
merge permanecem ligadas à conta resultante e não voltam para o ID recriado.
