import math
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Генератор экспоненциального распределения
class ExponGenerator:
    def __init__(self, lmbd, tiks_per_second):
        self.lmbd = lmbd
        self.tiks_per_second = tiks_per_second
        self.time_to_next_request = 0

    def generate(self):
        uniform_random_value = random.random()
        self.time_to_next_request = math.log(1 - uniform_random_value) * (-1 / self.lmbd)
        self.time_to_next_request = round(self.time_to_next_request * self.tiks_per_second)

# Класс для мест сети Петри
class Place:
    def __init__(self, name, tokens=0):
        self.name = name
        self.tokens = tokens

    def add_tokens(self, count=1):
        self.tokens += count

    def remove_tokens(self, count=1):
        if self.tokens >= count:
            self.tokens -= count

# Класс для переходов сети Петри
class Transition:
    def __init__(self, name, input_places, output_places):
        self.name = name
        self.input_places = input_places
        self.output_places = output_places

    def can_fire(self):
        return all(place.tokens > 0 for place in self.input_places)

    def fire(self):
        if self.can_fire():
            for place in self.input_places:
                place.remove_tokens()
            for place in self.output_places:
                place.add_tokens()

# Класс для управления сетью Петри
class PetriNet:
    def __init__(self):
        self.places = {}
        self.transitions = {}

    def add_place(self, name, tokens=0):
        self.places[name] = Place(name, tokens)

    def add_transition(self, name, input_places, output_places):
        self.transitions[name] = Transition(
            name,
            [self.places[ip] for ip in input_places],
            [self.places[op] for op in output_places]
        )

    def run_transition(self, name):
        if name in self.transitions and self.transitions[name].can_fire():
            self.transitions[name].fire()

# Основная функция симуляции СМО
def simulate_smo(num_processors=2, full_time=3000, max_treatment_time=100, my_lambda=5.0, max_queue_length=50):
    tiks_per_second = 50
    generator = ExponGenerator(my_lambda, tiks_per_second)

    # Инициализация сети Петри
    petri_net = PetriNet()
    petri_net.add_place('queue', 0)
    petri_net.add_place('processor1', 0)
    petri_net.add_place('processor2', 0)
    petri_net.add_place('completed', 0)
    petri_net.add_place('rejected', 0)

    # Переходы сети Петри
    petri_net.add_transition('enqueue', ['queue'], ['processor1', 'processor2'])
    petri_net.add_transition('process1', ['processor1'], ['completed'])
    petri_net.add_transition('process2', ['processor2'], ['completed'])

    # История токенов для визуализации
    history = {name: [] for name in petri_net.places}
    treatment_times = {name: 0 for name in ['processor1', 'processor2']}

    # Основной цикл симуляции
    for tik in range(full_time):
        # Генерация новой заявки
        if generator.time_to_next_request == 0:
            generator.generate()
            if petri_net.places['queue'].tokens < max_queue_length:
                petri_net.places['queue'].add_tokens()
            else:
                petri_net.places['rejected'].add_tokens()
        else:
            generator.time_to_next_request -= 1

        # Подача заявки в процессор 1
        if petri_net.places['processor1'].tokens == 0 and petri_net.places['queue'].tokens > 0:
            petri_net.places['processor1'].add_tokens()
            petri_net.places['queue'].remove_tokens()
            treatment_times['processor1'] = max_treatment_time

        # Подача заявки в процессор 2
        if petri_net.places['processor2'].tokens == 0 and petri_net.places['queue'].tokens > 0:
            petri_net.places['processor2'].add_tokens()
            petri_net.places['queue'].remove_tokens()
            treatment_times['processor2'] = max_treatment_time

        # Завершение обработки в процессоре 1
        if petri_net.places['processor1'].tokens > 0:
            treatment_times['processor1'] -= 1
            if treatment_times['processor1'] <= 0:
                petri_net.run_transition('process1')  # Перемещаем заявку из processor1 в completed

        # Завершение обработки в процессоре 2
        if petri_net.places['processor2'].tokens > 0:
            treatment_times['processor2'] -= 1
            if treatment_times['processor2'] <= 0:
                petri_net.run_transition('process2')  # Перемещаем заявку из processor2 в completed

        # Сохраняем текущее состояние токенов для визуализации
        for name in history:
            history[name].append(petri_net.places[name].tokens)

    # Настройка графика для анимации
    fig, ax = plt.subplots(figsize=(8, 4))
    positions = {
        'queue': (-1, 1.5),
        'processor1': (1.5, 2),
        'processor2': (1.5, 1),
        'completed': (4, 1.5),
        'rejected': (-1, 0.5)
    }

    def update_graph(frame):
        ax.clear()
        ax.set_xlim(-2, 6)
        ax.set_ylim(-1, 3)

        for name, pos in positions.items():
            ax.plot(*pos, 'o', markersize=30, label=name, color="lightblue")
            ax.text(pos[0], pos[1] + 0.3, f"{name}: {history[name][frame]}", ha='center')

        # Отображение связей между местами
        connections = [
            ('queue', 'processor1'),
            ('queue', 'processor2'),
            ('processor1', 'completed'),
            ('processor2', 'completed'),
            ('queue', 'rejected')
        ]
        for start, end in connections:
            ax.plot(
                [positions[start][0], positions[end][0]],
                [positions[start][1], positions[end][1]],
                'k-', lw=1
            )

    ani = FuncAnimation(fig, update_graph, frames=len(history['queue']), interval=20, repeat=False)
    plt.show()

simulate_smo(num_processors=2, full_time=3000, max_treatment_time=100, my_lambda=5, max_queue_length=50)
