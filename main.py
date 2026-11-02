"""Ponto de entrada do sistema: python main.py"""
import tkinter as tk
from tkinter import messagebox

from mysql.connector import Error

import database
from telas.janela import Janela


def main():
    try:
        database.criar_banco()
    except Error as erro:
        raiz = tk.Tk()
        raiz.withdraw()
        messagebox.showerror(
            "Erro de conexão",
            "Não foi possível conectar ao MySQL.\n"
            "Confira o arquivo .env.\n\n" + str(erro))
        return
    Janela().mainloop()


if __name__ == "__main__":
    main()