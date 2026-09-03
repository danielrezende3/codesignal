---

## Level 3 - Usuários e quotas

### Assinaturas adicionadas
```python
class FileStorage:
    def add_user(self, user_id: str, capacity: int) -> bool:
        ...

    def add_file_by(self, user_id: str, name: str, size: int) -> int | None:
        ...

    def update_capacity(self, user_id: str, capacity: int) -> int | None:
        ...
```

### Requisitos

Cada usuário possui uma capacidade máxima.

`add_user(user_id, capacity)`:
- IDs são únicos;
- Retorna `False` se já existir; caso contrário `True`.

`add_file_by(user_id, name, size)`:
- Adiciona um arquivo pertencente ao usuário;
- Não pode ultrapassar sua capacidade;
- Retorna a capacidade restante;
- Retorna `None` se falhar.

Arquivos criados por `add_file()` pertencem ao usuário especial `"admin"` e não contam para quotas.

`copy_file()` preserva o proprietário. Uma cópia realizada por usuário deve respeitar a quota do proprietário.

### Redução de capacidade

`update_capacity(user_id, capacity)` altera a capacidade máxima.

Se os arquivos existentes ultrapassarem a nova capacidade, remova arquivos até satisfazê-la.

Remova primeiro:
1. Arquivo de maior tamanho;
2. Em caso de empate → nome lexicograficamente menor.

Retorne a quantidade de arquivos removidos (ou `None` se o usuário não existir).
