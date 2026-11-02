"""Tela genérica de CRUD: formulário à esquerda e lista à direita.

Cada tela concreta só precisa declarar:
  titulo   -> nome da tela
  repo     -> módulo de repositorio (listar, buscar, inserir, atualizar, excluir)
  colunas  -> colunas da lista: (chave, título, largura)
  campos   -> lista de Campo
"""
import tkinter as tk
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from tkinter import messagebox, ttk

from mysql.connector import Error, errorcode

from telas import tema

FORMATO_DATA = "%d/%m/%Y"
FORMATO_DATAHORA = "%d/%m/%Y %H:%M"


@dataclass
class Campo:
    """Um campo do formulário.

    tipo: texto | longo | inteiro | decimal | data | datahora | escolha | fk | multi
    opcoes: lista de textos (escolha) ou função que devolve [(id, rótulo)] (fk e multi)
    """
    chave: str
    rotulo: str
    tipo: str = "texto"
    obrigatorio: bool = False
    opcoes: object = None

class TelaCrud(ttk.Frame):
    titulo = ""
    repo = None
    colunas = []
    campos = []

    def __init__(self, master):
        super().__init__(master, style="Fundo.TFrame", padding=12)
        self.widgets = {}    # chave -> widget do campo
        self.opcoes = {}     # chave -> [(id, rótulo)] dos campos fk/multi
        self.id_atual = None
        self.linhas = []
        self._montar_formulario()
        self._montar_lista()
        self.recarregar()

    # ------------------------------------------------------------ layout
    def _montar_formulario(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        form = ttk.Frame(self, style="Card.TFrame", padding=14)
        form.grid(row=0, column=0, sticky="ns", padx=(0, 12))

        ttk.Label(form, text=self.titulo, style="CardTitulo.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        for linha, campo in enumerate(self.campos, start=1):
            marca = " *" if campo.obrigatorio else ""
            ttk.Label(form, text=campo.rotulo + marca, style="Card.TLabel").grid(
                row=linha, column=0, sticky="nw", pady=4, padx=(0, 10))
            widget = self._criar_widget(form, campo)
            widget.grid(row=linha, column=1, sticky="ew", pady=4)
            self.widgets[campo.chave] = widget

        botoes = ttk.Frame(form, style="Card.TFrame")
        botoes.grid(row=len(self.campos) + 1, column=0, columnspan=2, pady=(14, 0))
        ttk.Button(botoes, text="Salvar", style="Amarelo.TButton",
                   command=self.salvar).pack(side="left", padx=3)
        ttk.Button(botoes, text="Excluir", style="Roxo.TButton",
                   command=self.excluir).pack(side="left", padx=3)
        ttk.Button(botoes, text="Novo", style="Roxo.TButton",
                   command=self.novo).pack(side="left", padx=3)

    def _criar_widget(self, pai, campo):
        if campo.tipo == "longo":
            return tk.Text(pai, width=32, height=5, wrap="word", font=tema.FONTE,
                           bg=tema.TEXTO, fg=tema.TEXTO_ESCURO, relief="flat")
        if campo.tipo == "multi":
            return tk.Listbox(pai, selectmode="multiple", exportselection=False,
                              height=6, width=34, font=tema.FONTE, relief="flat",
                              bg=tema.TEXTO, fg=tema.TEXTO_ESCURO,
                              selectbackground=tema.AMARELO,
                              selectforeground=tema.TEXTO_ESCURO)
        if campo.tipo == "escolha":
            return ttk.Combobox(pai, values=campo.opcoes, state="readonly", width=30)
        if campo.tipo == "fk":
            return ttk.Combobox(pai, state="readonly", width=30)
        return ttk.Entry(pai, width=32)

    def _montar_lista(self):
        lista = ttk.Frame(self, style="Fundo.TFrame")
        lista.grid(row=0, column=1, sticky="nsew")
        lista.rowconfigure(1, weight=1)
        lista.columnconfigure(0, weight=1)

        busca = ttk.Frame(lista, style="Fundo.TFrame")
        busca.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        ttk.Label(busca, text="Buscar:", style="Fundo.TLabel").pack(side="left")
        self.var_busca = tk.StringVar()
        self.var_busca.trace_add("write", lambda *_: self._filtrar_lista())
        ttk.Entry(busca, textvariable=self.var_busca, width=34).pack(side="left", padx=8)

        chaves = [c[0] for c in self.colunas]
        self.tabela = ttk.Treeview(lista, columns=chaves, show="headings",
                                   selectmode="browse")
        for chave, titulo, largura in self.colunas:
            self.tabela.heading(chave, text=titulo)
            self.tabela.column(chave, width=largura, anchor="w")
        self.tabela.grid(row=1, column=0, sticky="nsew")
        barra = ttk.Scrollbar(lista, orient="vertical", command=self.tabela.yview)
        barra.grid(row=1, column=1, sticky="ns")
        self.tabela.configure(yscrollcommand=barra.set)
        self.tabela.bind("<<TreeviewSelect>>", self._ao_selecionar)

            # ------------------------------------------------------------- dados
    def recarregar(self):
        """Atualiza as opções (fk/multi) e a lista com o que está no banco."""
        try:
            for campo in self.campos:
                if campo.tipo in ("fk", "multi"):
                    self._carregar_opcoes(campo)
            self.linhas = self.repo.listar()
            self._filtrar_lista()
        except Error as erro:
            self._mostrar_erro(erro)

    def _carregar_opcoes(self, campo):
        widget = self.widgets[campo.chave]
        if campo.tipo == "multi":
            marcados = self._ids_marcados(campo) if campo.chave in self.opcoes else []
        self.opcoes[campo.chave] = campo.opcoes()
        rotulos = [rotulo for _, rotulo in self.opcoes[campo.chave]]
        if campo.tipo == "fk":
            if widget.get() not in rotulos:
                widget.set("")
            widget["values"] = rotulos
        else:
            widget.delete(0, "end")
            for rotulo in rotulos:
                widget.insert("end", rotulo)
            self._marcar(campo, marcados)

    def _filtrar_lista(self):
        termo = self.var_busca.get().strip().lower()
        self.tabela.delete(*self.tabela.get_children())
        chaves = [c[0] for c in self.colunas]
        for linha in self.linhas:
            valores = ["" if linha[k] is None else str(linha[k]) for k in chaves]
            if termo and not any(termo in v.lower() for v in valores):
                continue
            self.tabela.insert("", "end", iid=str(linha["id"]), values=valores)

    def _ao_selecionar(self, _evento):
        selecao = self.tabela.selection()
        if not selecao:
            return
        self.id_atual = int(selecao[0])
        try:
            dados = self.repo.buscar(self.id_atual)
        except Error as erro:
            self._mostrar_erro(erro)
            return
        if dados:
            for campo in self.campos:
                self._escrever(campo, dados[campo.chave])

    # ------------------------------------------------- leitura e escrita
    def _ids_marcados(self, campo):
        widget = self.widgets[campo.chave]
        return [self.opcoes[campo.chave][i][0] for i in widget.curselection()]

    def _marcar(self, campo, ids):
        widget = self.widgets[campo.chave]
        widget.selection_clear(0, "end")
        for posicao, (id_, _) in enumerate(self.opcoes[campo.chave]):
            if id_ in ids:
                widget.selection_set(posicao)

    def _escrever(self, campo, valor):
        widget = self.widgets[campo.chave]
        if campo.tipo == "longo":
            widget.delete("1.0", "end")
            widget.insert("1.0", valor or "")
        elif campo.tipo == "multi":
            self._marcar(campo, valor or [])
        elif campo.tipo == "fk":
            rotulo = next((r for i, r in self.opcoes[campo.chave] if i == valor), "")
            widget.set(rotulo)
        elif campo.tipo == "escolha":
            widget.set(valor or "")
        else:
            if valor is None:
                texto = ""
            elif campo.tipo == "data":
                texto = valor.strftime(FORMATO_DATA)
            elif campo.tipo == "datahora":
                texto = valor.strftime(FORMATO_DATAHORA)
            else:
                texto = str(valor)
            widget.delete(0, "end")
            widget.insert(0, texto)

    def _ler(self, campo):
        widget = self.widgets[campo.chave]
        if campo.tipo == "multi":
            ids = self._ids_marcados(campo)
            if campo.obrigatorio and not ids:
                raise ValueError(f"Selecione ao menos um item em '{campo.rotulo}'.")
            return ids
        if campo.tipo == "longo":
            bruto = widget.get("1.0", "end").strip()
        else:
            bruto = widget.get().strip()
        if not bruto:
            if campo.obrigatorio:
                raise ValueError(f"O campo '{campo.rotulo}' é obrigatório.")
            return None
        try:
            if campo.tipo == "inteiro":
                return int(bruto)
            if campo.tipo == "decimal":
                return Decimal(bruto.replace(",", "."))
            if campo.tipo == "data":
                return datetime.strptime(bruto, FORMATO_DATA).date()
            if campo.tipo == "datahora":
                return datetime.strptime(bruto, FORMATO_DATAHORA)
            if campo.tipo == "fk":
                return next(i for i, r in self.opcoes[campo.chave] if r == bruto)
        except (ValueError, InvalidOperation, StopIteration):
            raise ValueError(f"Valor inválido em '{campo.rotulo}'.")
        return bruto

        # ------------------------------------------------------------ ações
    def novo(self):
        self.id_atual = None
        self.tabela.selection_remove(self.tabela.selection())
        for campo in self.campos:
            widget = self.widgets[campo.chave]
            if campo.tipo == "longo":
                widget.delete("1.0", "end")
            elif campo.tipo == "multi":
                widget.selection_clear(0, "end")
            elif campo.tipo in ("fk", "escolha"):
                widget.set("")
            else:
                widget.delete(0, "end")

    def salvar(self):
        try:
            dados = {campo.chave: self._ler(campo) for campo in self.campos}
            if self.id_atual is None:
                self.repo.inserir(dados)
            else:
                self.repo.atualizar(self.id_atual, dados)
        except ValueError as erro:
            messagebox.showwarning("Atenção", str(erro))
            return
        except Error as erro:
            self._mostrar_erro(erro)
            return
        self.novo()
        self.recarregar()

    def excluir(self):
        if self.id_atual is None:
            messagebox.showinfo("Atenção", "Selecione um item da lista para excluir.")
            return
        if not messagebox.askyesno("Confirmar", "Deseja realmente excluir este item?"):
            return
        try:
            self.repo.excluir(self.id_atual)
        except Error as erro:
            self._mostrar_erro(erro)
            return
        self.novo()
        self.recarregar()

    def _mostrar_erro(self, erro):
        if erro.errno == errorcode.ER_ROW_IS_REFERENCED_2:
            mensagem = "Não é possível excluir: este item está sendo usado em outro cadastro."
        elif erro.errno == errorcode.ER_DUP_ENTRY:
            mensagem = "Já existe um registro com esses dados."
        else:
            mensagem = f"Erro no banco de dados:\n{erro}"
        messagebox.showerror("Erro", mensagem)