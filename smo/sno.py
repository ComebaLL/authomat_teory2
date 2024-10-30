import math
import random
from scipy import stats
from matplotlib import pyplot as plt

# Состояния процессора
class ProcessorState:
    IDLE = "IDLE"
    BUSY = "BUSY"
    COMPLETED = "COMPLETED"

# Класс для генерации экспоненциально распределенных интервалов времени между заявками
class ExponGenerator:
    def __init__(self, lmbd, tiks_per_second):
        self.lmbd = lmbd
        self.tiks_per_second = tiks_per_second
        self.time_to_next_request = 0

    def generate(self):
        uniform_random_value = random.random()
        self.time_to_next_request = math.log(1 - uniform_random_value) * (-1 / self.lmbd)
        self.time_to_next_request = round(self.time_to_next_request * self.tiks_per_second)

class Request:
    def __init__(self, index):
        self.index = index
        self.treatment_time = 0
        self.waiting_time = 0

class RequestsContainer:
    def __init__(self):
        self.container = []

    def add_request(self, request):
        self.container.append(request)

class Queue(RequestsContainer):
    def __init__(self, length):
        super().__init__()
        self.length = length

    def add_request(self, request):
        if len(self.container) < self.length:
            self.container.append(request)
            return True
        else:
            return False

    def pop_request(self):
        return self.container.pop(0) if self.container else None

# Класс процессора с конечным автоматом
class Processor:
    def __init__(self):
        self.container = []
        self.treatment_time = 0
        self.state = ProcessorState.IDLE  # Начальное состояние
        self.state_changes = []  # Лог состояния

    def add_request(self, request):
        if self.state == ProcessorState.IDLE:
            self.container.append(request)
            self.treatment_time = request.treatment_time
            self.state = ProcessorState.BUSY
            self.log_state_change()
            return True
        return False

    def process(self):
        if self.state == ProcessorState.BUSY:
            self.treatment_time -= 1
            if self.treatment_time == 0:
                self.container.pop(0)
                self.state = ProcessorState.COMPLETED
                self.log_state_change()

        if self.state == ProcessorState.COMPLETED:
            self.state = ProcessorState.IDLE
            self.log_state_change()

    def log_state_change(self):
        self.state_changes.append((len(self.state_changes), self.state))

# Основная программа
def simulate_smo(num_processors=2):
    the_full_time = 100_000
    the_max_treatment_time = 2000
    the_max_queue_length = 10
    tiks_per_second = 100
    my_lambda = 2
    request_id = 0

    generator = ExponGenerator(my_lambda, tiks_per_second)
    queue = Queue(the_max_queue_length)
    rejected_requests = RequestsContainer()
    completed_requests = RequestsContainer()
    processors = [Processor() for _ in range(num_processors)]

    requests_in_queue = []
    requests_completed = []
    requests_rejected = []
    time = []

    for tik in range(the_full_time):
        for processor in processors:
            processor.process()
            if processor.state == ProcessorState.COMPLETED:
                temp_request = processor.pop_request()
                if temp_request:
                    completed_requests.add_request(temp_request)

        for processor in processors:
            if processor.state == ProcessorState.IDLE:
                temp_request = queue.pop_request()
                if temp_request:
                    processor.add_request(temp_request)

        if len(queue.container) > 0:
            for request in queue.container:
                request.waiting_time += 1

        if generator.time_to_next_request == 0:
            request_id += 1
            new_request = Request(request_id)
            new_request.treatment_time = random.randint(1, the_max_treatment_time)
            generator.generate()

            if not queue.add_request(new_request):
                rejected_requests.add_request(new_request)
        else:
            generator.time_to_next_request -= 1

        time.append(tik)
        requests_in_queue.append(len(queue.container))
        requests_completed.append(len(completed_requests.container))
        requests_rejected.append(len(rejected_requests.container))

    print('Отброшенные заявки:', len(rejected_requests.container))
    print('Обработанные заявки:', len(completed_requests.container))
    print('Оставшиеся в очереди:', len(queue.container))
    
    waiting_times = [request.waiting_time for request in completed_requests.container]
    if waiting_times:
        print('Описание времени ожидания:', stats.describe(waiting_times))
    else:
        print('Нет завершенных заявок для анализа времени ожидания.')


    plt.plot(time, requests_in_queue, label='Очередь')
    plt.title("График очереди")
    plt.show()

    plt.plot(time, requests_completed, label='Завершенные заявки')
    plt.title("График выполненных заявок")
    plt.show()

    plt.plot(time, requests_rejected, label='Отброшенные заявки')
    plt.title("График отброшенных заявок")
    plt.show()

    # График состояния процессоров
    for i, processor in enumerate(processors):
        times, states = zip(*processor.state_changes)
        plt.step(times, states, label=f'Процессор {i+1}')
    plt.title("График состояний процессоров")
    plt.xlabel("Время")
    plt.ylabel("Состояние")
    plt.legend()
    plt.show()

simulate_smo(num_processors=2)
