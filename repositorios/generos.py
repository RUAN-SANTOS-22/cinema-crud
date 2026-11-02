"""Acesso ao banco: tabela generos."""
import database as db


def listar():
    return db.consultar(
        "SELECT id_genero AS id, nome, descricao FROM generos ORDER BY nome")


def buscar(id_genero):
    linhas = db.consultar(
        "SELECT nome, descricao FROM generos WHERE id_genero = %s", (id_genero,))
    return linhas[0] if linhas else None


def inserir(dados):
    db.executar("INSERT INTO generos (nome, descricao) VALUES (%s, %s)",
                (dados["nome"], dados["descricao"]))


def atualizar(id_genero, dados):
    db.executar("UPDATE generos SET nome = %s, descricao = %s WHERE id_genero = %s",
                (dados["nome"], dados["descricao"], id_genero))


def excluir(id_genero):
    db.executar("DELETE FROM generos WHERE id_genero = %s", (id_genero,))


def opcoes():
    """Para os campos de seleção: lista de (id, rótulo)."""
    return [(g["id"], g["nome"]) for g in listar()]