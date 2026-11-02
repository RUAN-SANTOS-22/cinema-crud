"""Tema roxo e amarelo (cores, fontes e estilos do ttk)."""
from tkinter import ttk

ROXO_FUNDO = "#1E0E38"
ROXO_ESCURO = "#2D1450"
ROXO = "#5B2A9E"
ROXO_CLARO = "#7E4FC9"
AMARELO = "#FFD60A"
AMARELO_CLARO = "#FFE566"
TEXTO = "#F7F2FF"
TEXTO_ESCURO = "#1E0E38"

FONTE = ("Segoe UI", 10)
FONTE_NEGRITO = ("Segoe UI", 10, "bold")


def aplicar(janela):
    estilo = ttk.Style(janela)
    estilo.theme_use("clam")
    estilo.configure(".", font=FONTE)

    # fundos e textos
    estilo.configure("Fundo.TFrame", background=ROXO_FUNDO)
    estilo.configure("Card.TFrame", background=ROXO_ESCURO)
    estilo.configure("Fundo.TLabel", background=ROXO_FUNDO, foreground=TEXTO)
    estilo.configure("Card.TLabel", background=ROXO_ESCURO, foreground=TEXTO)
    estilo.configure("CardTitulo.TLabel", background=ROXO_ESCURO, foreground=AMARELO,
                     font=("Segoe UI", 13, "bold"))

    # abas
    estilo.configure("TNotebook", background=ROXO_FUNDO, borderwidth=0)
    estilo.configure("TNotebook.Tab", background=ROXO, foreground=TEXTO,
                     padding=(12, 6), font=FONTE_NEGRITO)
    estilo.map("TNotebook.Tab",
               background=[("selected", AMARELO)],
               foreground=[("selected", TEXTO_ESCURO)])

    # botões
    estilo.configure("Amarelo.TButton", background=AMARELO, foreground=TEXTO_ESCURO,
                     font=FONTE_NEGRITO, padding=(12, 6), borderwidth=0)
    estilo.map("Amarelo.TButton", background=[("active", AMARELO_CLARO)])
    estilo.configure("Roxo.TButton", background=ROXO_CLARO, foreground=TEXTO,
                     font=FONTE_NEGRITO, padding=(12, 6), borderwidth=0)
    estilo.map("Roxo.TButton", background=[("active", ROXO)])

    # campos
    estilo.configure("TEntry", fieldbackground=TEXTO, foreground=TEXTO_ESCURO, padding=4)
    estilo.configure("TCombobox", fieldbackground=TEXTO, foreground=TEXTO_ESCURO,
                     background=ROXO_CLARO, arrowcolor=TEXTO_ESCURO, padding=4)
    estilo.map("TCombobox", fieldbackground=[("readonly", TEXTO)],
               foreground=[("readonly", TEXTO_ESCURO)])

    # tabela
    estilo.configure("Treeview", background=TEXTO, fieldbackground=TEXTO,
                     foreground=TEXTO_ESCURO, rowheight=26, borderwidth=0)
    estilo.map("Treeview", background=[("selected", AMARELO)],
               foreground=[("selected", TEXTO_ESCURO)])
    estilo.configure("Treeview.Heading", background=ROXO, foreground=AMARELO,
                     font=FONTE_NEGRITO, padding=6, relief="flat")
    estilo.map("Treeview.Heading", background=[("active", ROXO_CLARO)])
    estilo.configure("Vertical.TScrollbar", background=ROXO_CLARO,
                     troughcolor=ROXO_ESCURO, arrowcolor=AMARELO)