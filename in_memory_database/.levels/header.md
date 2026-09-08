# In-Memory Database

Todos os métodos recebem um `timestamp` inteiro não negativo. As chamadas são
fornecidas em ordem **não decrescente de timestamp**, globalmente por instância:
uma chamada nunca tem timestamp menor que a anterior. Timestamps iguais são
permitidos; nesse caso, as operações são aplicadas na ordem das chamadas.
Não é necessário validar essa garantia nem tratar escritas fora de ordem.
