from repositorios import filmes, salas, sessoes
from telas.base import Campo, TelaCrud


class TelaSessoes(TelaCrud):
    titulo = "Sessões"
    repo = sessoes
    colunas = [("id", "ID", 50), ("filme", "Filme", 170), ("cinema", "Cinema", 130),
               ("sala", "Sala", 110), ("inicio", "Início", 120), ("idioma", "Idioma", 80),
               ("formato", "Fmt", 40), ("preco", "Preço", 70)]
    campos = [
        Campo("id_filme", "Filme", tipo="fk", obrigatorio=True, opcoes=filmes.opcoes),
        Campo("id_sala", "Sala", tipo="fk", obrigatorio=True, opcoes=salas.opcoes),
        Campo("data_hora_inicio", "Início (dd/mm/aaaa HH:MM)", tipo="datahora",
              obrigatorio=True),
        Campo("idioma", "Idioma", tipo="escolha", obrigatorio=True,
              opcoes=["Dublado", "Legendado"]),
        Campo("formato", "Formato", tipo="escolha", obrigatorio=True, opcoes=["2D", "3D"]),
        Campo("preco", "Preço (R$)", tipo="decimal", obrigatorio=True),
    ]