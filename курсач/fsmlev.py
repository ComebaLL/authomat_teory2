import requests

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
        print("Файл словаря не найден. Создайте файл russian_words.txt.")
        return []


def save_to_dictionary(filepath, dictionary):
    """
    Сохраняет обновлённый словарь в файл.
    """
    with open(filepath, "w", encoding="windows-1251") as file:
        file.write("\n".join(dictionary))


def suggest_word(input_word, dictionary, max_distance):
    """
    Предлагает варианты замены слова из словаря, основываясь на расстоянии Левенштейна.
    """
    suggestions = []
    for word in dictionary:
        lev_automaton = LevenshteinAutomaton(word, max_distance)
        lev_automaton.build_automaton()
        if lev_automaton.match(input_word):
            suggestions.append(word)
    return suggestions


def main():
    filepath = "russian.txt"
    dictionary = load_dictionary(filepath)

    if not dictionary:
        print("Словарь пуст или отсутствует. Начните добавлять слова.")

    input_word = input("Введите слово: ").strip()
    max_distance = 1

    suggestions = suggest_word(input_word, dictionary, max_distance)

    if suggestions:
        print("Возможно, вы имели в виду:")
        for suggestion in suggestions:
            print(f" - {suggestion}")
    else:
        print("Совпадений не найдено.")
        add_to_dict = input("Добавить слово в словарь? (да/нет): ").strip().lower()
        if add_to_dict == "да":
            dictionary.append(input_word)
            save_to_dictionary(filepath, dictionary)
            print(f"Слово '{input_word}' добавлено в словарь.")


if __name__ == "__main__":
    main()
