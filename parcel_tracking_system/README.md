# Parcel Tracking System

Implemente `ParcelTrackingSystemImpl`, um sistema em memória que associa tags a
encomendas. Cada encomenda é identificada por `parcel_id` e pode ter várias tags,
cada uma com um valor textual.

Nos Levels 1 e 2, as operações são aplicadas sequencialmente na ordem das
chamadas. A partir do Level 3, os métodos adicionados recebem um `timestamp`
inteiro não negativo. Essas chamadas são fornecidas em ordem **não decrescente de
timestamp**, globalmente por instância. Timestamps iguais são permitidos e, nesse
caso, prevalece a ordem das chamadas.

## Level 1 - Operações básicas com tags

### Assinaturas
```python
class ParcelTrackingSystemImpl:
    def set_tag(self, parcel_id: str, tag: str, value: str) -> None:
        ...

    def get_tag(self, parcel_id: str, tag: str) -> str | None:
        ...

    def remove_tag(self, parcel_id: str, tag: str) -> bool:
        ...
```

### Requisitos

`set_tag(parcel_id, tag, value)`:
- Define `tag` com `value` na encomenda `parcel_id`;
- Cria a encomenda caso ela ainda não exista;
- Sobrescreve o valor anterior caso a tag já exista.

`get_tag(parcel_id, tag)`:
- Retorna o valor associado à tag;
- Retorna `None` se a encomenda ou a tag não existir.

`remove_tag(parcel_id, tag)`:
- Remove a tag da encomenda;
- Retorna `True` se a tag existia e foi removida;
- Retorna `False` se a encomenda ou a tag não existir.

Encomendas e tags são independentes entre si. Todos os identificadores e valores
são comparados e armazenados exatamente como recebidos.

---
> 💡 Quando passar nos testes deste nível (`uv run sim test nubank`), use `uv run sim next nubank` para desbloquear o Level 2.
