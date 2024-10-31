import math
import random
from scipy import stats
from matplotlib import pyplot as plt
from enum import Enum, auto

# Определение состояний для процессора. Эти состояния помогут нам отслеживать,
# находится ли процессор в состоянии ожидания заявки, обработки или завершения.
class ProcessorState(Enum):
    IDLE = auto()        # Свободен, ожидает заявку
    BUSY = auto()        # Занят обработкой заявки
    COMPLETE = auto()    # Завершил обработку и освобождается

# Класс заявки, представляющий конкретный запрос на обработку
class Request:
    def __init__(self, treatment_time):
        self.treatment_time = treatment_time  # Время обработки заявки
        self.waiting_time = 0                 # Время ожидания заявки в очереди

# Класс для моделирования конечного автомата процессора (ProcessorFSM)
class ProcessorFSM:
    def __init__(self):
        self.state = ProcessorState.IDLE  # Начальное состояние — свободен
        self.current_request = None       # Текущая заявка, которую обрабатывает процессор
        self.treatment_time_left = 0      # Оставшееся время обработки текущей заявки

    # Метод для добавления новой заявки на обработку
    def add_request(self, request):
        # Если процессор свободен, он начинает обрабатывать новую заявку
        if self.state == ProcessorState.IDLE:
            self.current_request = request               # Сохраняем заявку
            self.treatment_time_left = request.treatment_time  # Устанавливаем время обработки
            self.state = ProcessorState.BUSY            # Переводим процессор в состояние BUSY
            return True
        return False

    # Метод для уменьшения оставшегося времени обработки и обновления состояния процессора
    def process(self):
        if self.state == ProcessorState.BUSY:
            if self.treatment_time_left > 0:
                self.treatment_time_left -= 1            # Уменьшаем оставшееся время на 1 тик
            if self.treatment_time_left == 0:
                self.state = ProcessorState.COMPLETE     # Если время закончилось, заявка завершена

    # Метод для завершения обработки и освобождения процессора
    def complete_request(self):
        if self.state == ProcessorState.COMPLETE:
            completed_request = self.current_request
            self.current_request = None                 # Очищаем текущую заявку
            self.state = ProcessorState.IDLE            # Процессор становится свободным
            return completed_request                    # Возвращаем выполненную заявку
        return None

# Класс для всей системы массового обслуживания с конечными автоматами процессоров
class FSMSystem:
    def __init__(self, num_processors, max_queue_length, max_treatment_time, full_time, my_lambda, tiks_per_second):
        self.queue = []                     # Очередь заявок, ожидающих обработки
        self.rejected_requests = []         # Список отклоненных заявок, когда очередь полна
        self.completed_requests = []        # Список выполненных заявок
        self.processors = [ProcessorFSM() for _ in range(num_processors)]  # Список процессоров
        self.num_processors = num_processors
        self.max_queue_length = max_queue_length  # Максимальная длина очереди
        self.max_treatment_time = max_treatment_time  # Максимальное время обработки одной заявки
        self.full_time = full_time              # Общее время симуляции
        self.lambda_ = my_lambda                # Интенсивность поступления заявок (лямбда)
        self.tiks_per_second = tiks_per_second  # Количество тиков в секунду
        self.time_points = []                   # Временные точки для построения графиков
        self.processor_states = [[] for _ in range(num_processors)]  # Состояния каждого процессора
        self.requests_in_queue = []             # Состояния очереди по времени
        self.requests_completed = []            # Количество выполненных заявок по времени
        self.requests_rejected = []             # Количество отклоненных заявок по времени
        self.time_to_next_request = 0           # Время до следующей заявки

    # Генерация новой заявки с случайным временем обработки
    def generate_request(self):
        request_time = random.randint(1, self.max_treatment_time)
        return Request(request_time)  # Возвращаем экземпляр Request

    # Основной цикл симуляции
    def run(self):
        # Проходим по каждому тиканью времени
        for tik in range(self.full_time):
            # Обрабатываем текущее состояние каждого процессора
            for i, processor in enumerate(self.processors):
                processor.process()  # Уменьшаем оставшееся время обработки, если процессор занят
                if processor.state == ProcessorState.COMPLETE:
                    # Если обработка завершена, добавляем заявку в список завершенных
                    completed_request = processor.complete_request()
                    if completed_request:
                        self.completed_requests.append(completed_request)
                # Записываем состояние процессора для построения графиков
                self.processor_states[i].append(1 if processor.state == ProcessorState.BUSY else 0)

            # Подаем заявки из очереди в свободные процессоры
            for processor in self.processors:
                if processor.state == ProcessorState.IDLE and self.queue:
                    processor.add_request(self.queue.pop(0))  # Передаем заявку из очереди в процессор

            # Увеличиваем время ожидания для всех заявок, находящихся в очереди
            for request in self.queue:
                request.waiting_time += 1

            # Генерация новой заявки
            if self.time_to_next_request == 0:
                new_request = self.generate_request()
                # Добавляем заявку в очередь, если она не полная, иначе отклоняем
                if len(self.queue) < self.max_queue_length:
                    self.queue.append(new_request)
                else:
                    self.rejected_requests.append(new_request)
                # Рассчитываем время до следующей заявки
                self.time_to_next_request = int(random.expovariate(self.lambda_) * self.tiks_per_second)
            else:
                self.time_to_next_request -= 1  # Уменьшаем таймер до следующей заявки

            # Сохраняем данные для построения графиков
            self.time_points.append(tik)
            self.requests_in_queue.append(len(self.queue))
            self.requests_completed.append(len(self.completed_requests))
            self.requests_rejected.append(len(self.rejected_requests))

        self.show_results()  # Выводим результаты симуляции

    # Метод для вывода результатов симуляции и построения графиков
    def show_results(self):
        print(f'Отброшенные заявки: {len(self.rejected_requests)}')
        print(f'Обработанные заявки: {len(self.completed_requests)}')
        # Рассчитываем и выводим статистику по времени ожидания
        waiting_times = [r.waiting_time for r in self.completed_requests]
        print('Описание времени ожидания:', stats.describe(waiting_times))

        # Построение графика очереди по времени
        plt.plot(self.time_points, self.requests_in_queue, label='Очередь')
        plt.title("График очереди")
        plt.show()

        # Построение графика завершенных заявок по времени
        plt.plot(self.time_points, self.requests_completed, label='Завершенные заявки')
        plt.title("График выполненных заявок")
        plt.show()

        # Построение графика отклоненных заявок по времени
        plt.plot(self.time_points, self.requests_rejected, label='Отброшенные заявки')
        plt.title("График отброшенных заявок")
        plt.show()

        # Построение графика состояний процессоров (1 - занят, 0 - свободен)
        for i, states in enumerate(self.processor_states):
            plt.plot(self.time_points, states, label=f'Процессор {i+1}')
        plt.title("Состояния процессоров (1 - занят, 0 - свободен)")
        plt.xlabel("Время (тики)")
        plt.ylabel("Состояние")
        plt.legend()
        plt.show()

# Создаем экземпляр системы и запускаем симуляцию
fsm_system = FSMSystem(
    num_processors=2, 
    max_queue_length=10, 
    max_treatment_time=2000, 
    full_time=100_000, 
    my_lambda=2, 
    tiks_per_second=100
)
fsm_system.run()
