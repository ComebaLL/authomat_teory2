import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

# Инициализация сети Петри
class PetriNet:
    def __init__(self):
        # Инициализация состояний
        self.philosophers = {f"P{i}": "thinking" for i in range(1, 6)}  # "thinking" или "eating"
        self.chopsticks = {f"C{i}": "free" for i in range(1, 6)}  # "free" или "taken"
        self.token_position = "P1"  # Начальная позиция токена (мудрец 1)

    def try_eat(self, philosopher):
        """Попытка начать есть для указанного мудреца."""
        left = f"C{philosopher[-1]}"  # Левая палочка
        right = f"C{(int(philosopher[-1]) % 5) + 1}"  # Правая палочка

        # Проверяем, свободны ли обе палочки
        if self.chopsticks[left] == "free" and self.chopsticks[right] == "free":
            self.philosophers[philosopher] = "eating"
            self.chopsticks[left] = "taken"
            self.chopsticks[right] = "taken"
            return True
        return False

    def stop_eat(self, philosopher):
        """Завершение еды для указанного мудреца."""
        left = f"C{philosopher[-1]}"  # Левая палочка
        right = f"C{(int(philosopher[-1]) % 5) + 1}"  # Правая палочка

        self.philosophers[philosopher] = "thinking"
        self.chopsticks[left] = "free"
        self.chopsticks[right] = "free"

    def get_next_philosopher(self, current):
        """Возвращает следующего мудреца по кругу."""
        current_id = int(current[-1])
        next_id = (current_id % 5) + 1
        return f"P{next_id}"


# Инициализация визуализации
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect("equal")
ax.axis("off")

# Координаты мудрецов и палочек
philosophers = {
    "P1": (1, 0), "P2": (0.5, 0.866), "P3": (-0.5, 0.866),
    "P4": (-1, 0), "P5": (-0.5, -0.866)
}
chopsticks = {
    "C1": (0.75, 0.433), "C2": (0, 0.866), "C3": (-0.75, 0.433),
    "C4": (-0.75, -0.433), "C5": (0, -0.866)
}

# Инициализация визуальных элементов
philosopher_patches = {}
chopstick_patches = {}
token = None

for phil, (x, y) in philosophers.items():
    rect = patches.Rectangle((x - 0.15, y - 0.1), 0.3, 0.2, edgecolor="black", facecolor="white", lw=1.5)
    philosopher_patches[phil] = rect
    ax.add_patch(rect)
    ax.text(x, y + 0.15, phil, ha="center", va="center", fontsize=9)

for chop, (x, y) in chopsticks.items():
    circle = patches.Circle((x, y), 0.1, edgecolor="black", facecolor="lightgray", lw=1.5)
    chopstick_patches[chop] = circle
    ax.add_patch(circle)
    ax.text(x, y + 0.15, chop, ha="center", va="center", fontsize=9)

token_position = "P1"
x, y = philosophers[token_position]
token = patches.Circle((x, y), 0.1, edgecolor="black", facecolor="red", lw=1.5)
ax.add_patch(token)

plt.draw()

# Функция обновления диаграммы
def update_diagram(net):
    """Обновление состояния сети Петри на диаграмме."""
    for phil, state in net.philosophers.items():
        color = "green" if state == "eating" else "white"
        philosopher_patches[phil].set_facecolor(color)

    for chop, state in net.chopsticks.items():
        color = "lightgray" if state == "free" else "gray"
        chopstick_patches[chop].set_facecolor(color)

    # Перемещение токена
    x, y = philosophers[net.token_position]
    token.set_center((x, y))
    fig.canvas.draw_idle()
    plt.pause(0.5)


# Логика работы сети Петри
net = PetriNet()
while True:
    current_philosopher = net.token_position

    # Попытка начать есть
    if net.try_eat(current_philosopher):
        update_diagram(net)
        time.sleep(2)  # Задержка во время еды
        net.stop_eat(current_philosopher)

    # Переход к следующему мудрецу
    net.token_position = net.get_next_philosopher(current_philosopher)
    update_diagram(net)
