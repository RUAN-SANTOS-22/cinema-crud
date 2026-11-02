"""Acesso ao banco: tabela cinemas."""
import database as db


def listar():
    return db.consultar(
        "SELECT id_cinema AS id, nome, endereco, cidade, estado, telefone "
        "FROM cinemas ORDER BY nome")


def buscar(id_cinema):
    linhas = db.consultar(
        "SELECT nome, endereco, cidade, estado, telefone "
        "FROM cinemas WHERE id_cinema = %s", (id_cinema,))
    return linhas[0] if linhas else None


def inserir(d):
    db.executar(
        "INSERT INTO cinemas (nome, endereco, cidade, estado, telefone) "
        "VALUES (%s, %s, %s, %s, %s)",
        (d["nome"], d["endereco"], d["cidade"], d["estado"], d["telefone"]))


def atualizar(id_cinema, d):
    db.executar(
        "UPDATE cinemas SET nome = %s, endereco = %s, cidade = %s, estado = %s, "
        "telefone = %s WHERE id_cinema = %s",
        (d["nome"], d["endereco"], d["cidade"], d["estado"], d["telefone"], id_cinema))


def excluir(id_cinema):
    db.executar("DELETE FROM cinemas WHERE id_cinema = %s", (id_cinema,))


def opcoes():
    return [(c["id"], c["nome"]) for c in listar()]