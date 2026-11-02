"""Configurações de acesso ao MySQL."""
import os

from dotenv import load_dotenv
load_dotenv(override=True) 

NOME_BANCO = os.getenv("MYSQL_DATABASE", "nomedobancopadrao")

MYSQL = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "usuariopadrao"),
    "password": os.getenv("MYSQL_PASSWORD", "senhapadrao"),
    "charset": "utf8mb4",
}