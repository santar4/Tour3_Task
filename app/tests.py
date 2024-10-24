import os
from io import BytesIO

from app import file_processor, FileWorker

import unittest


class FileProcessorTests(unittest.TestCase):

    def test_process_compress(self):
        class MockFile:
            def __init__(self, filename, data):
                self.filename = filename
                self.data = data

            def save(self, filepath):
                with open(filepath, 'wb') as f:
                    f.write(self.data)

        file = MockFile('test.txt', b'AAABBBCCC')
        output_file = file_processor.process_file(file, file.filename, 'compress')

        # Перевіряємо, що назва файла починається з "compressed_"
        self.assertTrue(output_file.startswith('compressed_'))

    def test_process_decompress(self):
        class MockFile:
            def __init__(self, filename, data):
                self.filename = filename
                self.data = data

            def save(self, filepath):
                with open(filepath, 'wb') as f:
                    f.write(self.data)

        file = MockFile('test.txt', b'A3B3C3')
        output_file = file_processor.process_file(file, file.filename, 'decompress')

        # Перевіряємо, що назва файла починається з "decompressed_"
        self.assertTrue(output_file.startswith('decompressed_'))


class TestFileWorker(unittest.TestCase):
    """Тести для FileWorker класу."""

    def setUp(self):
        """Ініціалізація об'єкта FileWorker перед кожним тестом."""
        self.file_handler = FileWorker(upload_folder='test_uploads')
        os.makedirs(self.file_handler.upload_folder, exist_ok=True)

    def tearDown(self):
        """Очистка тестових файлів після кожного тесту."""
        for file in os.listdir(self.file_handler.upload_folder):
            os.remove(os.path.join(self.file_handler.upload_folder, file))
        os.rmdir(self.file_handler.upload_folder)

    def test_save_file(self):
        """Тестуємо збереження файлу."""
        test_data = b'Test data'  # Замість BytesIO, просто байти
        filename = 'test.txt'
        file_path = self.file_handler.save_bytes(test_data, filename)  # Використовуємо save_bytes
        self.assertTrue(os.path.exists(file_path))

    def test_read_file(self):
        """Тестуємо запис і зчитування файлу."""
        filename = 'test.txt'
        with open(os.path.join(self.file_handler.upload_folder, filename), 'wb') as f:
            f.write(b'Test data')
        data = self.file_handler.read_file(os.path.join(self.file_handler.upload_folder, filename))
        self.assertEqual(data, b'Test data')

    def test_write_file(self):
        """Тестуємо запис даних у файл."""
        filename = 'test_output.txt'
        self.file_handler.write_file(os.path.join(self.file_handler.upload_folder, filename), b'Output data')
        with open(os.path.join(self.file_handler.upload_folder, filename), 'rb') as f:
            data = f.read()
        self.assertEqual(data, b'Output data')

    def test_get_file_size(self):
        """Тестуємо отримання розміру файлу."""
        filename = 'test.txt'
        with open(os.path.join(self.file_handler.upload_folder, filename), 'wb') as f:
            f.write(b'Test data')
        size = self.file_handler.get_file_size(os.path.join(self.file_handler.upload_folder, filename))
        self.assertEqual(size, len(b'Test data'))


if __name__ == '__main__':
    unittest.main()
