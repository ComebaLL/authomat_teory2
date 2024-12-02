import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation

# Размер сетки
size = 240
grid = np.full((size, size), -1)  # Инициализация сетки значением -1 (пустое пространство)

# Центр сетки
center = size // 2

# Цвета
color_map = mcolors.ListedColormap(['black', 'lightgreen', 'darkgreen'])

# Размер ромба
inner_size = 48

# Рисуем темно-зеленый ромб с черными треугольниками внутри
for i in range(center - inner_size, center + inner_size):
    for j in range(center - inner_size, center + inner_size):
        if abs(i - center) + abs(j - center) < inner_size:
            dx = j - center
            dy = center - i
            # Определяем треугольники внутри ромба
            if dx >= 0 and dy >= 0:
                grid[i, j] = 0 if (dx > dy) else 2
            elif dx >= 0 and dy < 0:
                grid[i, j] = 0 if (abs(dy) > dx) else 2
            elif dx < 0 and dy >= 0:
                grid[i, j] = 2 if (abs(dx) > dy) else 0
            elif dx < 0 and dy < 0:
                grid[i, j] = 2 if (abs(dy) > abs(dx)) else 0

# Правила для клеточного автомата (A, B, C)
rules = {
    0: [(0, 2, 0, 2), (2, 0, 0, 1)],  # A -> C or B
    1: [(2, 2, 1, 0), (15, 2, 1, 0)],  # B -> A
    2: [(2, 0, -1, 1), (0, 15, -1, 1), (15, 2, -1, 1)]  # C -> A
}

# Список направлений для соседей (вверх, вниз, влево, вправо и диагонали)
neighbors_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# Функция для подсчета соседей для конкретной клетки
def count_neighbors(i, j, grid):
    counts = [0, 0, 0]  # [0: для 0, 1: для 1, 2: для 2]
    
    # Проверяем соседей
    for di, dj in neighbors_offsets:
        ni, nj = i + di, j + dj
        if 0 <= ni < grid.shape[0] and 0 <= nj < grid.shape[1]:  # Проверяем, что сосед в пределах сетки
            state = grid[ni, nj]
            if state != -1:  # Если клетка активна (не пустая)
                counts[state] += 1
    return counts

# Обновление сетки по правилам
def update_grid(grid):
    new_grid = grid.copy()  # Копируем сетку, чтобы изменения не затронули текущие расчеты

    # Применяем правила только внутри ромба
    for i in range(center - inner_size, center + inner_size):
        for j in range(center - inner_size, center + inner_size):
            if abs(i - center) + abs(j - center) < inner_size:  # Проверка, что клетка внутри ромба
                current_state = grid[i, j]
                if current_state != -1:  # Применяем правило только если клетка активна
                    counts = count_neighbors(i, j, grid)  # Подсчитываем соседей
                    for rule in rules.get(current_state, []):  # Проверяем правила
                        a, b, c, next_state = rule
                        if counts[0] == a and counts[1] == b and counts[2] == c:
                            new_grid[i, j] = next_state  # Применяем новое состояние
    return new_grid

# Настройка анимации
fig, ax = plt.subplots(figsize=(12, 12))
im = ax.imshow(grid, cmap=color_map, interpolation="nearest")
ax.axis('off')

# Функция для обновления кадров
def animate(frame):
    global grid
    grid = update_grid(grid)  # Обновляем сетку по правилам
    im.set_data(grid)  # Обновляем отображение
    return [im]

# Создание анимации
ani = FuncAnimation(fig, animate, frames=100, interval=100, blit=True)

# Покажем анимацию
plt.show()
