---

## Level 2 - Busca e ordenação

### Assinaturas adicionadas
```python
class FileStorage:
    def find_files(self, prefix: str, suffix: str) -> list[str]:
        ...
```

### Requisitos

Encontre arquivos cujo nome começa com `prefix` **e** termina com `suffix`.

Retorne no formato:
```text
"<name>(<size>)"
```

Ordenação:
1. Maior tamanho primeiro;
2. Em caso de empate, nome lexicograficamente crescente.
