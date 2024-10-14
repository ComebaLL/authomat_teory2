import tkinter as tk
from tkinter import messagebox

class PushdownAutomaton:
    def __init__(self):
        self.stack = []  # стек для хранения состояний и долгов
        self.state = 'Счет Закрыт'  # начальное состояние
        self.stack.append('Счет Закрыт')  # Добавляем состояние в стек

    def transition(self, action):
        if self.state == 'Счет Хороший':
            if action == 'Обычное Снятие Денег':
                return "Обычное снятие денег успешно"
            elif action == 'Вклад':
                return "Вклад на счет успешно выполнен"
            elif action == 'Разрешенное Снятие Денег':
                # Добавляем долг в стек и меняем состояние
                self.stack.append('Долг')
                self.state = 'Превышены Расходы по Счету'
                return "Превышены расходы по счету, добавлен долг"
            elif action == 'Счет Закрыт':
                # Закрываем счет, добавляем это состояние в стек
                self.stack.append('Счет Закрыт')
                self.state = 'Счет Закрыт'
                return "Счет закрыт"
        
        elif self.state == 'Превышены Расходы по Счету':
            if action == 'Разрешенное Снятие Денег':
                # Если еще раз снимаем деньги, увеличиваем долг
                self.stack.append('Долг')
                return "Дополнительное снятие при превышенных расходах"
            elif action == 'Долг Погашен':
                if self.stack and 'Долг' in self.stack:
                    self.stack.remove('Долг')  # Удаляем один долг
                    if not 'Долг' in self.stack:  # Если долгов больше нет
                        self.state = 'Счет Хороший'
                    return "Долг погашен"
                else:
                    return "Нет долгов для погашения"
            elif action == 'Счет Закрыт':
                self.stack.append('Счет Закрыт')
                self.state = 'Счет Закрыт'
                return "Счет закрыт"

        elif self.state == 'Счет Закрыт':
            if action == 'Счет Открыт':
                # Открываем счет, добавляем это состояние в стек
                self.stack.append('Счет Открыт')
                self.state = 'Счет Хороший'
                return "Счет открыт, можно выполнять операции"
            else:
                return "Счет закрыт, операции недоступны"

    def get_state(self):
        return self.state

    def get_stack(self):
        return self.stack

    def has_debt(self):
        return 'Долг' in self.stack  # Если в стеке есть элемент "Долг"

# GUI с использованием tkinter
class AutomatonGUI:
    def __init__(self, root):
        self.automaton = PushdownAutomaton()

        # Основное окно
        self.root = root
        self.root.title("Конечный Автомат Счета")
        
        # Метки для отображения состояния
        self.state_label = tk.Label(root, text=f"Текущее состояние: {self.automaton.get_state()}")
        self.state_label.pack(pady=10)
        
        self.stack_label = tk.Label(root, text=f"Содержимое стека: {self.automaton.get_stack()}")
        self.stack_label.pack(pady=10)
        
        # Кнопки действий
        self.buttons = {}
        self.create_action_buttons()

        # Устанавливаем начальную видимость кнопок
        self.update_buttons_visibility()

    def create_action_buttons(self):
        actions = ['Обычное Снятие Денег', 'Вклад', 'Разрешенное Снятие Денег', 'Долг Погашен', 'Счет Открыт', 'Счет Закрыт']
        for action in actions:
            button = tk.Button(self.root, text=action, command=lambda a=action: self.perform_action(a))
            self.buttons[action] = button
            button.pack(pady=5)

    def perform_action(self, action):
        result = self.automaton.transition(action)
        messagebox.showinfo("Результат действия", result)

        # Обновляем метки
        self.state_label.config(text=f"Текущее состояние: {self.automaton.get_state()}")
        #self.stack_label.config(text=f"Содержимое стека: {self.automaton.get_stack()}")

        # Обновляем видимость кнопок после каждого действия
        self.update_buttons_visibility()

    def update_buttons_visibility(self):
        # Если счет закрыт, показываем только кнопку "Счет Открыт"
        if self.automaton.get_state() == 'Счет Закрыт':
            for action, button in self.buttons.items():
                if action == 'Счет Открыт':
                    button.pack(pady=5)
                else:
                    button.pack_forget()
        else:
            # Если есть долг, блокируем снятие денег
            has_debt = self.automaton.has_debt()
            for action, button in self.buttons.items():
                if action == 'Счет Открыт':
                    button.pack_forget()
                elif has_debt and action in ['Обычное Снятие Денег', 'Разрешенное Снятие Денег']:
                    button.config(state=tk.DISABLED)  # Блокируем снятие денег
                else:
                    button.config(state=tk.NORMAL)  # Включаем остальные кнопки
                button.pack(pady=5)

# Запуск GUI приложения
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('520x520')
    app = AutomatonGUI(root)
    root.mainloop()
