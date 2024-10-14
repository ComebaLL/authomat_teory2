import tkinter as tk
from tkinter import messagebox

class AccountStateMachine:
    def __init__(self, master):
        self.master = master
        self.master.title("Состояния счета")
        
        # Начальное состояние и баланс
        self.state = "Счет Открыт"
        self.balance = 0  # Начальный баланс
        self.overdraft_limit = -1000  # Лимит на овердрафт
        
        # Надписи для отображения состояния и баланса
        self.state_label = tk.Label(master, text=f"Текущее состояние: {self.state}", font=("Arial", 16))
        self.state_label.pack(pady=20)

        self.balance_label = tk.Label(master, text=f"Баланс: {self.balance} руб.", font=("Arial", 16))
        self.balance_label.pack(pady=10)
        
        # Поле для ввода суммы
        self.amount_label = tk.Label(master, text="Введите сумму:")
        self.amount_label.pack(pady=5)
        
        self.amount_entry = tk.Entry(master)
        self.amount_entry.pack(pady=5)

        # Кнопки для действий (создаются, но не показываются сразу)
        self.deposit_button = tk.Button(master, text="Вклад", command=self.deposit)
        self.withdraw_button = tk.Button(master, text="Обычное снятие денег", command=self.withdraw)
        self.overdraft_button = tk.Button(master, text="Разрешенное снятие денег", command=self.overdraft)
        self.pay_debt_button = tk.Button(master, text="Долг погашен", command=self.pay_debt)
        self.close_account_button = tk.Button(master, text="Закрыть счет", command=self.close_account)
        
        # Кнопка выхода
        self.exit_button = tk.Button(master, text="Выйти", command=self.master.quit)
        self.exit_button.pack(pady=20)

        # Первоначальная инициализация кнопок
        self.update_buttons()

    def update_state_and_balance(self):
        self.state_label.config(text=f"Текущее состояние: {self.state}")
        self.balance_label.config(text=f"Баланс: {self.balance} руб.")
        self.update_buttons()  # Обновляем кнопки при изменении состояния

    def get_amount(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную положительную сумму.")
            return None

    def deposit(self):
        amount = self.get_amount()
        if amount is None:
            return
        
        if self.state in ["Счет Открыт", "Счет Хороший"]:
            self.balance += amount
            messagebox.showinfo("Вклад", f"Вклад в размере {amount} руб. успешно сделан.")
        else:
            messagebox.showwarning("Ошибка", "Невозможно сделать вклад в текущем состоянии.")
        
        self.update_state_and_balance()

    def withdraw(self):
        amount = self.get_amount()
        if amount is None:
            return
        
        if self.state == "Счет Хороший" and self.balance >= amount:
            self.balance -= amount
            messagebox.showinfo("Снятие", f"Обычное снятие в размере {amount} руб. выполнено.")
        else:
            if self.balance < amount:
                messagebox.showwarning("Ошибка", "Недостаточно средств на счете для обычного снятия.")
            else:
                messagebox.showwarning("Ошибка", "Обычное снятие недоступно в текущем состоянии.")
        
        self.update_state_and_balance()

    def overdraft(self):
        amount = self.get_amount()
        if amount is None:
            return
        
        if self.state == "Счет Хороший":
            if self.balance - amount >= self.overdraft_limit:
                self.balance -= amount
                if self.balance < 0:
                    self.state = "Превышены расходы по счету"
                messagebox.showinfo("Снятие", f"Разрешенное снятие в размере {amount} руб. выполнено.")
            else:
                messagebox.showwarning("Ошибка", f"Овердрафт превышает лимит в {abs(self.overdraft_limit)} руб.")
        else:
                messagebox.showwarning("Ошибка", "Разрешенное снятие недоступно в текущем состоянии.")
        
        self.update_state_and_balance()

    def pay_debt(self):
        amount = self.get_amount()
        if amount is None:
            return
        
        if self.state == "Превышены расходы по счету":
            self.balance += amount
            if self.balance >= 0:
                self.state = "Счет Хороший"
            messagebox.showinfo("Долг", f"Погашено {amount} руб.")
        else:
            messagebox.showwarning("Ошибка", "Нет долга для погашения.")
        
        self.update_state_and_balance()

    def close_account(self):
        if self.state in ["Счет Открыт", "Счет Хороший"] and self.balance == 0:
            self.state = "Счет Закрыт"
            messagebox.showinfo("Закрытие счета", "Счет успешно закрыт.")
        elif self.balance != 0:
            messagebox.showwarning("Ошибка", "Закрытие счета возможно только при нулевом балансе.")
        else:
            messagebox.showwarning("Ошибка", "Невозможно закрыть счет в текущем состоянии.")
        
        self.update_state_and_balance()

    def update_buttons(self):
        # Удаляем все кнопки
        self.deposit_button.pack_forget()
        self.withdraw_button.pack_forget()
        self.overdraft_button.pack_forget()
        self.pay_debt_button.pack_forget()
        self.close_account_button.pack_forget()

        # Появление кнопок в зависимости от состояния
        if self.state in ["Счет Открыт", "Счет Хороший"]:
            self.deposit_button.pack(pady=5)
            self.withdraw_button.pack(pady=5)
            self.overdraft_button.pack(pady=5)
            self.close_account_button.pack(pady=5)
        elif self.state == "Превышены расходы по счету":
            self.pay_debt_button.pack(pady=5)

# Создание окна
root = tk.Tk()
app = AccountStateMachine(root)
root.mainloop()