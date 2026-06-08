import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime

# Arquivos usados pela aplicação.
ARQUIVO_BANCO = "estoque.db"
ARQUIVO_AUDITORIA = "auditoria.txt"


def formatar_preco(valor):
    return f"R$ {valor:.2f}"


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

    auditoria(
        f'ATUALIZAÇÃO - Produto "{nome}" alterado '
        f"(Nova Qtd: {quantidade}, Novo Preço: {preco:.2f})."
    )
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

    auditoria(f'EXCLUSÃO - Produto "{produto[1]}" removido do sistema.')
    return True


# Variáveis globais da interface.
var_id = None
var_nome = None
var_quantidade = None
var_preco = None
tabela_db = None


def carregar_dados():
    # Limpa a tabela e recarrega tudo do banco.
    for row in tabela_db.get_children():
        tabela_db.delete(row)

    for linha in buscar_produtos():
        tabela_db.insert(
            "",
            tk.END,
            values=(linha[0], linha[1], linha[2], formatar_preco(linha[3])),
        )


def limpar_campos():
    var_id.set("")
    var_nome.set("")
    var_quantidade.set("")
    var_preco.set("")


def selecionar_item(event):
    # Quando clica na tabela, joga os dados nos campos.
    item_selecionado = tabela_db.focus()
    if not item_selecionado:
        return

    valores = tabela_db.item(item_selecionado, "values")
    if valores:
        var_id.set(valores[0])
        var_nome.set(valores[1])
        var_quantidade.set(valores[2])
        preco_limpo = str(valores[3]).replace("R$", "").strip().replace(",", ".")
        var_preco.set(preco_limpo)


def validar_entradas():
    # Confere se os campos foram preenchidos e se são números válidos.
    nome = var_nome.get().strip()
    qtd = var_quantidade.get().strip()
    preco = var_preco.get().strip()

    if not nome or not qtd or not preco:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return False

    try:
        int(qtd)
        float(preco.replace(",", "."))
    except ValueError:
        messagebox.showwarning("Aviso", "Quantidade deve ser um inteiro e Preço um número.")
        return False

    return True


def adicionar():
    if validar_entradas():
        nome = var_nome.get().strip()
        qtd = int(var_quantidade.get().strip())
        preco = float(var_preco.get().replace(",", ".").strip())

        add_produto(nome, qtd, preco)
        carregar_dados()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso.")


def atualizar():
    if not var_id.get():
        messagebox.showwarning("Aviso", "Selecione um produto para atualizar.")
        return

    if validar_entradas():
        id_prod = int(var_id.get())
        nome = var_nome.get().strip()
        qtd = int(var_quantidade.get().strip())
        preco = float(var_preco.get().replace(",", ".").strip())

        if atualizar_produto(id_prod, nome, qtd, preco):
            carregar_dados()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")


def excluir():
    if not var_id.get():
        messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
        return

    id_prod = int(var_id.get())
    if messagebox.askyesno("Confirmar", "Deseja realmente excluir este produto?"):
        if excluir_prod(id_prod):
            carregar_dados()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Produto excluído. Log de auditoria gerado.")
        else:
            messagebox.showerror("Erro", "Falha ao excluir o produto.")


def criar_tela():
    global var_id, var_nome, var_quantidade, var_preco, tabela_db

    janela_sistema = tk.Tk()
    janela_sistema.title("Painel de Controle de Estoque")
    janela_sistema.geometry("600x350")

    criar_tabela()

    var_id = tk.StringVar()
    var_nome = tk.StringVar()
    var_quantidade = tk.StringVar()
    var_preco = tk.StringVar()

    frame_entradas = tk.Frame(janela_sistema, padx=10, pady=10)
    frame_entradas.pack(fill=tk.X)

    tk.Label(frame_entradas, text="Produto:").grid(row=0, column=0, sticky=tk.W, pady=2)
    tk.Entry(frame_entradas, textvariable=var_nome, width=22).grid(
        row=0, column=1, pady=2, padx=(5, 16)
    )

    tk.Label(frame_entradas, text="Quantidade:").grid(row=0, column=2, sticky=tk.W, pady=2)
    tk.Entry(frame_entradas, textvariable=var_quantidade, width=12).grid(
        row=0, column=3, pady=2, padx=(5, 16)
    )

    tk.Label(frame_entradas, text="Preço:").grid(row=0, column=4, sticky=tk.W, pady=2)
    tk.Entry(frame_entradas, textvariable=var_preco, width=12).grid(
        row=0, column=5, pady=2, padx=5
    )

    frame_botoes = tk.Frame(janela_sistema, padx=10, pady=5)
    frame_botoes.pack(fill=tk.X)

    tk.Button(frame_botoes, text="Incluir", command=adicionar).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Atualizar", command=atualizar).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Apagar", command=excluir).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Limpar", command=limpar_campos).pack(side=tk.LEFT, padx=5)

    frame_lista = tk.Frame(janela_sistema, padx=10, pady=10)
    frame_lista.pack(fill=tk.BOTH, expand=True)

    tabela_db = ttk.Treeview(
        frame_lista,
        columns=("id", "nome", "qtd", "preco"),
        show="headings",
    )

    tabela_db.heading("id", text="ID")
    tabela_db.heading("nome", text="Descrição do Produto")
    tabela_db.heading("qtd", text="Qtd em Estoque")
    tabela_db.heading("preco", text="Preço Unitário")

    tabela_db.column("id", width=50, anchor="center")
    tabela_db.column("nome", width=250, anchor="w")
    tabela_db.column("qtd", width=100, anchor="center")
    tabela_db.column("preco", width=120, anchor="center")

    tabela_db.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=tabela_db.yview)
    tabela_db.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tabela_db.bind("<ButtonRelease-1>", selecionar_item)

    carregar_dados()
    janela_sistema.mainloop()

if __name__ == "__main__":
    criar_tela()
