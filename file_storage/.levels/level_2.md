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

Prefixo ou sufixo vazio corresponde a qualquer nome nesse critério. Os dois
critérios podem se sobrepor no nome. Retorne `[]` se não houver correspondências.

Retorne no formato:
```text
"<name>(<size>)"
```

Ordenação:
1. Maior tamanho primeiro;
2. Em caso de empate, nome lexicograficamente crescente.
