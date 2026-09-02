# Mock 3 --- In-Memory Database

## Level 1 --- CRUD

Armazene:

```text
record -> field -> value
```

Implemente:

```python
set(timestamp, key, field, value) -> None
get(timestamp, key, field) -> int | None
delete(timestamp, key, field) -> bool
```

### Critérios de aceite

```python
db.set(1, "user1", "age", 26)
db.set(2, "user1", "score", 100)

db.get(3, "user1", "age") == 26

db.delete(4, "user1", "age") == True
db.get(5, "user1", "age") is None
```

---

## Level 2 --- Scan

Adicione:

```python
scan(timestamp, key) -> list[str]

scan_by_prefix(
    timestamp,
    key,
    prefix
) -> list[str]
```

Formato:

```text
"<field>(<value>)"
```

Sempre ordene por `field` lexicograficamente.

### Critérios de aceite

Dado:

```text
user1:
    age = 26
    address = 10
    score = 100
```

Então:

```python
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

---

## Level 3 --- TTL

Adicione:

```python
set_with_ttl(
    timestamp,
    key,
    field,
    value,
    ttl
) -> None
```

O valor existe no intervalo:

```text
timestamp <= t < timestamp + ttl
```

Portanto:

```python
db.set_with_ttl(100, "A", "x", 42, 50)

db.get(149, "A", "x") == 42
db.get(150, "A", "x") is None
```

`scan()` e `scan_by_prefix()` também não podem retornar valores expirados.

Um novo `set`/`set_with_ttl` sobrescreve o valor anterior.

---

## Level 4 --- Consultas históricas

Adicione:

```python
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

- criação;
- sobrescrita;
- delete;
- TTL;
- recriação posterior.

### Critérios de aceite

```python
db.set(10, "A", "x", 100)
db.set_with_ttl(20, "A", "x", 200, 20)
db.set(50, "A", "x", 300)

db.get_at(100, "A", "x", 15) == 100
db.get_at(101, "A", "x", 25) == 200
db.get_at(102, "A", "x", 45) is None
db.get_at(103, "A", "x", 60) == 300
```
