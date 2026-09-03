# CodeSignal - Mocks Progressivos em Python

Simulados inspirados nas avaliações progressivas do CodeSignal (tempo sugerido: 90 min por mock).



## 🎯 Ordem Recomendada

Resolva os mocks de forma progressiva (Level 1 → 4), mantendo a compatibilidade com os níveis anteriores:

1. [**Mock 3 — In-Memory Database**](./mock3/README.md) (`dict` → TTL → histórico)
2. [**Mock 1 — File Storage**](./mock1/README.md) (Estado → ranking → ownership)
3. [**Mock 4 — Employee System**](./mock4/README.md) (Intervalos + mudança de estado)
4. [**Mock 2 — Banking System**](./mock2/README.md) (Estado + operações pendentes + merge)



## 🧪 Testes

A execução é progressiva: o pytest só avança para o próximo nível quando o atual passar.

```bash
# Rodar um mock específico (ex: Mock 3)
uv run pytest mock3/

# Rodar apenas uma questão
uv run pytest mock3/test_question_1.py

# Rodar todos os mocks
uv run pytest
```

## 🧹 Linting e Formatação

```bash
uv run ruff check .          # Verificar lint
uv run ruff check --fix .    # Corrigir lint automaticamente
uv run ruff format .         # Formatar código
```
