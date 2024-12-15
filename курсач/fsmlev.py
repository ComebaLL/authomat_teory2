import requests
from bisect import bisect_left
from spellchecker import SpellChecker

spell = SpellChecker(language="ru")  # Инициализация для русского языка

class LevenshteinAutomaton:
    def __init__(self, word, max_distance):
        """
        word: Слово из словаря, с которым будем сравнивать.
        max_distance: Максимально допустимое расстояние Левенштейна.
        """
        self.word = word
        self.max_distance = max_distance

    def build_automaton(self):
        """
        Создаёт автомат с состояниями для расстояния Левенштейна.
        """
        word_len = len(self.word)
        states = {}

        for i in range(word_len + 1):
            for j in range(self.max_distance + 1):
                states[(i, j)] = set()

        for i in range(word_len + 1):
            for j in range(self.max_distance + 1):
                if j < self.max_distance:
                    # Добавление символа
                    states[(i, j)].add((i, j + 1))

                if i < word_len:
                    # Удаление символа
                    states[(i, j)].add((i + 1, j + 1))

                if i < word_len and j < self.max_distance:
                    # Замена символа
                    states[(i, j)].add((i + 1, j + 1))

                if i < word_len:
                    # Совпадение символа
                    states[(i, j)].add((i + 1, j))

        self.states = states

    def match(self, input_word):
        """
        Проверяет, возможно ли преобразовать input_word в self.word
        за max_distance операций.
        """
        current_states = {(0, 0)}

        for char in input_word:
            next_states = set()
            for state in current_states:
                i, j = state

                if j < self.max_distance:
                    # Добавление символа
                    next_states.add((i, j + 1))

                if i < len(self.word):
                    # Удаление символа
                    next_states.add((i + 1, j + 1))

                    # Совпадение или замена символа
                    if self.word[i] == char:
                        next_states.add((i + 1, j))
                    else:
                        next_states.add((i + 1, j + 1))

            current_states = next_states

        # Проверка, что конечное состояние допустимо
        return any(state[0] == len(self.word) and state[1] <= self.max_distance for state in current_states)


def load_dictionary(filepath):
    """
    Загружает словарь из локального текстового файла.
    """
    try:
        with open(filepath, "r", encoding="windows-1251") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print("Файл словаря не найден. Создайте файл sorted_words.txt.")
        return []


def save_to_dictionary(filepath, dictionary):
    """
    Сохраняет обновлённый словарь в файл.
    """
    with open(filepath, "w", encoding="windows-1251") as file:
        file.write("\n".join(dictionary))


def add_word_to_sorted_dictionary(word, filepath):
    """
    Добавляет слово в отсортированный словарь и сохраняет изменения.
    """
    dictionary = load_dictionary(filepath)
    if word not in dictionary:
        from bisect import insort
        insort(dictionary, word)  # Вставляем слово в отсортированный список
        save_to_dictionary(filepath, dictionary)
        print(f"Слово '{word}' добавлено в словарь.")
    else:
        print(f"Слово '{word}' уже есть в словаре.")


def suggest_word(input_word, dictionary, max_distance):
    """
    Предлагает варианты замены слова из словаря, используя оптимизированный поиск.
    """
    suggestions = []
    start_index = bisect_left(dictionary, input_word[:1])  # Начинаем сужение по первой букве

    for word in dictionary[start_index:]:
        if not word.startswith(input_word[:1]):
            break  # Прекращаем, если слова уже не совпадают по первой букве

        lev_automaton = LevenshteinAutomaton(word, max_distance)
        lev_automaton.build_automaton()
        if lev_automaton.match(input_word):
            suggestions.append(word)

        if len(suggestions) >= 5:  # Ограничиваем количество предложений
            break

    return suggestions


def check_spelling_and_suggest(input_word, dictionary, filepath, max_distance):
    """
    Проверяет слово на грамотность и предлагает варианты замены, если оно некорректно.
    """
    # Проверяем на грамотность
    if input_word in spell:  # Слово грамматически верное
        print(f"Слово '{input_word}' написано корректно.")
        return

    # Если слово некорректное, предлагаются варианты через Левенштейна
    print(f"Слово '{input_word}' возможно написано с ошибкой.")
    suggestions = suggest_word(input_word, dictionary, max_distance)

    if suggestions:
        print("Возможно, вы имели в виду:")
        for i, suggestion in enumerate(suggestions, start=1):
            print(f"{i}. {suggestion}")

        choice = input("Выберите номер слова для замены или введите 0, чтобы оставить своё слово: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(suggestions):
                new_word = suggestions[choice - 1]
                print(f"Вы выбрали: {new_word}")
            elif choice == 0:
                print("Вы оставили своё слово.")
            else:
                print("Неверный выбор. Слово оставлено без изменений.")
        else:
            print("Некорректный ввод. Слово оставлено без изменений.")
    else:
        print("Совпадений не найдено.")
        add_to_dict = input("Добавить слово в словарь? (да/нет): ").strip().lower()
        if add_to_dict == "да":
            add_word_to_sorted_dictionary(input_word, filepath)


def main():
    filepath = "sorted_words.txt"
    dictionary = load_dictionary(filepath)

    if not dictionary:
        print("Словарь пуст или отсутствует. Начните добавлять слова.")

    input_string = input("Введите слово: ").strip()
    max_distance = 1

    for word in input_string.split():
        check_spelling_and_suggest(word, dictionary, filepath, max_distance)


if __name__ == "__main__":
    main()
