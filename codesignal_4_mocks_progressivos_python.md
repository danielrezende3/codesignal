# CodeSignal --- 4 Mocks Progressivos em Python

Quatro simulados originais inspirados no formato de avaliações
progressivas do CodeSignal.

**Formato sugerido:** 90 minutos por mock.

> Cada nível inclui todos os requisitos dos níveis anteriores. As
> assinaturas indicadas devem ser mantidas.

------------------------------------------------------------------------

# Mock 1 --- File Storage

Implemente `FileStorage`, um sistema de armazenamento de arquivos em
memória.

## Level 1 --- Operações básicas

Implemente:

``` python
add_file(name: str, size: int) -> bool
get_file_size(name: str) -> int | None
copy_file(source: str, destination: str) -> bool
```

### Requisitos

`add_file(name, size)` adiciona um arquivo.

-   `name` é único.
-   Retorna `False` se já existir.
-   Caso contrário, adiciona e retorna `True`.

`get_file_size(name)`:

-   retorna o tamanho;
-   retorna `None` se não existir.

`copy_file(source, destination)`:

-   cria `destination` com o mesmo tamanho de `source`;
-   retorna `False` se `source` não existir;
-   retorna `False` se `destination` já existir;
-   caso contrário retorna `True`.

### Critérios de aceite

``` python
fs.add_file("/a.txt", 100)          == True
fs.add_file("/a.txt", 200)          == False
fs.get_file_size("/a.txt")          == 100
fs.get_file_size("/missing.txt")    is None

fs.copy_file("/a.txt", "/b.txt")    == True
fs.get_file_size("/b.txt")          == 100
fs.copy_file("/missing", "/c.txt")  == False
fs.copy_file("/a.txt", "/b.txt")    == False
```

## Level 2 --- Busca e ordenação

Adicione:

``` python
find_files(prefix: str, suffix: str) -> list[str]
```

Encontre arquivos cujo nome começa com `prefix` **e** termina com
`suffix`.

Retorne no formato:

``` text
"<name>(<size>)"
```

Ordenação:

1.  maior tamanho primeiro;
2.  em caso de empate, nome lexicograficamente crescente.

### Critérios de aceite

Dado:

``` python
fs.add_file("/docs/a.txt", 100)
fs.add_file("/docs/b.txt", 300)
fs.add_file("/docs/c.pdf", 500)
fs.add_file("/docs/d.txt", 300)
fs.add_file("/images/a.txt", 900)
```

Então:

``` python
fs.find_files("/docs", ".txt") == [
    "/docs/b.txt(300)",
    "/docs/d.txt(300)",
    "/docs/a.txt(100)",
]

fs.find_files("/nothing", ".txt") == []
```

## Level 3 --- Usuários e quotas

Adicione:

``` python
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

-   IDs são únicos;
-   retorna `False` se já existir.

`add_file_by`:

-   adiciona um arquivo pertencente ao usuário;
-   não pode ultrapassar sua capacidade;
-   retorna a capacidade restante;
-   retorna `None` se falhar.

Arquivos criados por `add_file()` pertencem ao usuário especial
`"admin"` e não contam para quotas.

`copy_file()` preserva o proprietário. Uma cópia realizada por usuário
deve respeitar a quota do proprietário.

### Redução de capacidade

`update_capacity()` altera a capacidade máxima.

Se os arquivos existentes ultrapassarem a nova capacidade, remova
arquivos até satisfazê-la.

Remova primeiro:

1.  arquivo de maior tamanho;
2.  empate → nome lexicograficamente menor.

Retorne a quantidade de arquivos removidos.

### Critérios de aceite

``` python
fs.add_user("daniel", 1000) == True
fs.add_user("daniel", 500)  == False

fs.add_file_by("daniel", "/a", 400) == 600
fs.add_file_by("daniel", "/b", 300) == 300
fs.add_file_by("daniel", "/c", 400) is None

fs.update_capacity("daniel", 500) == 1

fs.get_file_size("/a") is None
fs.get_file_size("/b") == 300
```

## Level 4 --- Compressão

Adicione:

``` python
compress_file(user_id: str, name: str) -> int | None
decompress_file(user_id: str, name: str) -> int | None
```

`compress_file()`:

-   arquivo precisa existir;
-   precisa pertencer ao usuário;
-   arquivo não pode já terminar em `.COMPRESSED`;
-   novo tamanho é `size // 2`;
-   arquivo passa de `name` para `name.COMPRESSED`;
-   retorna a capacidade restante.

`decompress_file()` realiza o inverso:

-   nome precisa terminar em `.COMPRESSED`;
-   tamanho dobra;
-   remove `.COMPRESSED`;
-   não pode ultrapassar quota;
-   nome original não pode estar ocupado.

### Critérios de aceite

``` python
fs.add_user("u1", 1000)
fs.add_file_by("u1", "/movie", 600)

fs.compress_file("u1", "/movie") == 700
fs.get_file_size("/movie") is None
fs.get_file_size("/movie.COMPRESSED") == 300

fs.decompress_file("u1", "/movie.COMPRESSED") == 400
fs.get_file_size("/movie") == 600
```

------------------------------------------------------------------------

# Mock 2 --- Banking System

Implemente um banco em memória.

Todos os métodos recebem `timestamp`, e as chamadas serão fornecidas em
**ordem estritamente crescente de timestamp**.

## Level 1 --- Contas

``` python
create_account(timestamp: int, account_id: str) -> bool

deposit(
    timestamp: int,
    account_id: str,
    amount: int
) -> int | None

pay(
    timestamp: int,
    account_id: str,
    amount: int
) -> int | None
```

`create_account` cria conta com saldo `0` e não permite ID duplicado.

`deposit` retorna o novo saldo.

`pay` retira dinheiro:

-   saldo nunca pode ficar negativo;
-   retorna novo saldo;
-   retorna `None` em caso de falha.

### Critérios de aceite

``` python
bank.create_account(1, "A") == True
bank.create_account(2, "A") == False

bank.deposit(3, "A", 1000) == 1000
bank.pay(4, "A", 300) == 700
bank.pay(5, "A", 800) is None
```

## Level 2 --- Ranking

Adicione:

``` python
top_spenders(timestamp: int, n: int) -> list[str]
```

Defina `outgoing` como todo dinheiro que efetivamente saiu de uma conta
por `pay`.

Retorne:

``` text
"<account_id>(<outgoing>)"
```

Ordenação:

1.  `outgoing` decrescente;
2.  account ID lexicograficamente crescente.

### Critérios de aceite

Se:

``` text
A: outgoing = 500
B: outgoing = 900
C: outgoing = 500
```

Então:

``` python
bank.top_spenders(100, 3) == [
    "B(900)",
    "A(500)",
    "C(500)",
]
```

## Level 3 --- Transferências pendentes

Adicione:

``` python
transfer(
    timestamp: int,
    source: str,
    target: str,
    amount: int
) -> str | None

accept_transfer(
    timestamp: int,
    account_id: str,
    transfer_id: str
) -> bool
```

Uma transferência:

-   retira imediatamente o dinheiro da origem;
-   fica pendente por **24 horas**;
-   use `86_400_000` unidades de timestamp como 24h;
-   somente `target` pode aceitar.

IDs:

``` text
transfer1
transfer2
transfer3
...
```

IDs são incrementados somente quando uma transferência é criada com
sucesso.

Se expirar:

-   dinheiro retorna para `source`;
-   transferência não pode mais ser aceita.

Transferências só contam como `outgoing` depois de aceitas.

### Critérios de aceite

``` python
bank.create_account(1, "A")
bank.create_account(2, "B")
bank.deposit(3, "A", 1000)

tid = bank.transfer(4, "A", "B", 400)

tid == "transfer1"

bank.accept_transfer(5, "B", "transfer1") == True
```

Após a aceitação:

``` text
A.balance = 600
B.balance = 400
A.outgoing = 400
```

## Level 4 --- Merge de contas

Adicione:

``` python
merge_accounts(
    timestamp: int,
    target: str,
    source: str
) -> bool
```

Faça merge de `source` em `target`.

Regras:

-   ambas precisam existir;
-   não podem ser a mesma conta;
-   saldo de `source` é adicionado a `target`;
-   `outgoing` de ambas é somado;
-   `source` deixa de existir.

Transferências pendentes envolvendo `source` devem passar a referenciar
`target`.

Se isso fizer origem e destino da transferência se tornarem iguais,
cancele a transferência e devolva o valor à conta resultante.

### Critérios de aceite

Antes:

``` text
A:
balance = 700
outgoing = 300

B:
balance = 400
outgoing = 200
```

Após:

``` python
bank.merge_accounts(100, "A", "B") == True
```

deve resultar em:

``` text
A.balance  = 1100
A.outgoing = 500

B não existe
```

------------------------------------------------------------------------

# Mock 3 --- In-Memory Database

## Level 1 --- CRUD

Armazene:

``` text
record -> field -> value
```

Implemente:

``` python
set(timestamp, key, field, value) -> None
get(timestamp, key, field) -> int | None
delete(timestamp, key, field) -> bool
```

### Critérios de aceite

``` python
db.set(1, "user1", "age", 26)
db.set(2, "user1", "score", 100)

db.get(3, "user1", "age") == 26

db.delete(4, "user1", "age") == True
db.get(5, "user1", "age") is None
```

## Level 2 --- Scan

Adicione:

``` python
scan(timestamp, key) -> list[str]

scan_by_prefix(
    timestamp,
    key,
    prefix
) -> list[str]
```

Formato:

``` text
"<field>(<value>)"
```

Sempre ordene por `field` lexicograficamente.

### Critérios de aceite

Dado:

``` text
user1:
    age = 26
    address = 10
    score = 100
```

Então:

``` python
db.scan(10, "user1") == [
    "address(10)",
    "age(26)",
    "score(100)",
]

db.scan_by_prefix(10, "user1", "a") == [
    "address(10)",
    "age(26)",
]
```

## Level 3 --- TTL

Adicione:

``` python
set_with_ttl(
    timestamp,
    key,
    field,
    value,
    ttl
) -> None
```

O valor existe no intervalo:

``` text
timestamp <= t < timestamp + ttl
```

Portanto:

``` python
db.set_with_ttl(100, "A", "x", 42, 50)

db.get(149, "A", "x") == 42
db.get(150, "A", "x") is None
```

`scan()` e `scan_by_prefix()` também não podem retornar valores
expirados.

Um novo `set`/`set_with_ttl` sobrescreve o valor anterior.

## Level 4 --- Consultas históricas

Adicione:

``` python
get_at(
    timestamp: int,
    key: str,
    field: str,
    at_timestamp: int
) -> int | None
```

A pergunta agora é:

> Qual era o valor desse campo em `at_timestamp`?

Considere:

-   criação;
-   sobrescrita;
-   delete;
-   TTL;
-   recriação posterior.

### Critérios de aceite

``` python
db.set(10, "A", "x", 100)
db.set_with_ttl(20, "A", "x", 200, 20)
db.set(50, "A", "x", 300)

db.get_at(100, "A", "x", 15) == 100
db.get_at(101, "A", "x", 25) == 200
db.get_at(102, "A", "x", 45) is None
db.get_at(103, "A", "x", 60) == 300
```

------------------------------------------------------------------------

# Mock 4 --- Employee System

## Level 1 --- Funcionários e horas

Implemente:

``` python
add_employee(
    employee_id: str,
    position: str,
    compensation: int
) -> bool

register(
    employee_id: str,
    timestamp: int
) -> str

get_worked_time(employee_id: str) -> int | None
```

`register` alterna:

``` text
fora -> entrou
dentro -> saiu
```

Retorne `"registered"` se a operação funcionar.

### Critérios de aceite

``` python
hr.add_employee("A", "developer", 100) == True
hr.add_employee("A", "manager", 200) == False

hr.register("A", 10)
hr.register("A", 50)

hr.get_worked_time("A") == 40
```

Períodos ainda não finalizados não contam.

## Level 2 --- Ranking

Adicione:

``` python
top_n_employees(
    n: int,
    position: str
) -> list[str]
```

Formato:

``` text
"<employee_id>(<worked_time>)"
```

Considere apenas funcionários cuja **posição atual** seja `position`.

Ordenação:

1.  tempo trabalhado decrescente;
2.  ID crescente.

### Critérios de aceite

Se:

``` text
A developer: 50 unidades trabalhadas
B developer: 80 unidades trabalhadas
C manager:   300 unidades trabalhadas
```

Então:

``` python
hr.top_n_employees(2, "developer") == [
    "B(80)",
    "A(50)",
]
```

## Level 3 --- Promoções

Adicione:

``` python
promote(
    employee_id: str,
    new_position: str,
    new_compensation: int,
    start_timestamp: int
) -> bool
```

Uma promoção fica **pendente**.

Ela entra em vigor no primeiro `register()` realizado em ou depois de
`start_timestamp`, desde que o funcionário esteja fora do escritório
antes desse registro.

Apenas uma promoção pode estar pendente por funcionário.

### Exemplo

``` text
posição = junior

promote(A, senior, 200, timestamp=100)

register(A, 80)
register(A, 90)

posição continua junior

register(A, 110)

posição passa a senior
```

### Critérios de aceite

-   funcionário inexistente → `False`;
-   promoção já pendente → `False`;
-   caso contrário → `True`;
-   horas anteriores continuam pertencendo à posição anterior;
-   `top_n_employees()` considera somente a posição atual.

## Level 4 --- Salário por período

Adicione:

``` python
calc_salary(
    employee_id: str,
    start_timestamp: int,
    end_timestamp: int
) -> int | None
```

`compensation` representa pagamento **por unidade de tempo trabalhada**.

Calcule somente a interseção dos períodos efetivamente trabalhados com:

``` text
[start_timestamp, end_timestamp)
```

e considere a remuneração vigente em cada período.

### Exemplo

Funcionário trabalha:

``` text
10 --------- 30
compensation = 5

50 ----------------- 80
compensation = 10
```

Consulta:

``` python
calc_salary("A", 20, 60)
```

Cálculo:

``` text
[20,30) = 10
10 * 5 = 50

[50,60) = 10
10 * 10 = 100

Total = 150
```

### Critérios de aceite

Também deve funcionar quando:

-   consulta começa no meio de um turno;
-   consulta termina no meio de um turno;
-   existem várias promoções históricas;
-   não existe trabalho no intervalo;
-   funcionário não existe;
-   há turno atualmente aberto --- a parte aberta não conta.

------------------------------------------------------------------------

# Estratégia de treino

Trate os quatro mocks como **quatro provas separadas**, não como 16
exercícios.

  Simulado             Principal habilidade                   Dificuldade
  -------------------- -------------------------------------- -------------
  In-Memory Database   `dict` → TTL → histórico               ★★★
  File Storage         estado → ranking → ownership           ★★★
  Employee System      intervalos + mudança de estado         ★★★★
  Banking System       estado + operações pendentes + merge   ★★★★

## Ordem recomendada

1.  In-Memory Database
2.  File Storage
3.  Employee System
4.  Banking System

## Método

Para cada mock:

1.  Reserve **90 minutos**.
2.  Comece vendo somente o **Level 1**.
3.  Implemente e teste.
4.  Só então revele o **Level 2**.
5.  Repita para Levels 3 e 4.
6.  Todos os testes dos níveis anteriores devem continuar passando.

Uma divisão inicial de tempo pode ser:

``` text
Level 1     15 min
Level 2     15 min
Level 3     25 min
Level 4     25 min
Debug       10 min
------------------
Total       90 min
```

A progressão deliberada força a refatoração das estruturas de dados
conforme novos requisitos aparecem, aproximando o treino do formato de
uma avaliação progressiva.
