import tkinter as tk
import time

class LightBulb:
    def __init__(self):
        self.state_stack = []  # Стек для хранения состояний
        self.state = "OFF"     # Текущее состояние
        self.start_time = None

    def turn_on(self):
        if self.state == "OFF":
            self.state_stack.append(self.state)  # Сохраняем предыдущее состояние
            self.state = "ON"
            self.start_time = time.time()

    def turn_off(self):
        if self.state == "ON":
            self.state_stack.append(self.state)  # Сохраняем предыдущее состояние
            self.state = "OFF"
            self.start_time = None

    def check_state(self):
        if self.state == "ON":
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= 10:
                self.state_stack.append(self.state)  # Сохраняем предыдущее состояние
                self.state = "BURNED"

    def get_state(self):
        return self.state

    def undo(self):
        if self.state_stack:
            self.state = self.state_stack.pop()  # Возвращаем предыдущее состояние
            if self.state == "ON":
                self.start_time = time.time()  # Сбрасываем таймер при восстановлении состояния "ON"
            else:
                self.start_time = None


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Управление лампочкой")
        
        self.bulb = LightBulb()

        self.bulb_canvas = tk.Canvas(master, width=200, height=200, bg="white")
        self.bulb_canvas.pack(pady=20)

        self.switch_button = tk.Button(master, text="Включить/Выключить", command=self.toggle_bulb)
        self.switch_button.pack(pady=10)

        self.undo_button = tk.Button(master, text="Отменить", command=self.undo_bulb)
        self.undo_button.pack(pady=10)

        self.update_bulb()  # Запускаем обновление состояния лампочки

    def toggle_bulb(self):
        if self.bulb.get_state() == "OFF":
            self.bulb.turn_on()
        elif self.bulb.get_state() == "ON":
            self.bulb.turn_off()
        self.update_bulb()  # Обновляем графическое состояние

    def undo_bulb(self):
        self.bulb.undo()  # Возвращаем предыдущее состояние
        self.update_bulb()  # Обновляем графическое состояние

    def update_bulb(self):
        self.bulb.check_state()  # Проверяем состояние лампочки

        # Обновляем цвет в зависимости от состояния
        if self.bulb.get_state() == "ON":
            self.bulb_canvas.create_oval(50, 50, 150, 150, fill="yellow", outline="black")
            self.master.after(1000, self.update_bulb)  # Проверяем состояние каждую секунду
        elif self.bulb.get_state() == "OFF":
            self.bulb_canvas.delete("all")  # Убираем круг
        elif self.bulb.get_state() == "BURNED":
            self.bulb_canvas.create_oval(50, 50, 150, 150, fill="gray", outline="black")
            self.switch_button.config(state="disabled")  # Выключаем кнопку
            self.undo_button.config(state="disabled")  # Выключаем кнопку отмены

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


