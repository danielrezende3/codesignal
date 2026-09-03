# CodeSignal - Mocks Progressivos em Python

Simulados inspirados nas avaliações progressivas do CodeSignal (tempo sugerido: 90 min por mock).

---

## 🎯 Ordem Recomendada

1. [**Mock 3 — In-Memory Database**](./mock3/README.md) (`dict` → TTL → histórico)
2. [**Mock 1 — File Storage**](./mock1/README.md) (Estado → ranking → ownership)
3. [**Mock 4 — Employee System**](./mock4/README.md) (Intervalos + mudança de estado)
4. [**Mock 2 — Banking System**](./mock2/README.md) (Estado + operações pendentes + merge)

---

## 🚀 Como Treinar (Simulação Passo a Passo)

Todos os mocks iniciam no **Level 1** com `solution.py` limpo e as assinaturas completas no `README.md`.

```bash
# 1. Ativar o mock desejado (ex: Mock 3)
uv run sim start 3

# 2. Executar os testes do mock ativo
uv run sim test

# 3. Quando os testes passarem, desbloquear o próximo nível
uv run sim next

# Ver o progresso de todos os mocks
uv run sim status

# Reiniciar um mock para o Level 1 se quiser recomeçar
uv run sim reset 3
```

---

## 🧹 Linting e Formatação

```bash
uv run ruff check .          # Verificar lint
uv run ruff check --fix .    # Corrigir lint automaticamente
uv run ruff format .         # Formatar código
```
