# Parcel Tracking System

Implemente `ParcelTrackingSystemImpl`, um sistema em memória que associa tags a
encomendas. Cada encomenda é identificada por `parcel_id` e pode ter várias tags,
cada uma com um valor textual.

Nos Levels 1 e 2, as operações são aplicadas sequencialmente na ordem das
chamadas. A partir do Level 3, os métodos adicionados recebem um `timestamp`
inteiro não negativo. Essas chamadas são fornecidas em ordem **não decrescente de
timestamp**, globalmente por instância. Timestamps iguais são permitidos e, nesse
caso, prevalece a ordem das chamadas.
