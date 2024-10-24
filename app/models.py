import os
from app.decorators import measure_time


class Compressionfunc:
    """Інтерфейс для функцій стискання і розпакування."""

    def compress(self, data: bytes) -> bytes:
        raise NotImplementedError

    def decompress(self, data: bytes) -> bytes:
        raise NotImplementedError


class RLECompression(Compressionfunc):
    """Алгоритм стискання RLE."""

    def compress(self, data: bytes) -> bytes:
        encoding = bytearray()
        i = 0

        while i < len(data):
            count = 1
            while i + 1 < len(data) and data[i] == data[i + 1]:
                count += 1
                i += 1

            encoding.append(data[i])
            encoding.extend(str(count).encode())  # Додаємо кількість повторень як байти
            i += 1

        return bytes(encoding)

    def decompress(self, data: bytes) -> bytes:
        """Алгоритм розпакування RLE."""
        decoding = bytearray()
        i = 0

        while i < len(data):
            char = data[i]  # Зчитуємо байт (символ)
            i += 1

            count = 0
            # Зчитуємо кількість повторень символу
            while i < len(data) and chr(data[i]).isdigit():
                try:
                    count = count * 10 + int(chr(data[i]))  # Перетворюємо символ на число
                except ValueError:
                    print(f"Невідомий символ: {data[i]}")  # Додаємо лог для помилкового запиту
                    count = 1  # Якщо трапиться помилка, то count будемо приймати як 1
                i += 1

            if count == 0:
                count = 1  # Якщо не було чисел, то мінімальна кількість буде = 1

            decoding.extend([char] * count)  # Додаємо символ до результату стільки разів, скільки зазначено

        return bytes(decoding)


class FileWorker:
    """Клас для роботи з файлами."""

    def __init__(self, upload_folder: str):
        self.upload_folder = upload_folder

    def save_file(self, file, filename: str) -> str:
        """Зберігаєм файл на диску."""
        file_path = os.path.join(self.upload_folder, filename)
        file.save(file_path)
        return file_path

    def read_file(self, file_path: str) -> bytes:
        """Зчитує файл у байтах."""
        with open(file_path, 'rb') as f:
            data = f.read()
            return data

    def write_file(self, file_path: str, data: bytes) -> None:
        """Записує дані у файл."""
        with open(file_path, 'wb') as f:
            f.write(data)

    def get_file_size(self, file_path: str) -> int:
        """Повертаємо розмір файлу."""
        return os.path.getsize(file_path)


class FileProcessor:
    """Клас для стиснення та розпакування файлів."""

    def __init__(self, strategy: Compressionfunc, file_handler: FileWorker):
        self.strategy = strategy
        self.file_handler = file_handler

    @measure_time
    def process_file(self, file, filename: str, operation: str) -> str:
        file_path = self.file_handler.save_file(file, filename)

        # Читаємо дані файлу
        data = self.file_handler.read_file(file_path)

        # Обробляємо залежно від операції
        if operation == 'compress':
            processed_data = self.strategy.compress(data)
            output_file = 'compressed_' + filename  # Правильна назва файлу
            output_file = output_file.replace(" ", "_")
        elif operation == 'decompress':
            processed_data = self.strategy.decompress(data)
            output_file = 'decompressed_' + filename  # Правильна назва файлу
            output_file = output_file.replace(" ", "_")
        else:
            raise ValueError("Невідома операція")

        output_path = os.path.join(self.file_handler.upload_folder, output_file)
        self.file_handler.write_file(output_path, processed_data)

        print(f"Generated file: {output_file}")  # Додаємо лог для перевірки

        return output_file



