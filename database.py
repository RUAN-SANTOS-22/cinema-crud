"""Conexão com o MySQL e funções auxiliares de consulta."""
from contextlib import contextmanager

import mysql.connector

import config


def conectar(com_banco=True):
    parametros = dict(config.MYSQL)
    if com_banco:
        parametros["database"] = config.NOME_BANCO
    return mysql.connector.connect(**parametros)


@contextmanager
def transacao():
    """Abre uma conexão e entrega um cursor. Faz commit no fim (ou rollback se der erro)."""
    conexao = conectar()
    try:
        cursor = conexao.cursor(dictionary=True, buffered=True)
        yield cursor
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def consultar(sql, params=()):
    """SELECT: devolve uma lista de dicionários."""
    with transacao() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def executar(sql, params=()):
    """INSERT/UPDATE/DELETE: devolve o último id gerado."""
    with transacao() as cur:
        cur.execute(sql, params)
        return cur.lastrowid