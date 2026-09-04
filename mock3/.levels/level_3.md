---

## Level 3 - Promoções

### Assinaturas adicionadas
```python
class EmployeeSystem:
    def promote(
        self,
        employee_id: str,
        new_position: str,
        new_compensation: int,
        start_timestamp: int
    ) -> bool:
        ...
```

### Requisitos

Uma promoção fica **pendente**:
- Ela entra em vigor no primeiro `register()` realizado em ou depois de `start_timestamp`, desde que o funcionário esteja fora do escritório antes desse registro.
- Apenas uma promoção pode estar pendente por funcionário.
- Retorna `False` se o funcionário não existir ou já tiver uma promoção pendente; caso contrário `True`.
- Horas anteriores continuam pertencendo à posição anterior; `top_n_employees()`
  considera somente as horas trabalhadas na posição atual.
