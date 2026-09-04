---

## Level 2 - Ranking

### Assinaturas adicionadas
```python
class EmployeeSystem:
    def top_n_employees(self, n: int, position: str) -> list[str]:
        ...
```

### Requisitos

Retorne os `n` funcionários com maior tempo trabalhado na **posição atual** cuja
posição atual seja `position`.

Formato de retorno:
```text
"<employee_id>(<worked_time>)"
```

`worked_time` é o tempo acumulado exclusivamente na posição atual. Depois de
uma promoção, o tempo trabalhado nas posições anteriores não entra nesse valor.

Ordenação:
1. Tempo trabalhado decrescente;
2. `employee_id` lexicograficamente crescente.
