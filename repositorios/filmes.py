"""Acesso ao banco: tabela filmes + tabela associativa filmes_generos (N:N)."""
import database as db


def listar():
    # GROUP_CONCAT junta os gêneros do filme em um único texto
    return db.consultar(
        "SELECT f.id_filme AS id, f.titulo, "
        "       GROUP_CONCAT(g.nome ORDER BY g.nome SEPARATOR ', ') AS generos, "
        "       f.duracao_min, f.classificacao, "
        "       DATE_FORMAT(f.data_lancamento, '%d/%m/%Y') AS lancamento "
        "FROM filmes f "
        "LEFT JOIN filmes_generos fg ON fg.id_filme = f.id_filme "
        "LEFT JOIN generos g ON g.id_genero = fg.id_genero "
        "GROUP BY f.id_filme ORDER BY f.titulo")


def buscar(id_filme):
    linhas = db.consultar(
        "SELECT titulo, sinopse, duracao_min, classificacao, data_lancamento "
        "FROM filmes WHERE id_filme = %s", (id_filme,))
    if not linhas:
        return None
    filme = linhas[0]
    ids = db.consultar(
        "SELECT id_genero FROM filmes_generos WHERE id_filme = %s", (id_filme,))
    filme["generos"] = [linha["id_genero"] for linha in ids]
    return filme


def _salvar_generos(cursor, id_filme, ids_generos):
    """Regrava as linhas da tabela associativa para o filme."""
    cursor.execute("DELETE FROM filmes_generos WHERE id_filme = %s", (id_filme,))
    cursor.executemany(
        "INSERT INTO filmes_generos (id_filme, id_genero) VALUES (%s, %s)",
        [(id_filme, id_genero) for id_genero in ids_generos])


def inserir(d):
    with db.transacao() as cur:   # filme + gêneros: tudo ou nada
        cur.execute(
            "INSERT INTO filmes (titulo, sinopse, duracao_min, classificacao, "
            "data_lancamento) VALUES (%s, %s, %s, %s, %s)",
            (d["titulo"], d["sinopse"], d["duracao_min"], d["classificacao"],
             d["data_lancamento"]))
        _salvar_generos(cur, cur.lastrowid, d["generos"])


def atualizar(id_filme, d):
    with db.transacao() as cur:
        cur.execute(
            "UPDATE filmes SET titulo = %s, sinopse = %s, duracao_min = %s, "
            "classificacao = %s, data_lancamento = %s WHERE id_filme = %s",
            (d["titulo"], d["sinopse"], d["duracao_min"], d["classificacao"],
             d["data_lancamento"], id_filme))
        _salvar_generos(cur, id_filme, d["generos"])


def excluir(id_filme):
    # as linhas de filmes_generos somem sozinhas (ON DELETE CASCADE)
    db.executar("DELETE FROM filmes WHERE id_filme = %s", (id_filme,))


def opcoes():
    return [(f["id"], f["titulo"]) for f in listar()]