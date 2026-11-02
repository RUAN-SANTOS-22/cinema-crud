"""Acesso ao banco: tabela salas."""
import database as db


def listar():
    return db.consultar(
        "SELECT s.id_sala AS id, c.nome AS cinema, s.nome, s.capacidade, s.tipo "
        "FROM salas s JOIN cinemas c ON c.id_cinema = s.id_cinema "
        "ORDER BY c.nome, s.nome")


def buscar(id_sala):
    linhas = db.consultar(
        "SELECT id_cinema, nome, capacidade, tipo FROM salas WHERE id_sala = %s",
        (id_sala,))
    return linhas[0] if linhas else None


def inserir(d):
    db.executar(
        "INSERT INTO salas (id_cinema, nome, capacidade, tipo) VALUES (%s, %s, %s, %s)",
        (d["id_cinema"], d["nome"], d["capacidade"], d["tipo"]))


def atualizar(id_sala, d):
    db.executar(
        "UPDATE salas SET id_cinema = %s, nome = %s, capacidade = %s, tipo = %s "
        "WHERE id_sala = %s",
        (d["id_cinema"], d["nome"], d["capacidade"], d["tipo"], id_sala))


def excluir(id_sala):
    db.executar("DELETE FROM salas WHERE id_sala = %s", (id_sala,))


def opcoes():
    """Rótulo 'Cinema - Sala' para usar no cadastro de sessões."""
    linhas = db.consultar(
        "SELECT s.id_sala AS id, CONCAT(c.nome, ' - ', s.nome) AS rotulo "
        "FROM salas s JOIN cinemas c ON c.id_cinema = s.id_cinema "
        "ORDER BY c.nome, s.nome")
    return [(l["id"], l["rotulo"]) for l in linhas]