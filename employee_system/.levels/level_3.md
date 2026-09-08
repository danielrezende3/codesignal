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
- Enquanto pendente, não altera a posição nem a remuneração vigente.
- Na entrada que ativa a promoção, a posição e a remuneração mudam imediatamente,
  e a promoção deixa de estar pendente. Já é possível agendar outra promoção,
  mesmo antes da saída desse novo turno.
- Uma saída nunca ativa a promoção. Se um turno começou antes de `start_timestamp`,
  todo esse turno mantém a posição e a remuneração da entrada, mesmo que termine depois.
- `new_compensation` e `start_timestamp` são inteiros não negativos.
  `start_timestamp` é um limite para uma entrada futura, não uma alteração retroativa:
  registros já realizados não são reprocessados.
- É permitido manter o mesmo nome de posição e alterar somente a remuneração,
  assim como retornar a uma posição ocupada anteriormente.
- Cada ativação inicia uma nova etapa: o tempo usado por `top_n_employees()` volta
  a zero, mesmo se o nome da posição se repetir. Tempos de etapas anteriores
  não são recuperados ao retornar a uma posição.
- `get_worked_time()` continua somando todos os turnos finalizados, incluindo
  todas as etapas anteriores. O histórico desses turnos deve ser preservado.

Exemplo: um funcionário entra como junior em `80`, com promoção prevista para
`100`, e sai em `120`. Essas `40` unidades continuam sendo de junior. Ao entrar
em `130`, passa à nova posição e aparece no ranking dela com tempo `0` até sair.
