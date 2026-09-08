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
- Calcule somente a interseção dos turnos finalizados com `[start_timestamp, end_timestamp)`.
  Turnos ainda abertos não contribuem, mesmo que a consulta termine depois da entrada.
- Cada turno é o intervalo semiaberto `[entrada, saída)` e usa, em toda sua duração,
  a remuneração vigente na entrada. Promoções não alteram turnos anteriores nem
  dividem a remuneração de um turno que atravessa o horário agendado.
- Retorne `None` se o funcionário não existir.
- Para um funcionário existente, retorne `0` se `start_timestamp >= end_timestamp`
  ou se nenhum turno finalizado tiver interseção de duração positiva com a consulta.
- Consultas não alteram registros nem ativam promoções; podem consultar qualquer
  período, sem precisar seguir a ordem dos timestamps de `register()`.
