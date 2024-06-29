import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta

class CancelClassesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cancelar Aulas")

        self.tab_control = ttk.Notebook(root)
        
        self.create_interval_tab()
        self.create_repeating_tab()
        
        self.tab_control.pack(expand=1, fill='both')
    
    def create_interval_tab(self):
        self.interval_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.interval_tab, text='Cancelar por Intervalo')
        
        ttk.Label(self.interval_tab, text="Data Inicial").grid(column=0, row=0, padx=10, pady=10)
        self.start_cal = Calendar(self.interval_tab, selectmode='day', year=2024, month=6, day=1)
        self.start_cal.grid(column=1, row=0, padx=10, pady=10)
        
        ttk.Label(self.interval_tab, text="Data Final").grid(column=0, row=1, padx=10, pady=10)
        self.end_cal = Calendar(self.interval_tab, selectmode='day', year=2024, month=6, day=1)
        self.end_cal.grid(column=1, row=1, padx=10, pady=10)
        
        self.interval_button = ttk.Button(self.interval_tab, text="Cancelar Aulas", command=self.cancel_by_interval)
        self.interval_button.grid(column=0, row=2, columnspan=2, pady=10)
    
    def create_repeating_tab(self):
        self.repeating_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.repeating_tab, text='Cancelar por Repetição')
        
        ttk.Label(self.repeating_tab, text="Data Inicial").grid(column=0, row=0, padx=10, pady=10)
        self.start_repeat_cal = Calendar(self.repeating_tab, selectmode='day', year=2024, month=6, day=1)
        self.start_repeat_cal.grid(column=1, row=0, padx=10, pady=10)
        
        ttk.Label(self.repeating_tab, text="Quantidade de Dias").grid(column=0, row=1, padx=10, pady=10)
        self.days_entry = ttk.Entry(self.repeating_tab)
        self.days_entry.grid(column=1, row=1, padx=10, pady=10)
        
        ttk.Label(self.repeating_tab, text="Número de Repetições").grid(column=0, row=2, padx=10, pady=10)
        self.repetitions_entry = ttk.Entry(self.repeating_tab)
        self.repetitions_entry.grid(column=1, row=2, padx=10, pady=10)
        
        self.repeating_button = ttk.Button(self.repeating_tab, text="Cancelar Aulas", command=self.cancel_by_repeating)
        self.repeating_button.grid(column=0, row=3, columnspan=2, pady=10)
    
    def cancel_by_interval(self):
        start_date = self.start_cal.get_date()
        end_date = self.end_cal.get_date()
        
        start_date = datetime.strptime(start_date, '%m/%d/%y')
        end_date = datetime.strptime(end_date, '%m/%d/%y')
        
        if start_date > end_date:
            messagebox.showerror("Erro", "A data inicial deve ser anterior à data final.")
            return
        
        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date.strftime('%d/%m/%Y'))
            current_date += timedelta(days=1)
        
        messagebox.showinfo("Datas Canceladas", "\n".join(dates))
    
    def cancel_by_repeating(self):
        start_date = self.start_repeat_cal.get_date()
        days_interval = self.days_entry.get()
        repetitions = self.repetitions_entry.get()
        
        try:
            start_date = datetime.strptime(start_date, '%m/%d/%y')
            days_interval = int(days_interval)
            repetitions = int(repetitions)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")
            return
        
        dates = []
        current_date = start_date
        for _ in range(repetitions + 1):
            dates.append(current_date.strftime('%d/%m/%Y'))
            current_date += timedelta(days=days_interval)
        
        messagebox.showinfo("Datas Canceladas", "\n".join(dates))

if __name__ == "__main__":
    root = tk.Tk()
    app = CancelClassesApp(root)
    root.mainloop()
