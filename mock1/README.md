# Mock 1 - File Storage

Implemente `FileStorage`, um sistema de armazenamento de arquivos em memória.

## Level 1 - Operações básicas

Implemente:

```python
add_file(name: str, size: int) -> bool
get_file_size(name: str) -> int | None
copy_file(source: str, destination: str) -> bool
```

### Requisitos

`add_file(name, size)` adiciona um arquivo.

- `name` é único.
- Retorna `False` se já existir.
- Caso contrário, adiciona e retorna `True`.

`get_file_size(name)`:

- retorna o tamanho;
- retorna `None` se não existir.

`copy_file(source, destination)`:

- cria `destination` com o mesmo tamanho de `source`;
- retorna `False` se `source` não existir;
- retorna `False` se `destination` já existir;
- caso contrário retorna `True`.

## Level 2 - Busca e ordenação

Adicione:

```python
find_files(prefix: str, suffix: str) -> list[str]
```

Encontre arquivos cujo nome começa com `prefix` **e** termina com `suffix`.

Retorne no formato:

```text
"<name>(<size>)"
```

Ordenação:

1. maior tamanho primeiro;
2. em caso de empate, nome lexicograficamente crescente.

## Level 3 - Usuários e quotas

Adicione:

```python
add_user(user_id: str, capacity: int) -> bool

add_file_by(
    user_id: str,
    name: str,
    size: int
) -> int | None

update_capacity(
    user_id: str,
    capacity: int
) -> int | None
```

Cada usuário possui uma capacidade máxima.

`add_user`:

- IDs são únicos;
- retorna `False` se já existir.

`add_file_by`:

- adiciona um arquivo pertencente ao usuário;
- não pode ultrapassar sua capacidade;
- retorna a capacidade restante;
- retorna `None` se falhar.

Arquivos criados por `add_file()` pertencem ao usuário especial `"admin"` e não contam para quotas.

`copy_file()` preserva o proprietário. Uma cópia realizada por usuário deve respeitar a quota do proprietário.

### Redução de capacidade

`update_capacity()` altera a capacidade máxima.

Se os arquivos existentes ultrapassarem a nova capacidade, remova arquivos até satisfazê-la.

Remova primeiro:

1. arquivo de maior tamanho;
2. empate → nome lexicograficamente menor.

Retorne a quantidade de arquivos removidos.

## Level 4 - Compressão

Adicione:

```python
compress_file(user_id: str, name: str) -> int | None
decompress_file(user_id: str, name: str) -> int | None
```

`compress_file()`:

- arquivo precisa existir;
- precisa pertencer ao usuário;
- arquivo não pode já terminar em `.COMPRESSED`;
- novo tamanho é `size // 2`;
- arquivo passa de `name` para `name.COMPRESSED`;
- retorna a capacidade restante.

`decompress_file()` realiza o inverso:

- nome precisa terminar em `.COMPRESSED`;
- tamanho dobra;
- remove `.COMPRESSED`;
- não pode ultrapassar quota;
- nome original não pode estar ocupado.
