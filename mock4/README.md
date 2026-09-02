# Mock 4 --- Employee System

## Level 1 --- Funcionários e horas

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

Retorne `"registered"` se a operação funcionar.

### Critérios de aceite

```python
hr.add_employee("A", "developer", 100) == True
hr.add_employee("A", "manager", 200) == False

hr.register("A", 10)
hr.register("A", 50)

hr.get_worked_time("A") == 40
```

Períodos ainda não finalizados não contam.

---

## Level 2 --- Ranking

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

### Critérios de aceite

Se:

```text
A developer: 50 unidades trabalhadas
B developer: 80 unidades trabalhadas
C manager:   300 unidades trabalhadas
```

Então:

```python
hr.top_n_employees(2, "developer") == [
    "B(80)",
    "A(50)",
]
```

---

## Level 3 --- Promoções

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

Ela entra em vigor no primeiro `register()` realizado em ou depois de `start_timestamp`, desde que o funcionário esteja fora do escritório antes desse registro.

Apenas uma promoção pode estar pendente por funcionário.

### Exemplo

```text
posição = junior

promote(A, senior, 200, timestamp=100)

register(A, 80)
register(A, 90)

posição continua junior

register(A, 110)

posição passa a senior
```

### Critérios de aceite

- funcionário inexistente → `False`;
- promoção já pendente → `False`;
- caso contrário → `True`;
- horas anteriores continuam pertencendo à posição anterior;
- `top_n_employees()` considera somente a posição atual.

---

## Level 4 --- Salário por período

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

### Exemplo

Funcionário trabalha:

```text
10 --------- 30
compensation = 5

50 ----------------- 80
compensation = 10
```

Consulta:

```python
calc_salary("A", 20, 60)
```

Cálculo:

```text
[20,30) = 10
10 * 5 = 50

[50,60) = 10
10 * 10 = 100

Total = 150
```

### Critérios de aceite

Também deve funcionar quando:

- consulta começa no meio de um turno;
- consulta termina no meio de um turno;
- existem várias promoções históricas;
- não existe trabalho no intervalo;
- funcionário não existe;
- há turno atualmente aberto --- a parte aberta não conta.
```,Description:
