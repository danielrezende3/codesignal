---

## Level 4 - Salário por período

### Assinaturas adicionadas
```python
class EmployeeSystem:
    def calc_salary(
        self,
        employee_id: str,
        start_timestamp: int,
        end_timestamp: int
    ) -> int | None:
        ...
```

### Requisitos

Calcula a remuneração devida ao funcionário no intervalo:
```text
[start_timestamp, end_timestamp)
```

Regras:
- `compensation` representa pagamento **por unidade de tempo trabalhada**.
- Calcule somente a interseção dos períodos efetivamente trabalhados com `[start_timestamp, end_timestamp)`.
- Considere a remuneração vigente em cada período de trabalho.
- Retorne `None` se o funcionário não existir.
