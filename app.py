import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime
import os

# --- Lógica de Banco de Dados ---
def conectar():
    conn = sqlite3.connect("estoque.db")
    return conn

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def inserir_produto(nome, quantidade, preco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
    cursor.execute("SELECT * FROM produtos ORDER BY id DESC LIMIT 1")
    produto_novo = cursor.fetchone()
    mensagem = "inserção"
    conn.commit()
    conn.close()
    registrar_auditoria(produto_novo, mensagem)

def buscar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    linhas = cursor.fetchall()
    conn.close()
    return linhas

def atualizar_produto(id_produto, nome, quantidade, preco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id=?", (id_produto,))
    produto_antigo = cursor.fetchone()
    mensagem = "atualização"
    cursor.execute("UPDATE produtos SET nome=?, quantidade=?, preco=? WHERE id=?", (nome, quantidade, preco, id_produto))
    conn.commit()
    conn.close()
    registrar_auditoria(produto_antigo, mensagem)
    return True

def excluir_produto_db(id_produto):
    # Primeiro busca o produto para registrar no log
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id=?", (id_produto,))
    produto = cursor.fetchone()
    mensagem = "exclusão"
    
    if produto:
        cursor.execute("DELETE FROM produtos WHERE id=?", (id_produto,))
        conn.commit()
        conn.close()
        # Registrar auditoria
        registrar_auditoria(produto, mensagem="exclusão")
        return True
    
    conn.close()
    return False

# --- Lógica de Auditoria ---
def registrar_auditoria(produto, mensagem):
    id_prod, nome, quantidade, preco = produto
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = f"[{data_hora}] {mensagem.upper()}: ID: {id_prod}, Nome: '{nome}', Quantidade: {quantidade}, Preço: {preco:.2f}\n"
    
    with open("auditoria.txt", "a", encoding="utf-8") as f:
        f.write(log_msg)

# --- Lógica de Interface (GUI) ---
class EstoqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Estoque")
        self.root.geometry("600x450")
        
        criar_tabela()
        
        # Variáveis
        self.var_id = tk.StringVar()
        self.var_nome = tk.StringVar()
        self.var_quantidade = tk.StringVar()
        self.var_preco = tk.StringVar()
        
        # Frame Entradas
        frame_entradas = tk.Frame(self.root, padx=10, pady=10)
        frame_entradas.pack(fill=tk.X) # roda pé
        
        tk.Label(frame_entradas, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=2)
        tk.Entry(frame_entradas, textvariable=self.var_nome, width=30).grid(row=0, column=1, pady=2, padx=5)
        
        tk.Label(frame_entradas, text="Quantidade:").grid(row=1, column=0, sticky=tk.W, pady=2)
        tk.Entry(frame_entradas, textvariable=self.var_quantidade, width=30).grid(row=1, column=1, pady=2, padx=5)
        
        tk.Label(frame_entradas, text="Preço:").grid(row=2, column=0, sticky=tk.W, pady=2)
        tk.Entry(frame_entradas, textvariable=self.var_preco, width=30).grid(row=2, column=1, pady=2, padx=5)
        
        # Frame Botões
        frame_botoes = tk.Frame(self.root, padx=10, pady=5)
        frame_botoes.pack(fill=tk.X)
        
        tk.Button(frame_botoes, text="Adicionar", command=self.adicionar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Atualizar", command=self.atualizar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Excluir", command=self.excluir).pack(side=tk.LEFT, padx=5)
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
        if self.validar_entradas():
            nome = self.var_nome.get().strip()
            qtd = int(self.var_quantidade.get().strip())
            preco = float(self.var_preco.get().replace(',', '.').strip())
            
            inserir_produto(nome, qtd, preco)
            self.carregar_dados()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso.")

    def atualizar(self):
        if not self.var_id.get():
            messagebox.showwarning("Aviso", "Selecione um produto para atualizar.")
            return
            
        if self.validar_entradas():
            id_prod = self.var_id.get()
            nome = self.var_nome.get().strip()
            qtd = int(self.var_quantidade.get().strip())
            preco = float(self.var_preco.get().replace(',', '.').strip())
            
            atualizar_produto(id_prod, nome, qtd, preco)
            self.carregar_dados()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")

    def excluir(self):
        if not self.var_id.get():
            messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
            return
            
        id_prod = self.var_id.get()
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este produto?"):
            if excluir_produto_db(id_prod):
                self.carregar_dados()
                self.limpar_campos()
                messagebox.showinfo("Sucesso", "Produto excluído. Log de auditoria gerado.")
            else:
                messagebox.showerror("Erro", "Falha ao excluir o produto.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EstoqueApp(root)
    root.mainloop()
