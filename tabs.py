import tkinter as tk
from tkinter import ttk

# Função principal
def main():
    root = tk.Tk()
    root.title("Mudança de cor do Notebook")
    
    # Cria o estilo
    style = ttk.Style()

    # Verifica os temas disponíveis
    print(style.theme_names())

    # Define o tema (opcional, escolha um tema disponível)
    style.theme_use('default')

    # Configura o estilo do Notebook
    style.configure('TNotebook', background='lightblue', borderwidth=0)
    style.configure('TNotebook.Tab', background='lightgray', padding=[10, 2])

    # Adiciona um efeito visual ao selecionar um tab
    style.map('TNotebook.Tab', background=[('selected', 'blue')])

    # Cria o Notebook
    tab_control = ttk.Notebook(root, style='TNotebook')

    # Cria alguns tabs
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)

    tab_control.add(tab1, text='Tab 1')
    tab_control.add(tab2, text='Tab 2')

    # Adiciona conteúdo aos tabs
    ttk.Label(tab1, text='Conteúdo do Tab 1').grid(column=0, row=0, padx=10, pady=10)
    ttk.Label(tab2, text='Conteúdo do Tab 2').grid(column=0, row=0, padx=10, pady=10)

    tab_control.pack(expand=1, fill='both')

    root.mainloop()

# Chama a função principal
if __name__ == "__main__":
    main()
