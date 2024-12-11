def sort_file_alphabetically(input_filepath, output_filepath):
    """
    Сортирует содержимое файла по алфавиту и сохраняет в новый файл.

    input_filepath: Путь к исходному файлу.
    output_filepath: Путь к файлу, куда будет записан результат.
    """
    try:
        # Чтение строк из файла
        with open(input_filepath, 'r', encoding='windows-1251') as file:
            lines = file.readlines()

        # Удаление лишних пробелов и пустых строк
        lines = [line.strip() for line in lines if line.strip()]

        # Сортировка строк
        lines.sort()

        # Запись отсортированных строк в новый файл
        with open(output_filepath, 'w', encoding='windows-1251') as file:
            file.write('\n'.join(lines))

        print(f"Файл успешно отсортирован и сохранён в: {output_filepath}")

    except FileNotFoundError:
        print(f"Ошибка: Файл {input_filepath} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример использования
input_file = 'russian.txt'  # Исходный файл
output_file = 'sorted_words.txt'  # Файл для сохранения результата
sort_file_alphabetically(input_file, output_file)
