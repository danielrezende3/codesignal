# CodeSignal --- 4 Mocks Progressivos em Python

Quatro simulados originais inspirados no formato de avaliações progressivas do CodeSignal.

**Formato sugerido:** 90 minutos por mock.

> Cada nível inclui todos os requisitos dos níveis anteriores. As assinaturas indicadas devem ser mantidas.

---

## 📂 Estrutura dos Mocks

| Pasta | Simulado | Principal habilidade | Dificuldade |
| :--- | :--- | :--- | :--- |
| [**mock1/**](./mock1/README.md) | File Storage | Estado → ranking → ownership | ★★★ |
| [**mock2/**](./mock2/README.md) | Banking System | Estado + operações pendentes + merge | ★★★★ |
| [**mock3/**](./mock3/README.md) | In-Memory Database | `dict` → TTL → histórico | ★★★ |
| [**mock4/**](./mock4/README.md) | Employee System | Intervalos + mudança de estado | ★★★★ |

---

## 🎯 Estratégia de Treino

Trate os quatro mocks como **quatro provas separadas**, não como 16 exercícios.

### Ordem recomendada

1. [**Mock 3 --- In-Memory Database**](./mock3/README.md)
2. [**Mock 1 --- File Storage**](./mock1/README.md)
3. [**Mock 4 --- Employee System**](./mock4/README.md)
4. [**Mock 2 --- Banking System**](./mock2/README.md)

### Método

Para cada mock:

1. Reserve **90 minutos**.
2. Comece vendo somente o **Level 1**.
3. Implemente e teste.
4. Só então revele o **Level 2**.
5. Repita para Levels 3 e 4.
6. Todos os testes dos níveis anteriores devem continuar passando.

#### Divisão de tempo sugerida

```text
Level 1     15 min
Level 2     15 min
Level 3     25 min
Level 4     25 min
Debug       10 min
------------------
Total       90 min
```

A progressão deliberada força a refatoração das estruturas de dados conforme novos requisitos aparecem, aproximando o treino do formato de uma avaliação progressiva.
