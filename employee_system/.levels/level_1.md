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

`compensation` e timestamps são inteiros não negativos. Para cada funcionário,
os timestamps de `register()` são fornecidos em ordem não decrescente; timestamps
iguais são permitidos e podem formar um turno de duração zero. Não há garantia
de ordem cronológica global entre registros de funcionários diferentes.

`add_employee(employee_id, position, compensation)`:
- Adiciona um funcionário com sua posição e compensação por unidade de tempo.
- Retorna `False` se o funcionário já existir, sem alterar seus dados ou histórico;
  caso contrário `True`. O funcionário começa fora do escritório.

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
- Retorna `0` se o funcionário não tiver nenhum período finalizado.
- Se o funcionário não existir, retorna `None`.
