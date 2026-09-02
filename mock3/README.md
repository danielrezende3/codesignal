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

- `scan()` e `scan_by_prefix()` não podem retornar valores expirados.
- Um novo `set`/`set_with_ttl` sobrescreve o valor anterior.

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
