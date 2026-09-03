---

## Level 4 - Compressão

### Assinaturas adicionadas
```python
class FileStorage:
    def compress_file(self, user_id: str, name: str) -> int | None:
        ...

    def decompress_file(self, user_id: str, name: str) -> int | None:
        ...
```

### Requisitos

`compress_file(user_id, name)`:
- Arquivo precisa existir;
- Precisa pertencer ao usuário;
- Arquivo não pode já terminar em `.COMPRESSED`;
- Novo tamanho é `size // 2`;
- Arquivo passa de `name` para `name.COMPRESSED`;
- Retorna a capacidade restante (ou `None` se falhar).

`decompress_file(user_id, name)` realiza o inverso:
- Nome precisa terminar em `.COMPRESSED`;
- Tamanho dobra;
- Remove `.COMPRESSED`;
- Não pode ultrapassar quota;
- Nome original não pode estar ocupado;
- Retorna a capacidade restante (ou `None` se falhar).
