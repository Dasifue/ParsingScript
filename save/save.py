import json
import csv

from .file_error import FileExtensionError

class SaveData:

    def __init__(self, path: str = None, echo: bool = False):
        self.path = path
        self.echo = echo

    def file_path(self, file_name: str) -> str:
        if self.path.endswith('/'):
            file_name = f"{self.path}{file_name}"
        else:
            file_name = f"{self.path}/{file_name}"
        return file_name


    def save_in_txt(self, file_name: str, data: dict) -> None:
        """
        Метод сохраняет данные о публикации в txt файле

        Параметры:
        - file_name: str = название или путь к файлу
        - data: dict = данные о публикации
        """
        if not file_name.endswith(".txt"):
            raise FileExtensionError("Файл должен иметь расширение .txt")
        
        if self.path is not None:
            file_name = self.file_path(file_name=file_name)        

        with open(file=file_name, mode="a", encoding="utf-8") as file: #безопасное открытие файла
            text = f"{data}\n\n\n" #форматирование текста
            file.write(text) #запись текста в файл

            if self.echo == True:
                print(f"В файл {file_name} были записаны данные: {data}")


    def save_in_csv(self, file_name: str, data: dict) -> None:
        """
        Метод сохраняет данные о публикации в csv файле

        Параметры:
        - file_name: str = название или путь к файлу
        - data: dict = данные о публикации
        """

        if not file_name.endswith(".csv"):
            raise FileExtensionError("Файл должен иметь расширение .csv")
        
        if self.path is not None:
            file_name = self.file_path(file_name=file_name)
        
        with open(file=file_name, mode="a", encoding="utf-8") as file:
            writer = csv.DictWriter(f=file, fieldnames=data.keys()) #инициализация объекта класса с передачей ключей
            writer.writeheader() #создание столбцов 
            writer.writerow(data) # создание строк

            if self.echo == True:
                print(f"В файл {file_name} были записаны данные: {data}")

    
    def save_in_json(self, file_name: str, data: str) -> None:
        """
        Метод сохраняет данные о публикации в json файле

        Параметры:
        - file_name: str = название или путь к файлу
        - data: dict = данные о публикации
        """
        if not file_name.endswith(".json"):
            raise FileExtensionError("Файл должен иметь расширение .json")
        
        if self.path is not None:
            file_name = self.file_path(file_name=file_name)
        
        with open(file=file_name, mode="a", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False) #сохранение данных в json файл
    
            if self.echo == True:
                print(f"В файл {file_name} были записаны данные: {data}")
