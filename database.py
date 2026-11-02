"""Conexão com o MySQL e funções auxiliares de consulta."""
from contextlib import contextmanager
from pathlib import Path

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

def executar_script(nome_arquivo):
    """Executa um arquivo .sql da pasta do projeto (comandos separados por ';')."""
    caminho = Path(__file__).resolve().parent / nome_arquivo
    linhas = [l for l in caminho.read_text(encoding="utf-8").splitlines()
              if not l.strip().startswith("--")]
    comandos = [c.strip() for c in "\n".join(linhas).split(";") if c.strip()]
    conexao = conectar(com_banco=False)
    try:
        cursor = conexao.cursor()
        for comando in comandos:
            cursor.execute(comando)
        conexao.commit()
    finally:
        conexao.close()

def criar_banco():
    """Cria o banco e as tabelas, se ainda não existirem."""
    executar_script("schema.sql")