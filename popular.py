"""Popula o banco com dados de exemplo.

python popular.py            -> carrega os dados (só se o banco estiver vazio)
python popular.py --limpar   -> apaga TUDO e carrega os dados de novo
"""
import sys

import database as db

# ordem de limpeza: primeiro as tabelas que dependem das outras
TABELAS = ["sessoes", "filmes_generos", "salas", "filmes", "cinemas", "generos"]


def contar(tabela):
    return db.consultar(f"SELECT COUNT(*) AS n FROM {tabela}")[0]["n"]


def limpar():
    """Esvazia todas as tabelas e reinicia os ids."""
    with db.transacao() as cur:
        cur.execute("SET FOREIGN_KEY_CHECKS = 0")   # permite truncar tabelas com FK
        for tabela in TABELAS:
            cur.execute(f"TRUNCATE TABLE {tabela}")
        cur.execute("SET FOREIGN_KEY_CHECKS = 1")


def main():
    db.criar_banco()
    if "--limpar" in sys.argv:
        limpar()
    elif any(contar(t) > 0 for t in TABELAS):
        print("O banco já tem dados. Use 'python popular.py --limpar' para recomeçar.")
        return
    db.executar_script("dados_exemplo.sql")
    print("Dados carregados:")
    for tabela in reversed(TABELAS):
        print(f"  {tabela:<16} {contar(tabela)} registros")


if __name__ == "__main__":
    main()