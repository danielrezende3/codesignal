---

## Level 3 - Operações com timestamp e tempo de retenção

### Assinaturas adicionadas
```python
class ParcelTrackingSystemImpl:
    def set_tag_at(
        self, parcel_id: str, tag: str, value: str, timestamp: int
    ) -> None:
        ...

    def get_tag_at(
        self, parcel_id: str, tag: str, timestamp: int
    ) -> str | None:
        ...

    def remove_tag_at(
        self, parcel_id: str, tag: str, timestamp: int
    ) -> bool:
        ...

    def set_tag_with_hold(
        self,
        parcel_id: str,
        tag: str,
        value: str,
        timestamp: int,
        ttl: int,
    ) -> None:
        ...

    def list_tags_at(self, parcel_id: str, timestamp: int) -> list[str]:
        ...

    def list_tags_by_prefix_at(
        self, parcel_id: str, prefix: str, timestamp: int
    ) -> list[str]:
        ...
```

### Requisitos

`set_tag_at(...)` define ou sobrescreve uma tag no instante informado. A nova tag
é permanente, inclusive quando substitui uma tag que possuía expiração.

`get_tag_at(...)` retorna o valor válido no instante informado, ou `None` se a
encomenda ou tag não existir ou se a tag já tiver expirado.

`remove_tag_at(...)` remove uma tag somente se ela estiver válida no instante
informado. Retorna `True` quando remove e `False` quando a encomenda ou a tag não
existe, já foi removida ou já expirou.

`set_tag_with_hold(...)` define ou sobrescreve uma tag com tempo de vida `ttl`:
- Para `ttl > 0`, a tag é válida no intervalo semiaberto
  `[timestamp, timestamp + ttl)`;
- No instante exato `timestamp + ttl`, ela já está expirada;
- Para `ttl == 0`, a tag não expira.

`list_tags_at(...)` e `list_tags_by_prefix_at(...)` seguem as mesmas regras de
formatação, filtro e ordenação do Level 2, omitindo tags expiradas no timestamp da
consulta.

Qualquer nova definição substitui completamente o valor e a expiração anteriores.
Quando uma versão expira, uma versão antiga da mesma tag não reaparece.
