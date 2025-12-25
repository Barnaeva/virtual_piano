import json
import pygame
import os

def read_json(filename: str) -> dict:
    """
    Read a JSON file and return a dictionary.

    :param filename: The name of the JSON file.
    :return: A dictionary with the data.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"JSON format error in file {filename}: {e}")
        return {}
    except Exception as exc:
        print(f"Error reading JSON: {exc}")
        return {}


def write_json(filename: str, data: dict) -> None:
    """
    Write data to a JSON file.

    :param filename: The name of the file to write.
    :param data: The data to write.
    """
    try:
        os.makedirs("melodies", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except PermissionError:
        print(f"No permission to write to file {filename}.")
    except Exception as exc:
        print(f"Error writing JSON: {exc}")


def add_mel_json(filename: str, melody_data: dict) -> bool:
    """Добавить сохраненную мелодию в указанный файл как элемент массива"""
    try:
        # 1. Проверяем и создаем папку если нужно
        folder = os.path.dirname(filename)
        if folder:
            os.makedirs(folder, exist_ok=True)

        # 2. Если файла нет - создаем массив с одной мелодией
        if not os.path.exists(filename):
            melodies = [melody_data]  # ← ПЕРВАЯ МЕЛОДИЯ В МАССИВЕ
            print(f"📁 Создан новый файл с первой мелодией: {filename}")

        # 3. Если файл есть - читаем и добавляем
        else:
            with open(filename, 'r', encoding='utf-8') as f:
                content = json.load(f)

            # Проверяем формат
            if isinstance(content, list):
                melodies = content
                melodies.append(melody_data)  # ← ДОБАВЛЯЕМ В МАССИВ
            elif isinstance(content, dict):
                # Если уже есть одна мелодия как объект - делаем массив из двух
                melodies = [content, melody_data]
                print(f"⚠️ Преобразовано в массив: {filename}")
            else:
                # Неизвестный формат - начинаем с массива с одной мелодией
                melodies = [melody_data]
                print(f"⚠️ Неизвестный формат, создан новый массив: {filename}")

        # 4. Сохраняем как массив
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(melodies, f, ensure_ascii=False, indent=2)

        print(f"✅ Добавлено в {filename}, всего: {len(melodies)} мелодий")
        return True

    except Exception as e:
        print(f"❌ Ошибка добавления в {filename}: {e}")
        return False


def update_melody_name(filename, old_name, new_name):
    """Обновляет имя мелодии в JSON файле"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            melodies = json.load(file)

        # Ищем мелодию по старому имени
        for melody in melodies:
            if melody.get('name') == old_name:
                melody['name'] = new_name
                break

        # Сохраняем обратно
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(melodies, file, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        print(f"Ошибка обновления имени мелодии: {e}")
        return False


def load_icon(filename: str):
    """Загружает иконку из файла"""
    try:
        icon = pygame.image.load(filename).convert_alpha()
        return icon
    except Exception as e:
        print(f"Не удалось загрузить иконку {filename}: {e}")
        return None


def delete_melody(filename: str,melody_name: dict):
    """
    Удаляет мелодию по имени из файла mel.json

    Args:
        melody_name: Имя мелодии для удаления (например, "Гуси")

    Returns:
        True если удалено, False если нет
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            melodies = json.load(f)

        initial_count = len(melodies)

        kept_melodies = [
            m for m in melodies
            if not (m.get("name") == melody_name and m.get("flag") == 0)
        ]

        deleted_count = initial_count - len(kept_melodies)

        if deleted_count == 0:
            print(f"⚠️ Мелодия '{melody_name}' не найдена или системная")
            return False

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(kept_melodies, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print(f"Error delete melody: {e}")
        return False