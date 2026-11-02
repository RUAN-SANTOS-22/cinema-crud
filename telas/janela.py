"""Janela principal: título + uma aba para cada tela."""
import tkinter as tk
from tkinter import ttk
from telas import tema
from telas.tela_generos import TelaGeneros

# (título da aba, classe da tela). Cada funcionalidade nova entra aqui.
TELAS = [
    ("Gêneros", TelaGeneros),
]


class Janela(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Cinema")
        self.geometry("1180x640")
        self.minsize(980, 560)
        self.configure(bg=tema.ROXO_FUNDO)
        tema.aplicar(self)

        tk.Label(self, text="🎬  Sistema de Cinema", font=("Segoe UI", 18, "bold"),
                 bg=tema.ROXO_ESCURO, fg=tema.AMARELO, anchor="w",
                 padx=16, pady=10).pack(fill="x")

        self.abas = ttk.Notebook(self)
        self.abas.pack(fill="both", expand=True, padx=10, pady=10)
        self.telas = []
        for titulo, classe in TELAS:
            tela = classe(self.abas)
            self.abas.add(tela, text=f"  {titulo}  ")
            self.telas.append(tela)
        self.abas.bind("<<NotebookTabChanged>>", self._ao_trocar_aba)

    def _ao_trocar_aba(self, _evento):
        # recarrega a aba para refletir cadastros feitos em outras abas
        if self.telas:
            self.telas[self.abas.index("current")].recarregar()