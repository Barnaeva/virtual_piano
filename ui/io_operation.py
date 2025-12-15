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


def load_icon(filename: str):
    """Загружает иконку из файла"""
    try:
        icon = pygame.image.load(filename).convert_alpha()
        return icon
    except Exception as e:
        print(f"Не удалось загрузить иконку {filename}: {e}")
        return None