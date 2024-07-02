import json
import tkinter as tk
from tkinter import END, ttk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import CancelarEmLote


class CancelClassesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cancelar Aulas")

        #Cria o estilo
        style = ttk.Style()

        # Verifica os temas disponíveis
        print(style.theme_names())

        # Define o tema (opcional, escolha um tema disponível)
        style.theme_use('default')

        # Configura o estilo do Notebook
        style.configure('TNotebook')
        style.configure('TNotebook.Tab', background='lightgray', padding=[10, 2], font=('Helvetica', 11, 'bold'))

        # Adiciona um efeito visual ao selecionar um tab

        cor = '#B0C4DE'
        style.map('TNotebook.Tab', background=[('selected', cor)])

        self.tab_control = ttk.Notebook(root,style='TNotebook')

        self.create_interval_tab()
        self.create_repeating_tab()
        self.create_help_tab()
        self.create_about_tab()

        self.tab_control.pack(expand=1, fill='both')

    def create_about_tab(self):
        self.about_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.about_tab, text='Sobre')
        about_text = "Sobre o Programa:\n\n"
        about_text +="Este é um software educacional experimental desenvolvido por Wanderson Rigo,\n"
        about_text += "professor do IFC - Campus Videira.\n\n"
        about_text +="O objetivo deste software é cancelar várias aulas, poupando trabalho manual e repetitivo.\n\n"
        about_text +="Versão: 1.0\n"
        about_text +="Desenvolvido com entusiasmo em: 2024\n"
        about_text +="Contato: wanderson.rigo@ifc.edu.br\n\n"
        about_text +="Este software é gratuito e de código aberto. Você pode modificar e distribuir este software,\n"
        about_text += "desde que mantenha a referência ao autor original.\n\n"
        about_text +="Use por sua conta e risco. Este software é fornecido sem garantia de qualquer tipo.\n\n"
        about_text += "O autor não se responsabiliza por qualquer dano causado pelo uso deste software."
        ttk.Label(self.about_tab, text=about_text).pack(padx=10, pady=10)

    def create_help_tab(self):
        self.help_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.help_tab, text='Ajuda')
        help_text = "Este programa foi desenvolvido para auxiliar na tarefa de cancelar várias aulas no SIGAA.\n\n"
        help_text += "Configure no arquivo 'config.json' o seu login, senha (opcional) e o nome da disciplina no SIGAA.\n\n"
        help_text += "As aulas podem ser canceladas por INTERVALO ou REPETIÇÃO.\n\n"
        help_text += "   a) INTERVALO, insira a data inicial e a data final e clique no botão 'Cancelar Aulas'.\n\n"
        help_text += "   b) REPETIÇÃO, insira a data inicial, a quantidade de dias entre as aulas e o número de \n"
        help_text += "repetições e clique no botão 'Cancelar Aulas'."

        ttk.Label(self.help_tab, text=help_text).pack(padx=10, pady=10)

    def create_interval_tab(self):
        self.interval_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.interval_tab, text='Cancelar por Intervalo')

        ttk.Label(self.interval_tab, text="Data Inicial").grid(
            column=0, row=0, padx=10, pady=10)
        self.start_cal = Calendar(self.interval_tab, selectmode='day')
        self.start_cal.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(self.interval_tab, text="Data Final").grid(
            column=0, row=1, padx=10, pady=10)
        self.end_cal = Calendar(self.interval_tab, selectmode='day')
        self.end_cal.grid(column=1, row=1, padx=10, pady=10)

        self.interval_button = ttk.Button(
            self.interval_tab, text="Cancelar Aulas", command=self.cancel_by_interval)
        self.interval_button.grid(column=0, row=2, columnspan=2, pady=10)

    def create_repeating_tab(self):
        self.repeating_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.repeating_tab, text='Cancelar por Repetição')

        ttk.Label(self.repeating_tab, text="Data Inicial").grid(
            column=0, row=0, padx=10, pady=10)
        self.start_repeat_cal = Calendar(self.repeating_tab, selectmode='day')
        self.start_repeat_cal.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(self.repeating_tab, text="Dias entre aulas").grid(
            column=0, row=1, padx=10, pady=10)
        self.days_entry = ttk.Entry(self.repeating_tab)
        self.days_entry.grid(column=1, row=1, padx=10, pady=10)
        self.days_entry.insert(END, '7')

        ttk.Label(self.repeating_tab, text="Número de Repetições").grid(
            column=0, row=2, padx=10, pady=10)
        self.repetitions_entry = ttk.Entry(self.repeating_tab)
        self.repetitions_entry.grid(column=1, row=2, padx=10, pady=10)

        self.repeating_button = ttk.Button(
            self.repeating_tab, text="Cancelar Aulas", command=self.cancel_by_repeating)
        self.repeating_button.grid(column=0, row=3, columnspan=2, pady=10)

    def clean_date_string(self, date_str):
        # Remove caracteres extras ao redor da data
        return date_str.strip()

    def cancel_by_interval(self):
        start_date_str = self.clean_date_string(self.start_cal.get_date())
        end_date_str = self.clean_date_string(self.end_cal.get_date())

        try:
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
            end_date = datetime.strptime(end_date_str, '%d/%m/%Y')

        except ValueError as e:
            print(f"Erro ao converter data: {e}")
            messagebox.showerror("Erro", "Por favor, insira uma data válida.")
            return

        if start_date > end_date:
            messagebox.showerror(
                "Erro", "A data inicial deve ser anterior à data final.")
            return

        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date.strftime('%d/%m/%Y'))
            current_date += timedelta(days=1)

        allDates = ""

        # Itera sobre a lista de datas, com um passo de 5 em 5
        for i in range(0, len(dates), 5):
            # Junta as próximas 5 datas usando ' ' como separador e adiciona uma quebra de linha no final
            allDates += ' '.join(dates[i:i+5]) + "\n"

        ret = messagebox.askokcancel("Confirma as Datas?", allDates)

        if ret:
            # repassando as datas para a classe CancelarEmLote
            self.initSigaa(dates)
        else:
            # parar a execução
            print("Operação cancelada pelo usuário!")
            return

    def initSigaa(self, dates):
        try:
            with open("config.json", "r", encoding="utf-8") as config_file:
                config = json.load(config_file)
                print("Configurações carregadas com sucesso!")
                CancelarEmLote.extrair_notas_sigaa(config, dates)
            print("Aulas canceladas no SIGAA com sucesso!")
        except Exception as e:
            print("Erro na operação:", e)

    def cancel_by_repeating(self):
        start_date_str = self.clean_date_string(
            self.start_repeat_cal.get_date())
        days_interval_str = self.days_entry.get()
        repetitions_str = self.repetitions_entry.get()

        try:
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
            days_interval = int(days_interval_str)
            repetitions = int(repetitions_str)

            if days_interval <= 0 or repetitions < 0:
                raise ValueError("Valores inválidos")

        except ValueError as e:
            print(f"Erro ao converter data ou valores: {e}")
            messagebox.showerror(
                "Erro", "Por favor, insira valores válidos. Quantidade de dias deve ser maior que zero e repetições não pode ser negativo.")
            return

        dates = []
        current_date = start_date
        for _ in range(repetitions + 1):
            dates.append(current_date.strftime('%d/%m/%Y'))
            current_date += timedelta(days=days_interval)

        allDates = ""

        # Itera sobre a lista de datas, com um passo de 5 em 5
        for i in range(0, len(dates), 5):
            # Junta as próximas 5 datas usando ' ' como separador e adiciona uma quebra de linha no final
            allDates += ' '.join(dates[i:i+5]) + "\n"

        ret = messagebox.askokcancel("Confirma as Datas?", allDates)

        if ret:
            # repassando as datas para a classe CancelarEmLote
            self.initSigaa(dates)
        else:
            # parar a execução
            print("Operação cancelada pelo usuário")
            return


# Verifica se o arquivo está sendo executado diretamente
if __name__ == "__main__":
    root = tk.Tk()
    app = CancelClassesApp(root)
    root.mainloop()
