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

Cada usuário comum possui uma capacidade máxima, dada por um inteiro não negativo.
A capacidade usada é a soma dos tamanhos de todos os arquivos que lhe pertencem;
a restante é `capacity - capacidade_usada`. O limite pode ser atingido exatamente.
Os nomes dos arquivos são únicos em todo o sistema, independentemente do proprietário.

### Usuário especial `admin`

- `"admin"` é um proprietário reservado e implícito, disponível desde a criação do sistema.
- Arquivos criados por `add_file()`, inclusive nos níveis anteriores, pertencem a `"admin"`.
- Admin tem armazenamento ilimitado: seus arquivos e cópias não consomem quota de usuários comuns.
- **Garantia de entrada:** nenhum método que recebe `user_id` será chamado com `"admin"`,
  incluindo `add_user()`, `add_file_by()` e `update_capacity()`.
  Não é necessário definir um retorno de capacidade restante infinita.

### Operações de usuários

`add_user(user_id, capacity)`:
- IDs são únicos;
- Retorna `False` se já existir, sem alterar sua capacidade ou arquivos; caso contrário `True`.

`add_file_by(user_id, name, size)`:
- Adiciona um arquivo pertencente ao usuário;
- Não pode ultrapassar sua capacidade;
- Retorna a capacidade restante;
- Retorna `None` se o usuário não existir, o nome já estiver ocupado (por qualquer proprietário)
  ou não houver capacidade suficiente. A falha não cria arquivo nem consome capacidade.

`copy_file()` preserva o proprietário e cria um arquivo independente com o mesmo tamanho.
Não há usuário executor nessa assinatura: a cópia consome a capacidade do proprietário
do arquivo de origem. Retorna `False`, sem alterações, se a capacidade restante desse
proprietário for insuficiente, além das falhas já previstas no Level 1.
Cópias de arquivos de admin não têm limite de capacidade.
`get_file_size()` e `find_files()` continuam consultando arquivos de todos os proprietários.

### Redução de capacidade

`update_capacity(user_id, capacity)` substitui a capacidade máxima pelo novo valor;
não soma nem subtrai esse valor da capacidade anterior.

Se os arquivos pertencentes a esse usuário ultrapassarem a nova capacidade, remova
somente arquivos dele até que a soma dos tamanhos seja menor ou igual ao novo limite.
Arquivos de outros usuários e de admin não são afetados.

Remova primeiro:
1. Arquivo de maior tamanho;
2. Em caso de empate → nome lexicograficamente menor.

Retorne a quantidade de arquivos removidos (ou `None` se o usuário não existir).
Retorne `0` se nenhuma remoção for necessária. O novo limite permanece em vigor
para operações posteriores. Arquivos removidos deixam de aparecer nas consultas,
e seus nomes ficam disponíveis novamente.

Exemplo: um usuário com capacidade `500` e arquivos `/a(300)` e `/b(200)` passa
a ter capacidade `250`. Remova `/a`, retorne `1` e mantenha `/b`; sobram `50`
unidades de capacidade. Arquivos de admin permanecem intactos.
