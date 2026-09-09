---

## Level 2 - Listagem de tags

### Assinaturas adicionadas
```python
class ParcelTrackingSystemImpl:
    def list_tags(self, parcel_id: str) -> list[str]:
        ...

    def list_tags_by_prefix(self, parcel_id: str, prefix: str) -> list[str]:
        ...
```

### Requisitos

`list_tags(parcel_id)`:
- Retorna todas as tags da encomenda.

`list_tags_by_prefix(parcel_id, prefix)`:
- Retorna somente as tags cujo nome começa com `prefix`;
- Um prefixo vazio corresponde a todas as tags.

Cada item deve ter o formato:
```text
"<tag>(<value>)"
```

Ordene o resultado lexicograficamente pelo nome da tag. Se a encomenda não
existir ou nenhuma tag corresponder ao prefixo, retorne `[]`.
