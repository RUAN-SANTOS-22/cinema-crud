from repositorios import filmes, generos
from telas.base import Campo, TelaCrud


class TelaFilmes(TelaCrud):
    titulo = "Filmes"
    repo = filmes
    colunas = [("id", "ID", 50), ("titulo", "Título", 210), ("generos", "Gêneros", 190),
               ("duracao_min", "Min", 50), ("classificacao", "Class.", 60),
               ("lancamento", "Lançamento", 90)]
    campos = [
        Campo("titulo", "Título", obrigatorio=True),
        # "multi": o usuário marca vários gêneros (grava na tabela filmes_generos)
        Campo("generos", "Gêneros", tipo="multi", obrigatorio=True, opcoes=generos.opcoes),
        Campo("duracao_min", "Duração (min)", tipo="inteiro", obrigatorio=True),
        Campo("classificacao", "Classificação", tipo="escolha", obrigatorio=True,
              opcoes=["L", "10", "12", "14", "16", "18"]),
        Campo("data_lancamento", "Lançamento (dd/mm/aaaa)", tipo="data"),
        Campo("sinopse", "Sinopse", tipo="longo"),
    ]