# File Storage

Implemente `FileStorage`, um sistema de armazenamento de arquivos em memória.

Os métodos não recebem timestamps. As operações são aplicadas sequencialmente
na ordem das chamadas.

## Level 1 - Operações básicas

### Assinaturas
```python
class FileStorage:
    def add_file(self, name: str, size: int) -> bool:
        ...

    def get_file_size(self, name: str) -> int | None:
        ...

    def copy_file(self, source: str, destination: str) -> bool:
        ...
```

### Requisitos

Os nomes são strings comparadas exatamente como recebidas, sem normalização de
caminhos. `size` é um inteiro não negativo; arquivos de tamanho zero são válidos.
Operações que falham não alteram os arquivos existentes.

`add_file(name, size)` adiciona um arquivo:
- `name` é único.
- Retorna `False` se já existir.
- Caso contrário, adiciona e retorna `True`.

`get_file_size(name)`:
- Retorna o tamanho do arquivo;
- Retorna `None` se não existir.

`copy_file(source, destination)`:
- Cria `destination` com o mesmo tamanho de `source`;
- Retorna `False` se `source` não existir;
- Retorna `False` se `destination` já existir;
- Caso contrário retorna `True`.

---
> 💡 Quando passar nos testes deste nível (`uv run sim test file_storage`), use `uv run sim next file_storage` para desbloquear o Level 2.
