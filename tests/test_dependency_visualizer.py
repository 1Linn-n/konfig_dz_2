import unittest
from unittest.mock import patch, mock_open
import sys
import os
import io
import tarfile
from unittest.mock import patch, mock_open

# Добавляем основную директорию проекта в путь поиска модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dependency_visualizer import DependencyVisualizer

class TestDependencyVisualizer(unittest.TestCase):

    def setUp(self):
        """Настраивает тестовые данные."""
        self.apkindex_url = "http://example.com/APKINDEX.tar.gz"
        self.output_puml = "dependencies.puml"
        self.visualizer = DependencyVisualizer(self.apkindex_url, self.output_puml)

    @patch('dependency_visualizer.DependencyVisualizer.fetch_apkindex')
    @patch('dependency_visualizer.DependencyVisualizer.parse_apkindex')
    def test_run(self, mock_parse_apkindex, mock_fetch_apkindex):
        """Тестирует основной метод run."""
        mock_parse_apkindex.return_value = {
            'example-package': ['dep1', 'dep2'],
            'dep1': ['subdep1'],
            'dep2': [],
            'subdep1': []
        }
        self.visualizer.run()
        mock_fetch_apkindex.assert_called_once()
        mock_parse_apkindex.assert_called_once()

    @patch('requests.get')
    @patch('tarfile.open')
    def test_fetch_apkindex(self, mock_tarfile_open, mock_get):
        """Тестирует загрузку APKINDEX."""

        # Создаём тестовые данные для tar.gz в памяти
        tar_data = io.BytesIO()
        with tarfile.open(fileobj=tar_data, mode="w:gz") as tar:
            # Добавляем файл внутри архива
            info = tarfile.TarInfo(name="dummy.txt")
            info.size = len("dummy content")
            tar.addfile(info, io.BytesIO(b"dummy content"))

        # Перемещаем курсор в начало, чтобы можно было читать данные
        tar_data.seek(0)

        # Мокируем ответ от requests.get, чтобы он возвращал данные tar.gz
        mock_get.return_value.content = tar_data.read()
        mock_get.return_value.raise_for_status = lambda: None

        # Мокируем первый вызов tarfile.open для записи (создание архива)
        mock_tarfile = mock_tarfile_open.return_value.__enter__.return_value
        mock_tarfile.getnames.return_value = ["dummy.txt"]  # Пример имени файла в архиве
        mock_tarfile.extractall = lambda path: None  # Мокируем метод извлечения файлов

        # Вызываем метод, который должен работать с tar-файлом
        with patch('builtins.open', mock_open()) as mocked_open:
            self.visualizer.fetch_apkindex()

            # Проверяем, что open() был вызван правильно
            mocked_open.assert_called_with("APKINDEX.tar.gz", "wb")

        # Проверяем, что tarfile.open был вызван дважды: для записи и для извлечения
        mock_tarfile_open.assert_any_call("APKINDEX.tar.gz", "r:gz")
        mock_tarfile_open.assert_any_call(fileobj=tar_data, mode="w:gz")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data="C:\nP: example-package\nD: dep1 dep2\nC:\nP: dep1\nD: subdep1\nC:\nP: dep2\nD:\nC:\nP: subdep1\nD:")
    def test_parse_apkindex(self, mock_open, mock_exists):
        """Тестирует парсинг APKINDEX."""
        mock_exists.return_value = True
        dependencies = self.visualizer.parse_apkindex()
        self.assertIn('example-package', dependencies)
        self.assertIn('dep1', dependencies['example-package'])
        self.assertIn('dep2', dependencies['example-package'])
        self.assertIn('subdep1', dependencies['dep1'])

    def test_create_dependency_graph(self):
        """Тестирует создание графа зависимостей."""
        dependencies = {
            'example-package': ['dep1', 'dep2'],
            'dep1': ['subdep1'],
            'dep2': [],
            'subdep1': []
        }
        graph = self.visualizer.create_dependency_graph(dependencies)
        self.assertIn('dep1', graph['example-package'])
        self.assertIn('dep2', graph['example-package'])
        self.assertIn('subdep1', graph['dep1'])

    @patch('builtins.open', new_callable=mock_open)
    def test_visualize_graph(self, mock_open):
        """Тестирует генерацию PlantUML."""
        graph = {
            'example-package': ['dep1', 'dep2'],
            'dep1': ['subdep1'],
            'dep2': [],
            'subdep1': []
        }
        self.visualizer.visualize_graph(graph)
        mock_open.assert_called_with(self.output_puml, 'w', encoding='utf-8')
        mock_open().write.assert_any_call("@startuml\n")
        mock_open().write.assert_any_call('"example-package" --> "dep1"\n')
        mock_open().write.assert_any_call('"example-package" --> "dep2"\n')
        mock_open().write.assert_any_call('"dep1" --> "subdep1"\n')
        mock_open().write.assert_any_call("@enduml\n")

if __name__ == '__main__':
    unittest.main()
