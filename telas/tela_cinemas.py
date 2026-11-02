from repositorios import cinemas
from telas.base import Campo, TelaCrud

ESTADOS = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
           "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]


class TelaCinemas(TelaCrud):
    titulo = "Cinemas"
    repo = cinemas
    colunas = [("id", "ID", 50), ("nome", "Nome", 170), ("endereco", "Endereço", 220),
               ("cidade", "Cidade", 120), ("estado", "UF", 40), ("telefone", "Telefone", 110)]
    campos = [
        Campo("nome", "Nome", obrigatorio=True),
        Campo("endereco", "Endereço", obrigatorio=True),
        Campo("cidade", "Cidade", obrigatorio=True),
        Campo("estado", "UF", tipo="escolha", obrigatorio=True, opcoes=ESTADOS),
        Campo("telefone", "Telefone"),
    ]