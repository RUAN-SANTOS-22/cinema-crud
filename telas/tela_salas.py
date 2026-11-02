from repositorios import cinemas, salas
from telas.base import Campo, TelaCrud


class TelaSalas(TelaCrud):
    titulo = "Salas"
    repo = salas
    colunas = [("id", "ID", 50), ("cinema", "Cinema", 200), ("nome", "Sala", 160),
               ("capacidade", "Capacidade", 90), ("tipo", "Tipo", 110)]
    campos = [
        Campo("id_cinema", "Cinema", tipo="fk", obrigatorio=True, opcoes=cinemas.opcoes),
        Campo("nome", "Nome da sala", obrigatorio=True),
        Campo("capacidade", "Capacidade", tipo="inteiro", obrigatorio=True),
        Campo("tipo", "Tipo", tipo="escolha", obrigatorio=True,
              opcoes=["Convencional", "VIP", "IMAX", "4DX", "3D"]),
    ]