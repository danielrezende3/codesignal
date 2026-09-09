---

## Level 4 - Checkpoint e restauração

### Assinaturas adicionadas
```python
class ParcelTrackingSystemImpl:
    def checkpoint(self, timestamp: int) -> int:
        ...

    def restore_checkpoint(
        self, timestamp: int, timestamp_to_restore: int
    ) -> None:
        ...
```

### Requisitos

`checkpoint(timestamp)`:
- Descarta primeiro as tags expiradas no `timestamp`;
- Armazena uma cópia independente do estado completo nesse instante;
- Retorna a quantidade de encomendas que possuem ao menos uma tag válida;
- Um novo checkpoint no mesmo timestamp substitui o anterior.

`restore_checkpoint(timestamp, timestamp_to_restore)` restaura o estado completo
do checkpoint mais recente cujo timestamp seja menor ou igual a
`timestamp_to_restore`:
- Tags criadas após o checkpoint são descartadas;
- Tags removidas ou sobrescritas após o checkpoint retornam ao estado salvo;
- Se não houver checkpoint elegível, a operação não altera o estado;
- É garantido que `timestamp_to_restore <= timestamp`.

Ao restaurar, preserve o tempo de vida restante que cada tag possuía quando o
checkpoint foi criado. Se o checkpoint escolhido ocorreu em
`checkpoint_timestamp`, cada expiração finita deve ser deslocada por:
```text
timestamp - checkpoint_timestamp
```

Assim, a nova expiração é a expiração original mais esse deslocamento. Tags
permanentes continuam permanentes. Restaurar não remove os checkpoints já
armazenados.
