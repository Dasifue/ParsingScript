class FileExtensionError(Exception):
    def __init__(self, message: str = "Ошибка расширения файла"):
        self.message = message
        super().__init__(self.message)