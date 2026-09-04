# Employee System

## Level 1 - Funcionários e horas

### Assinaturas
```python
class EmployeeSystem:
    def add_employee(self, employee_id: str, position: str, compensation: int) -> bool:
        ...

    def register(self, employee_id: str, timestamp: int) -> str:
        ...

    def get_worked_time(self, employee_id: str) -> int | None:
        ...
```

### Requisitos

`add_employee(employee_id, position, compensation)`:
- Adiciona um funcionário com sua posição e compensação por unidade de tempo.
- Retorna `False` se o funcionário já existir; caso contrário `True`.

`register(employee_id, timestamp)` alterna o estado de presença do funcionário:
```text
fora -> entrou
dentro -> saiu
```
- Retorne `"registered"` se a operação funcionar.
- Retorne `""` se o funcionário não existir.
- Períodos ainda não finalizados (atualmente dentro) não contam para o tempo trabalhado.

`get_worked_time(employee_id)`:
- Retorna o tempo total trabalhado (soma de todos os intervalos `saiu - entrou`).
- Se o funcionário não existir, retorna `None`.

---
> 💡 Quando passar nos testes deste nível (`uv run sim test employee_system`), use `uv run sim next employee_system` para desbloquear o Level 2.
