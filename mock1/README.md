# Mock 1 --- File Storage

Implemente `FileStorage`, um sistema de armazenamento de arquivos em memória.

## Level 1 --- Operações básicas

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

### Critérios de aceite

```python
fs.add_file("/a.txt", 100)          == True
fs.add_file("/a.txt", 200)          == False
fs.get_file_size("/a.txt")          == 100
fs.get_file_size("/missing.txt")    is None

fs.copy_file("/a.txt", "/b.txt")    == True
fs.get_file_size("/b.txt")          == 100
fs.copy_file("/missing", "/c.txt")  == False
fs.copy_file("/a.txt", "/b.txt")    == False
```

---

## Level 2 --- Busca e ordenação

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

### Critérios de aceite

Dado:

```python
fs.add_file("/docs/a.txt", 100)
fs.add_file("/docs/b.txt", 300)
fs.add_file("/docs/c.pdf", 500)
fs.add_file("/docs/d.txt", 300)
fs.add_file("/images/a.txt", 900)
```

Então:

```python
fs.find_files("/docs", ".txt") == [
    "/docs/b.txt(300)",
    "/docs/d.txt(300)",
    "/docs/a.txt(100)",
]

fs.find_files("/nothing", ".txt") == []
```

---

## Level 3 --- Usuários e quotas

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

### Critérios de aceite

```python
fs.add_user("daniel", 1000) == True
fs.add_user("daniel", 500)  == False

fs.add_file_by("daniel", "/a", 400) == 600
fs.add_file_by("daniel", "/b", 300) == 300
fs.add_file_by("daniel", "/c", 400) is None

fs.update_capacity("daniel", 500) == 1

fs.get_file_size("/a") is None
fs.get_file_size("/b") == 300
```

---

## Level 4 --- Compressão

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

### Critérios de aceite

```python
fs.add_user("u1", 1000)
fs.add_file_by("u1", "/movie", 600)

fs.compress_file("u1", "/movie") == 700
fs.get_file_size("/movie") is None
fs.get_file_size("/movie.COMPRESSED") == 300

fs.decompress_file("u1", "/movie.COMPRESSED") == 400
fs.get_file_size("/movie") == 600
```
