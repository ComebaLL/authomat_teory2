import tkinter as tk


def build_automaton(pattern):
    # Приводим подстроку к нижнему регистру для регистронезависимой обработки
    pattern = pattern.lower()

    # Определяем длину подстроки
    m = len(pattern)

    # Если подстрока пустая, возвращаем пустой автомат и пустой алфавит
    if m == 0:
        return [{}], set()

    # Алфавит — множество всех уникальных символов, присутствующих в подстроке
    alphabet = set(pattern)

    # Инициализируем автомат как список словарей, каждый из которых представляет состояния автомата
    # Количество состояний равно длине подстроки + 1 (включая начальное состояние)
    automaton = [{} for _ in range(m + 1)]

    # Префикс-функция — вспомогательный массив для оптимизации переходов
    prefix = [0] * m

    # Построение префикс-функции
    # Префикс-функция определяет длину наибольшего собственного префикса, который также является суффиксом
    j = 0  # Текущий индекс в подстроке
    for i in range(1, m):  # Перебираем символы подстроки, начиная со второго
        while j > 0 and pattern[i] != pattern[j]:
            # Если символы не совпадают, сокращаем длину текущего префикса
            j = prefix[j - 1]
        if pattern[i] == pattern[j]:
            # Если символы совпадают, увеличиваем длину префикса
            j += 1
        # Записываем длину префикса для текущего символа
        prefix[i] = j

    # Заполнение таблицы переходов автомата
    # Для каждого состояния определяем, куда переходить по каждому символу из алфавита
    for state in range(m + 1):  # Перебираем состояния автомата (0 до m включительно)
        for char in alphabet:  # Перебираем символы алфавита
            if state < m and char == pattern[state]:
                # Если символ совпадает с ожидаемым, переходим в следующее состояние
                automaton[state][char] = state + 1
            elif state > 0:
                # Если символ не совпадает, возвращаемся в состояние,
                # соответствующее длине наибольшего собственного префикса (по префикс-функции)
                automaton[state][char] = automaton[prefix[state - 1]].get(char, 0)
            else:
                # Если в начальном состоянии символ не совпадает, остаёмся в начальном состоянии
                automaton[state][char] = 0

    # Возвращаем автомат и алфавит
    return automaton, alphabet


def search_with_automaton(text, pattern):
    # Приводим текст и подстроку к нижнему регистру
    text = text.lower()
    pattern = pattern.lower()

    if not pattern:
        return []  # Если подстрока пустая, возвращаем пустой список

    automaton, _ = build_automaton(pattern)
    state = 0
    matches = []

    # Перебираем символы текста, двигаясь по автомату
    for i, char in enumerate(text):
        state = automaton[state].get(char, 0)
        if state == len(pattern):  # Если достигнуто конечное состояние
            matches.append(i - len(pattern) + 1)

    return matches



# Обработчик кнопки: построение автомата и выполнение поиска
def display_automaton_and_search():
    text = entry_text.get("1.0", tk.END).strip()  # Получение текста из текстового поля
    pattern = entry_pattern.get().strip()  # Получение подстроки из поля ввода

    if not text or not pattern:
        return

    automaton, alphabet = build_automaton(pattern)
    alphabet = sorted(alphabet)  # Сортировка алфавита для корректного отображения

    # Очистка области вывода таблицы
    for widget in frame_table.winfo_children():
        widget.destroy()

    # Отображение таблицы переходов
    header = ["State"] + alphabet
    for col, text in enumerate(header):
        tk.Label(frame_table, text=text, relief="ridge", width=10).grid(row=0, column=col)

    for state, transitions in enumerate(automaton):
        tk.Label(frame_table, text=state, relief="ridge", width=10).grid(row=state + 1, column=0)
        for col, char in enumerate(alphabet, start=1):
            value = transitions.get(char, 0)
            tk.Label(frame_table, text=value, relief="ridge", width=10).grid(row=state + 1, column=col)

    # Выполнение поиска
    #matches = search_with_automaton(text, pattern)
    #results_label.config(text=f"Matches found: {len(matches)}. Positions: {matches}")


# Создание основного окна приложения
root = tk.Tk()
root.title("DFA for Substring Search")
root.geometry("500x600")
root.resizable(False, False)

# Поле ввода текста
frame_text = tk.Frame(root)
frame_text.pack(pady=10)

tk.Label(frame_text, text="Enter the text:").pack(anchor="w", padx=5)
entry_text = tk.Text(frame_text, height=5, width=60)
entry_text.pack(padx=5, pady=5)

# Поле ввода подстроки
frame_pattern = tk.Frame(root)
frame_pattern.pack(pady=10)

tk.Label(frame_pattern, text="Enter the pattern:").pack(anchor="w", padx=5)
entry_pattern = tk.Entry(frame_pattern, width=40)
entry_pattern.pack(padx=5, pady=5)

# Кнопка для запуска построения автомата и поиска
button_build = tk.Button(root, text="Matrix", command=display_automaton_and_search)
button_build.pack(pady=10)

# Область для отображения таблицы переходов
frame_table = tk.Frame(root)
frame_table.pack(pady=10)

# Метка для отображения результатов поиска
#results_label = tk.Label(root, text="Result", wraplength=480, justify="left")
#results_label.pack(pady=10)

# Запуск основного цикла приложения
root.mainloop()
