# CodeSignal Industry Coding Assessment

Simulados inspirados nas avaliações progressivas do [CodeSignal](https://support.codesignal.com/hc/en-us/articles/19116922232983-What-are-the-Industry-Coding-Assessment-ICA-rules) (tempo sugerido: 90 min por mock).

## 🎯 Simulados (Ordem de Treino)

- [**Integer Container**](./integer_container/README.md) (coleções → mediana)
- [**In-Memory Database**](./in_memory_database/README.md) (`dict` → TTL → histórico)
- [**File Storage**](./file_storage/README.md) (Estado → ranking → ownership)
- [**Employee System**](./employee_system/README.md) (Intervalos + mudança de estado)
- [**Banking System**](./banking_system/README.md) (Estado + operações pendentes + merge)

## 🚀 Como Treinar (Simulação Passo a Passo)

Todos os mocks iniciam no **Level 1** com `solution.py` limpo e as assinaturas completas no `README.md`.
O simulador descobre automaticamente as pastas que contêm uma estrutura `.levels` válida.

```bash
# Mostra status dos mocks
uv run sim

# Validar o nível atual e desbloquear o próximo
uv run sim next in_memory_database

# Executar os testes sem avançar de nível
uv run sim test in_memory_database

# Reiniciar um mock para o Level 1 se quiser recomeçar
uv run sim reset in_memory_database
```
