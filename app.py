import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime

# Arquivos usados pela aplicação.
ARQUIVO_BANCO = "estoque.db"
ARQUIVO_AUDITORIA = "auditoria.txt"


def criar_tabela():
    # Cria a tabela apenas na primeira execução.
    with sqlite3.connect(ARQUIVO_BANCO) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL
            )
            """
        )


def auditoria(acao, produto):
    # Se não houver produto, não grava nada no arquivo de auditoria.
    if not produto:
        return

    id_prod, nome, quantidade, preco = produto
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    texto = (
        f"[{data_hora}] {acao.upper()}: ID: {id_prod}, Nome: '{nome}', "
        f"Quantidade: {quantidade}, Preço: {preco:.2f}\n"
    )

    with open(ARQUIVO_AUDITORIA, "a", encoding="utf-8") as arquivo:
        arquivo.write(texto)


def buscar_produtos():
    # Busca todos os produtos para mostrar na tabela da tela.
    with sqlite3.connect(ARQUIVO_BANCO) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos ORDER BY id")
        return cursor.fetchall()


def add_produto(nome, quantidade, preco):
    # Insere no banco e depois registra a ação no log.
    with sqlite3.connect(ARQUIVO_BANCO) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
            (nome, quantidade, preco),
        )
        id_novo = cursor.lastrowid
        cursor.execute(
            "SELECT id, nome, quantidade, preco FROM produtos WHERE id = ?",
            (id_novo,),
        )
        produto_novo = cursor.fetchone()

    auditoria("inserção", produto_novo)


def atualizar_produto(id_produto, nome, quantidade, preco):
    # Primeiro verifica se o produto existe.
    with sqlite3.connect(ARQUIVO_BANCO) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nome, quantidade, preco FROM produtos WHERE id = ?",
            (id_produto,),
        )
        produto_antigo = cursor.fetchone()

        if not produto_antigo:
            return False

        cursor.execute(
            "UPDATE produtos SET nome = ?, quantidade = ?, preco = ? WHERE id = ?",
            (nome, quantidade, preco, id_produto),
        )

    auditoria("atualização", produto_antigo)
    return True


def excluir_prod(id_produto):
    # Busca antes de excluir para poder registrar no log.
    with sqlite3.connect(ARQUIVO_BANCO) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nome, quantidade, preco FROM produtos WHERE id = ?",
            (id_produto,),
        )
        produto = cursor.fetchone()

        if not produto:
            return False

        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))

    auditoria("exclusão", produto)
    return True


class Estoque:
    def __init__(self, root):
        self.root = root
        self.root.title("Meu Primeiro Sistema de Estoque")
        self.root.geometry("760x450")
        
        criar_tabela()
        
        # Variáveis que ficam ligadas aos campos de entrada.
        self.var_id = tk.StringVar()
        self.var_nome = tk.StringVar()
        self.var_quantidade = tk.StringVar()
        self.var_preco = tk.StringVar()
        
        # Frame Entradas
        frame_entradas = tk.Frame(self.root, padx=10, pady=10)
        frame_entradas.pack(fill=tk.X)
        
        tk.Label(frame_entradas, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=2)
        tk.Entry(frame_entradas, textvariable=self.var_nome, width=22).grid(row=0, column=1, pady=2, padx=(5, 16))

        tk.Label(frame_entradas, text="Quantidade:").grid(row=0, column=2, sticky=tk.W, pady=2)
        tk.Entry(frame_entradas, textvariable=self.var_quantidade, width=12).grid(row=0, column=3, pady=2, padx=(5, 16))

        tk.Label(frame_entradas, text="Preço:").grid(row=0, column=4, sticky=tk.W, pady=2)
        tk.Entry(frame_entradas, textvariable=self.var_preco, width=12).grid(row=0, column=5, pady=2, padx=5)
        
        # Frame Botões
        frame_botoes = tk.Frame(self.root, padx=10, pady=5)
        frame_botoes.pack(fill=tk.X)
        
        tk.Button(frame_botoes, text="Incluir", command=self.adicionar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Atualizar", command=self.atualizar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Apagar", command=self.excluir).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        
        # Frame Lista
        frame_lista = tk.Frame(self.root, padx=10, pady=10)
        frame_lista.pack(fill=tk.BOTH, expand=True)
        
        colunas = ("ID", "Nome", "Quantidade", "Preço")
        self.tree = ttk.Treeview(frame_lista, columns=colunas, show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Preço", text="Preço (R$)")
        
        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=250)
        self.tree.column("Quantidade", width=100)
        self.tree.column("Preço", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.selecionar_item)
        
        self.carregar_dados()
        
    def carregar_dados(self):
        # Limpa a tabela e recarrega tudo do banco.
        for row in self.tree.get_children():
            self.tree.delete(row)
        for linha in buscar_produtos():
            self.tree.insert("", tk.END, values=linha)
            
    def limpar_campos(self):
        self.var_id.set("")
        self.var_nome.set("")
        self.var_quantidade.set("")
        self.var_preco.set("")
        
    def selecionar_item(self, event):
        # Quando clica na tabela, joga os dados nos campos.
        item_selecionado = self.tree.focus()
        if not item_selecionado:
            return
        valores = self.tree.item(item_selecionado, "values")
        if valores:
            self.var_id.set(valores[0])
            self.var_nome.set(valores[1])
            self.var_quantidade.set(valores[2])
            self.var_preco.set(valores[3])
            
    def validar_entradas(self):
        # Confere se os campos foram preenchidos e se são números válidos.
        nome = self.var_nome.get().strip()
        qtd = self.var_quantidade.get().strip()
        preco = self.var_preco.get().strip()
        
        if not nome or not qtd or not preco:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return False
            
        try:
            int(qtd)
            float(preco.replace(',', '.'))
        except ValueError:
            messagebox.showwarning("Aviso", "Quantidade deve ser um inteiro e Preço um número.")
            return False
            
        return True

    def adicionar(self):
        # Botão Adicionar.
        if self.validar_entradas():
            nome = self.var_nome.get().strip()
            qtd = int(self.var_quantidade.get().strip())
            preco = float(self.var_preco.get().replace(',', '.').strip())
            
            add_produto(nome, qtd, preco)
            self.carregar_dados()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso.")

    def atualizar(self):
        # Botão Atualizar.
        if not self.var_id.get():
            messagebox.showwarning("Aviso", "Selecione um produto para atualizar.")
            return
            
        if self.validar_entradas():
            id_prod = int(self.var_id.get())
            nome = self.var_nome.get().strip()
            qtd = int(self.var_quantidade.get().strip())
            preco = float(self.var_preco.get().replace(',', '.').strip())
            
            if atualizar_produto(id_prod, nome, qtd, preco):
                self.carregar_dados()
                self.limpar_campos()
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
            else:
                messagebox.showerror("Erro", "Produto não encontrado.")

    def excluir(self):
        # Botão Excluir.
        if not self.var_id.get():
            messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
            return
            
        id_prod = int(self.var_id.get())
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este produto?"):
            if excluir_prod(id_prod):
                self.carregar_dados()
                self.limpar_campos()
                messagebox.showinfo("Sucesso", "Produto excluído. Log de auditoria gerado.")
            else:
                messagebox.showerror("Erro", "Falha ao excluir o produto.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Estoque(root)
    root.mainloop()
