---

## Level 2 - Ranking

### Assinaturas adicionadas
```python
class EmployeeSystem:
    def top_n_employees(self, n: int, position: str) -> list[str]:
        ...
```

### Requisitos

Retorne os `n` funcionários com maior tempo trabalhado cuja **posição atual** seja `position`.

Formato de retorno:
```text
"<employee_id>(<worked_time>)"
```

Ordenação:
1. Tempo trabalhado decrescente;
2. `employee_id` lexicograficamente crescente.
