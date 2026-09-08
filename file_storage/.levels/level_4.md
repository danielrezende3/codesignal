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

Vale a garantia do Level 3: `user_id` nunca é `"admin"`. As duas operações
preservam o proprietário e atualizam a capacidade usada pelo novo tamanho.
Em qualquer falha, retorne `None` sem alterar nomes, tamanhos ou capacidade usada.

`compress_file(user_id, name)`:
- Usuário precisa existir;
- Arquivo precisa existir;
- Precisa pertencer ao usuário;
- Arquivo não pode já terminar em `.COMPRESSED`;
- O nome de destino `name + ".COMPRESSED"` não pode estar ocupado por nenhum arquivo;
- Novo tamanho é `size // 2`;
- Arquivo passa de `name` para `name.COMPRESSED`;
- Retorna a capacidade restante (ou `None` se falhar).

`decompress_file(user_id, name)`:
- Usuário e arquivo precisam existir, e o arquivo precisa pertencer ao usuário;
- Nome precisa terminar em `.COMPRESSED`;
- Tamanho dobra;
- Remove somente a última ocorrência do sufixo `.COMPRESSED`;
- Não pode ultrapassar quota;
- Nome original não pode estar ocupado;
- Retorna a capacidade restante (ou `None` se falhar).

Na descompressão, substitua o tamanho comprimido pelo tamanho dobrado ao verificar
a quota: `capacidade_usada - tamanho_atual + tamanho_atual * 2 <= capacity`.
Não remova outros arquivos para liberar espaço.

Nomes terminados em `.COMPRESSED` também podem ser criados por adição ou cópia;
não é necessário ter chamado `compress_file()` para poder descomprimi-los.
As operações usam apenas o tamanho atual. Assim, um arquivo de tamanho `101`
vira `50` ao comprimir e `100` ao descomprimir; o tamanho original não é restaurado.
