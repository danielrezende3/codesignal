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

`worked_time` soma somente os períodos finalizados pelo funcionário nessa posição.

Inclua funcionários com tempo `0`, inclusive aqueles com um período ainda aberto.
`n` é um inteiro não negativo. Retorne no máximo `n` resultados; se houver menos
funcionários na posição, retorne todos eles. Retorne `[]` quando `n == 0` ou
nenhum funcionário tiver a posição solicitada.

Ordenação:
1. Tempo trabalhado decrescente;
2. `employee_id` lexicograficamente crescente.
