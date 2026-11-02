"""Acesso ao banco: tabela sessoes (liga filme + sala + horário)."""
import database as db


def listar():
    return db.consultar(
        "SELECT s.id_sessao AS id, f.titulo AS filme, c.nome AS cinema, sa.nome AS sala, "
        "       DATE_FORMAT(s.data_hora_inicio, '%d/%m/%Y %H:%i') AS inicio, "
        "       s.idioma, s.formato, "
        "       CONCAT('R$ ', REPLACE(s.preco, '.', ',')) AS preco "
        "FROM sessoes s "
        "JOIN filmes f ON f.id_filme = s.id_filme "
        "JOIN salas sa ON sa.id_sala = s.id_sala "
        "JOIN cinemas c ON c.id_cinema = sa.id_cinema "
        "ORDER BY s.data_hora_inicio DESC")


def buscar(id_sessao):
    linhas = db.consultar(
        "SELECT id_filme, id_sala, data_hora_inicio, idioma, formato, preco "
        "FROM sessoes WHERE id_sessao = %s", (id_sessao,))
    return linhas[0] if linhas else None


def inserir(d):
    db.executar(
        "INSERT INTO sessoes (id_filme, id_sala, data_hora_inicio, idioma, formato, preco) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (d["id_filme"], d["id_sala"], d["data_hora_inicio"], d["idioma"],
         d["formato"], d["preco"]))


def atualizar(id_sessao, d):
    db.executar(
        "UPDATE sessoes SET id_filme = %s, id_sala = %s, data_hora_inicio = %s, "
        "idioma = %s, formato = %s, preco = %s WHERE id_sessao = %s",
        (d["id_filme"], d["id_sala"], d["data_hora_inicio"], d["idioma"],
         d["formato"], d["preco"], id_sessao))


def excluir(id_sessao):
    db.executar("DELETE FROM sessoes WHERE id_sessao = %s", (id_sessao,))