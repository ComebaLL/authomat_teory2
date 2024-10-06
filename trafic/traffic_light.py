import tkinter as tk  # Импортируем модуль для создания графического интерфейса
import time  # Импортируем модуль для работы с временем

# Класс TrafficLight описывает поведение светофора
class TrafficLight:
    def __init__(self):
        self.state_stack = []  # Стек для хранения предыдущих состояний светофора
        self.state = "RED"  # Начальное состояние светофора — "Красный"
        self.start_time = time.time()  # Сохраняем время, когда началось текущее состояние
        self.cycle_type = 1  # Тип текущего цикла (1 - стандартный, 2 - со стрелкой)

    # Переход в состояние "Желтый"
    def switch_to_yellow(self):
        self.state_stack.append(self.state)  # Добавляем текущее состояние в стек
        self.state = "YELLOW"  # Устанавливаем новое состояние — "Желтый"
        self.start_time = time.time()  # Обновляем время начала состояния

    # Переход в состояние "Зеленый" (в зависимости от типа цикла)
    def switch_to_green(self):
        self.state_stack.append(self.state)  # Добавляем текущее состояние в стек
        self.state = "GREEN"  # Устанавливаем новое состояние — "Зеленый"
        self.start_time = time.time()  # Обновляем время начала состояния

    # Переход в состояние "Красный"
    def switch_to_red(self):
        self.state_stack.append(self.state)  # Добавляем текущее состояние в стек
        self.state = "RED"  # Устанавливаем новое состояние — "Красный"
        self.start_time = time.time()  # Обновляем время начала состояния
        # Переключаем цикл после завершения полного цикла
        if self.cycle_type == 1:
            self.cycle_type = 2
        else:
            self.cycle_type = 1

    # Метод для управления состояниями и переключениями
    def check_state(self):
        elapsed_time = time.time() - self.start_time  # Сколько времени прошло с начала состояния

        # Переходы между состояниями
        if self.state == "RED" and elapsed_time >= 10:
            self.switch_to_yellow()  # Переключаемся на желтый через 10 секунд

        elif self.state == "YELLOW" and elapsed_time >= 6:
            self.switch_to_green()  # Переключаемся на зеленый через 6 секунд

        elif self.state == "GREEN" and elapsed_time >= 10:
            # Если зеленый горит уже 10 секунд, переключаемся на красный
            self.switch_to_red()

    # Метод для получения текущего состояния светофора и типа цикла
    def get_state_and_cycle(self):
        return self.state, self.cycle_type


# Основное приложение, которое создает графический интерфейс для отображения светофора
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Светофор")  # Устанавливаем заголовок окна

        # Создаем объект светофора
        self.traffic_light = TrafficLight()

        # Создаем Canvas (холст) для отображения графики (светофора)
        self.light_canvas = tk.Canvas(master, width=200, height=500, bg="white")
        self.light_canvas.pack(pady=20)  # Располагаем холст с отступами

        # Создаем зеленую стрелку вверх для второго цикла
        self.arrow_image = tk.PhotoImage(file="arrow_up.ppm")

        # Запускаем процесс обновления состояния светофора каждые 500 миллисекунд
        self.update_light()

    # Метод для обновления графического интерфейса в зависимости от состояния светофора
    def update_light(self):
        self.traffic_light.check_state()  # Проверяем и обновляем состояние светофора

        # Получаем текущее состояние светофора и тип цикла
        current_state, cycle_type = self.traffic_light.get_state_and_cycle()

        # Очищаем холст перед перерисовкой
        self.light_canvas.delete("all")

        # В зависимости от текущего состояния рисуем "лампочки" светофора
        if current_state == "RED":
            self.draw_light("red", "black", "black", cycle_type)  # Красный включен, желтый и зеленый выключены
        elif current_state == "YELLOW":
            self.draw_light("black", "yellow", "black", cycle_type)  # Желтый включен, красный и зеленый выключены
        elif current_state == "GREEN":
            if cycle_type == 1:
                # Первый цикл: рисуем зеленый круг
                self.draw_light("black", "black", "green", cycle_type)  # Зеленый включен, красный и желтый выключены
            elif cycle_type == 2:
                # Второй цикл: рисуем зеленую стрелку
                self.draw_light("black", "black", "arrow", cycle_type)

        # Через 500 миллисекунд перезапускаем метод для плавного обновления
        self.master.after(500, self.update_light)

    # Метод для рисования кругов (светофорных лампочек) на холсте
    def draw_light(self, red, yellow, green, cycle_type):
        # Рисуем три круга, представляющие красный, желтый и зеленый цвета
        # Координаты для каждого цвета фиксированы, но цвет круга зависит от переданных параметров
        self.light_canvas.create_oval(50, 50, 150, 150, fill=red, outline="black")
        self.light_canvas.create_oval(50, 200, 150, 300, fill=yellow, outline="black")
        
        if green == "green":
            self.light_canvas.create_oval(50, 350, 150, 450, fill="green", outline="black")  # Зеленый круг
        elif green == "arrow":
            # Для второго цикла рисуем стрелку вместо круга
            self.light_canvas.create_image(100, 400, image=self.arrow_image)  # Зеленая стрелка вверх

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()  # Создаем основное окно приложения
    app = App(root)  # Создаем объект приложения, передавая ему окно
    root.mainloop()  # Запускаем основной цикл обработки событий приложения (интерфейс)
