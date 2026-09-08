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

`promote(employee_id, new_position, new_compensation, start_timestamp)` agenda uma promoção para o funcionário.

A promoção não altera imediatamente sua posição ou remuneração. Ela será aplicada na primeira **entrada no escritório** realizada com:

```text
timestamp >= start_timestamp
```

Ou seja, apenas uma chamada de `register()` feita enquanto o funcionário está fora pode ativar uma promoção.

Exemplo:

```text
register("alice", 80)       # entrada
promote("alice", "senior", 20, 100)

register("alice", 120)      # saída; promoção ainda não é aplicada
register("alice", 130)      # entrada; promoção é aplicada aqui
```

Regras:

* Retorne `False` se o funcionário não existir.
* Retorne `False` se já houver uma promoção aguardando ativação para esse funcionário.
* Caso contrário, agende a promoção e retorne `True`.
* Enquanto aguarda ativação, a promoção não altera a posição nem a remuneração atuais.
* Uma saída nunca ativa uma promoção.
* Quando uma entrada ativa a promoção:

  * `new_position` passa a ser a posição atual;
  * `new_compensation` passa a ser a remuneração atual;
  * a promoção deixa de estar aguardando ativação.
* Depois que uma promoção for ativada, outra promoção já pode ser agendada, inclusive antes da saída do turno atual.
* Se um funcionário já estiver dentro do escritório quando `start_timestamp` for alcançado, seu turno atual continua pertencendo à posição em que foi iniciado. A promoção será aplicada somente em uma entrada futura.
* `start_timestamp` não altera nem reprocessa registros anteriores. Ele apenas define o menor timestamp em que uma futura entrada pode ativar a promoção.
* `start_timestamp` é um limite de ativação, não o instante da chamada de `promote()`, e não precisa seguir a ordem dos timestamps de `register()`.
* `new_compensation` e `start_timestamp` são inteiros não negativos.
* É permitido:

  * manter o mesmo nome de posição e alterar apenas a remuneração;
  * retornar posteriormente para uma posição ocupada anteriormente.

### Ranking após promoções

Cada promoção ativada inicia uma nova etapa de trabalho para o funcionário.

`top_n_employees()` considera apenas o tempo trabalhado na **etapa atual** do funcionário.

Assim, quando uma promoção é ativada:

* o funcionário passa a aparecer no ranking da nova posição;
* seu tempo para esse ranking começa em `0`;
* períodos trabalhados em etapas anteriores não contam para o ranking atual;
* retornar futuramente para uma posição com o mesmo nome também inicia uma nova etapa.

`get_worked_time()` não é afetado por essa separação em etapas e continua retornando o total de todos os períodos finalizados do funcionário.

### Exemplo

```text
add_employee("alice", "junior", 10)

register("alice", 80)       # entra como junior

promote("alice", "senior", 20, 100)

register("alice", 120)      # sai
                            # turno 80-120 continua sendo junior

register("alice", 130)      # entra e ativa a promoção
                            # agora é senior

top_n_employees(1, "senior")
# ["alice(0)"]

register("alice", 150)      # sai após trabalhar 20 unidades como senior

top_n_employees(1, "senior")
# ["alice(20)"]

get_worked_time("alice")
# 60
```
