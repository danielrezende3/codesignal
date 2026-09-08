# CodeSignal Industry Coding Assessment

Simulados inspirados nas avaliações progressivas do [CodeSignal](https://support.codesignal.com/hc/en-us/articles/19116922232983-What-are-the-Industry-Coding-Assessment-ICA-rules) (tempo sugerido: 90 min por mock).

## 🎯 Simulados (Ordem de Treino)

- [**Integer Container**](./integer_container/README.md)
- [**In-Memory Database**](./in_memory_database/README.md)
- [**File Storage**](./file_storage/README.md)
- [**Employee System**](./employee_system/README.md)
- [**Banking System**](./banking_system/README.md)

## 🚀 Como Treinar (Simulação Passo a Passo)

Todos os mocks começam no **Level 1**, com o `solution.py` limpo e as assinaturas necessárias disponíveis no `README.md`.

A cada novo nível:

* um novo arquivo de testes é adicionado;
* os testes dos níveis anteriores continuam sendo executados **sequencialmente**;
* o `README.md` é atualizado com as novas instruções e requisitos.

Assim, o mesmo código evolui progressivamente conforme novos níveis são desbloqueados.

### comandos disponíveis

```bash
# Mostrar o status dos mocks
uv run sim

# Validar o nível atual e desbloquear o próximo
uv run sim next in_memory_database

# Executar os testes disponíveis sem avançar de nível
uv run sim test file_storage

# Reiniciar o mock para o Level 1
uv run sim reset employee_system
```
