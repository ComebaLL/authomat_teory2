import math
import random
from scipy import stats
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.animation import FuncAnimation
from enum import Enum, auto

class ProcessorState(Enum):
    IDLE = auto()
    BUSY = auto()
    COMPLETE = auto()

class Request:
    def __init__(self, treatment_time):
        self.treatment_time = treatment_time
        self.waiting_time = 0

class ProcessorFSM:
    def __init__(self):
        self.state = ProcessorState.IDLE
        self.current_request = None
        self.treatment_time_left = 0

    def add_request(self, request):
        if self.state == ProcessorState.IDLE:
            self.current_request = request
            self.treatment_time_left = request.treatment_time
            self.state = ProcessorState.BUSY
            return True
        return False

    def process(self):
        if self.state == ProcessorState.BUSY:
            if self.treatment_time_left > 0:
                self.treatment_time_left -= 1
            if self.treatment_time_left == 0:
                self.state = ProcessorState.COMPLETE

    def complete_request(self):
        if self.state == ProcessorState.COMPLETE:
            completed_request = self.current_request
            self.current_request = None
            self.state = ProcessorState.IDLE
            return completed_request
        return None

class FSMSystem:
    def __init__(self, num_processors, max_queue_length, max_treatment_time, full_time, my_lambda, tiks_per_second):
        self.queue = []
        self.rejected_requests = []
        self.completed_requests = []
        self.processors = [ProcessorFSM() for _ in range(num_processors)]
        self.num_processors = num_processors
        self.max_queue_length = max_queue_length
        self.max_treatment_time = max_treatment_time
        self.full_time = full_time
        self.lambda_ = my_lambda
        self.tiks_per_second = tiks_per_second
        self.time_points = []
        self.processor_states = [[] for _ in range(num_processors)]
        self.requests_in_queue = []
        self.requests_completed = []
        self.requests_rejected = []
        self.time_to_next_request = 0

    def generate_request(self):
        request_time = random.randint(1, self.max_treatment_time)
        return Request(request_time)

    def step(self, tik):
        for i, processor in enumerate(self.processors):
            processor.process()
            if processor.state == ProcessorState.COMPLETE:
                completed_request = processor.complete_request()
                if completed_request:
                    self.completed_requests.append(completed_request)
            self.processor_states[i].append(processor.state)

        for processor in self.processors:
            if processor.state == ProcessorState.IDLE and self.queue:
                processor.add_request(self.queue.pop(0))

        for request in self.queue:
            request.waiting_time += 1

        if self.time_to_next_request == 0:
            new_request = self.generate_request()
            if len(self.queue) < self.max_queue_length:
                self.queue.append(new_request)
            else:
                self.rejected_requests.append(new_request)
            self.time_to_next_request = int(random.expovariate(self.lambda_) * self.tiks_per_second)
        else:
            self.time_to_next_request -= 1

        self.time_points.append(tik)
        self.requests_in_queue.append(len(self.queue))
        self.requests_completed.append(len(self.completed_requests))
        self.requests_rejected.append(len(self.rejected_requests))

    def animate_system(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        queue_rect = patches.Rectangle((0.1, 0.8), 0.2, 0.1, edgecolor='black', facecolor='lightblue')
        ax.add_patch(queue_rect)
        ax.text(0.2, 0.85, 'Queue', ha='center', fontsize=12)
        
        processor_circles = []
        for i in range(self.num_processors):
            circle = patches.Circle((0.5 + i * 0.2, 0.5), 0.08, edgecolor='black', facecolor='lightgray')
            ax.add_patch(circle)
            processor_circles.append(circle)
            ax.text(0.5 + i * 0.2, 0.6, f'Processor {i+1}', ha='center', fontsize=10)

        text_elements = []

        def update(frame):
            
            while ax.texts:
                ax.texts[-1].remove()

            self.step(frame)
            text_elements.append(ax.text(0.2, 0.85, f'Queue: {len(self.queue)}', ha='center', fontsize=12))
            for i, processor in enumerate(self.processors):
                color = 'green' if processor.state == ProcessorState.IDLE else 'red' if processor.state == ProcessorState.BUSY else 'yellow'
                processor_circles[i].set_facecolor(color)
                text_elements.append(ax.text(0.5 + i * 0.2, 0.4, processor.state.name, ha='center', fontsize=10, color=color))
            text_elements.append(ax.text(0.2, 0.1, f'Completed: {len(self.completed_requests)}', ha='center', fontsize=12))
            text_elements.append(ax.text(0.7, 0.1, f'Rejected: {len(self.rejected_requests)}', ha='center', fontsize=12))

        ani = FuncAnimation(fig, update, frames=range(self.full_time), repeat=False)
        plt.show()

# Запуск системы с анимацией
fsm_system = FSMSystem(
    num_processors=2,
    max_queue_length=10,
    max_treatment_time=20,
    full_time=1000,
    my_lambda=2,
    tiks_per_second=10
)
fsm_system.animate_system()
