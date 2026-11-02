from repositorios import generos
from telas.base import Campo, TelaCrud


class TelaGeneros(TelaCrud):
    titulo = "Gêneros"
    repo = generos
    colunas = [("id", "ID", 50), ("nome", "Nome", 180), ("descricao", "Descrição", 380)]
    campos = [
        Campo("nome", "Nome", obrigatorio=True),
        Campo("descricao", "Descrição"),
    ]