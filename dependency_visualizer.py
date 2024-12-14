import re
from collections import defaultdict
import requests
import tarfile
import os

class DependencyVisualizer:
    def __init__(self, apkindex_url, output_puml):
        self.apkindex_url = apkindex_url
        self.output_puml = output_puml
        self.apkindex_file = "APKINDEX"  # Локальный файл после загрузки

    def fetch_apkindex(self):
        """Загружает APKINDEX.tar.gz и извлекает его содержимое."""
        print(f"Fetching APKINDEX from {self.apkindex_url}")
        response = requests.get(self.apkindex_url)
        response.raise_for_status()
        with open("APKINDEX.tar.gz", "wb") as f:
            f.write(response.content)

        with tarfile.open("APKINDEX.tar.gz", "r:gz") as tar:
            tar.extractall(path=".")

    def parse_apkindex(self):
        """Парсит файл APKINDEX и извлекает зависимости пакетов."""
        if not os.path.exists(self.apkindex_file):
            raise FileNotFoundError(f"{self.apkindex_file} not found. Make sure it's downloaded.")

        with open(self.apkindex_file, 'r', encoding='utf-8') as f:
            data = f.read()

        # Регулярное выражение для выделения секций пакетов
        sections = re.split(r'\n(?=C:)', data)
        package_dependencies = {}

        for section in sections:
            lines = section.strip().split('\n')
            pkg_name = None
            dependencies = []

            for line in lines:
                if line.startswith("P:"):
                    pkg_name = line[2:].strip()
                elif line.startswith("D:"):
                    dependencies = line[2:].strip().split()

            if pkg_name:
                package_dependencies[pkg_name] = dependencies

        return package_dependencies

    def create_dependency_graph(self, dependencies):
        """Создаёт граф зависимостей в формате словаря."""
        graph = defaultdict(list)
        for pkg, deps in dependencies.items():
            for dep in deps:
                graph[pkg].append(dep)
        return graph

    def visualize_graph(self, graph):
        """Генерирует файл dependencies.puml для визуализации графа."""
        with open(self.output_puml, 'w', encoding='utf-8') as f:
            f.write("@startuml\n")
            for pkg, deps in graph.items():
                for dep in deps:
                    f.write(f'"{pkg}" --> "{dep}"\n')
            f.write("@enduml\n")

        print(f"Граф зависимостей сохранён в {self.output_puml}")

    def run(self):
        """Основной метод для выполнения всех шагов."""
        self.fetch_apkindex()
        dependencies = self.parse_apkindex()
        graph = self.create_dependency_graph(dependencies)
        self.visualize_graph(graph)

if __name__ == "__main__":
    APKINDEX_URL = "http://dl-cdn.alpinelinux.org/alpine/v3.12/main/x86/APKINDEX.tar.gz"
    OUTPUT_PUML = "dependencies.puml"

    visualizer = DependencyVisualizer(APKINDEX_URL, OUTPUT_PUML)
    visualizer.run()
