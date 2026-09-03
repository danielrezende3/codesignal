# Mock 4 - Employee System

## Level 1 - Funcionários e horas

Implemente:

```python
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

```text
fora -> entrou
dentro -> saiu
```

- Retorne `"registered"` se a operação funcionar.
- Períodos ainda não finalizados não contam.
- Se o funcionário não existir, `get_worked_time` deve retornar `None`.

---

## Level 2 - Ranking

Adicione:

```python
top_n_employees(
    n: int,
    position: str
) -> list[str]
```

Formato:

```text
"<employee_id>(<worked_time>)"
```

Considere apenas funcionários cuja **posição atual** seja `position`.

Ordenação:

1. tempo trabalhado decrescente;
2. ID crescente.

---

## Level 3 - Promoções

Adicione:

```python
promote(
    employee_id: str,
    new_position: str,
    new_compensation: int,
    start_timestamp: int
) -> bool
```

Uma promoção fica **pendente**.

- Ela entra em vigor no primeiro `register()` realizado em ou depois de `start_timestamp`, desde que o funcionário esteja fora do escritório antes desse registro.
- Apenas uma promoção pode estar pendente por funcionário.
- Retorna `False` se o funcionário não existir ou já tiver uma promoção pendente.
- Horas anteriores continuam pertencendo à posição anterior; `top_n_employees()` considera somente a posição atual.

---

## Level 4 - Salário por período

Adicione:

```python
calc_salary(
    employee_id: str,
    start_timestamp: int,
    end_timestamp: int
) -> int | None
```

`compensation` representa pagamento **por unidade de tempo trabalhada**.

Calcule somente a interseção dos períodos efetivamente trabalhados com:

```text
[start_timestamp, end_timestamp)
```

e considere a remuneração vigente em cada período.
