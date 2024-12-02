import tkinter as tk

# Размер сетки и клетки
GRID_SIZE = 50
CELL_SIZE = 8

# Начальное состояние автомата
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
turmite_position = [GRID_SIZE // 2, GRID_SIZE // 2]
turmite_state = 'A'
turmite_direction = 0

# Правила переходов
RULES = {
    ('A', 0): (2, 0, 'C'),
    ('A', 2): (0, 0, 'B'),
    ('B', 2): (2, 1, 'A'),
    ('B', 15): (2, 1, 'A'),
    ('C', 2): (0, -1, 'A'),
    ('C', 0): (15, -1, 'A'),
    ('C', 15): (2, -1, 'A'),
}

# Преобразование кода цвета в цвет
COLOR_MAP = {
    0: "black", 1: "blue", 2: "cyan", 3: "green", 4: "yellow",
    5: "magenta", 6: "red", 7: "purple", 8: "brown", 9: "gray",
    10: "lightblue", 11: "lightgreen", 12: "lightyellow", 13: "pink",
    14: "orange", 15: "white"
}

# Функции для управления автоматом
def apply_rules(state, cell):
    return RULES.get((state, cell), (cell, 0, state))

def move_turmite():
    global turmite_position, turmite_direction, turmite_state

    x, y = turmite_position
    current_cell = grid[y][x]

    new_cell_color, turn_direction, new_state = apply_rules(turmite_state, current_cell)
    grid[y][x] = new_cell_color
    turmite_state = new_state
    turmite_direction = (turmite_direction + turn_direction + 4) % 4

    dx, dy = 0, 0
    if turmite_direction == 0: dy = -1
    elif turmite_direction == 1: dx = 1
    elif turmite_direction == 2: dy = 1
    elif turmite_direction == 3: dx = -1

    turmite_position[0] = (x + dx + GRID_SIZE) % GRID_SIZE
    turmite_position[1] = (y + dy + GRID_SIZE) % GRID_SIZE

def reset():
    global grid, turmite_position, turmite_state, turmite_direction
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    turmite_position = [GRID_SIZE // 2, GRID_SIZE // 2]
    turmite_state = 'A'
    turmite_direction = 0

def update():
    move_turmite()
    canvas.delete("all")
    draw_grid()
    window.after(1, update)

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = COLOR_MAP[grid[y][x]]
            canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill=color, outline="darkgray"
            )
    x, y = turmite_position
    canvas.create_rectangle(
        x * CELL_SIZE, y * CELL_SIZE,
        (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
        fill="magenta"
    )

# Инициализация окна
window = tk.Tk()
window.title("Клеточный автомат")
canvas = tk.Canvas(window, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, bg="white")
canvas.pack()

# Кнопки управления
control_frame = tk.Frame(window)
control_frame.pack()

start_button = tk.Button(control_frame, text="Старт", command=lambda: update())
start_button.pack(side=tk.LEFT)

stop_button = tk.Button(control_frame, text="Стоп", command=lambda: window.after_cancel(update))
stop_button.pack(side=tk.LEFT)

reset_button = tk.Button(control_frame, text="Сброс", command=lambda: [reset(), draw_grid()])
reset_button.pack(side=tk.LEFT)

# Запуск программы
reset()
draw_grid()
window.mainloop()
