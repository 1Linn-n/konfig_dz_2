# Dependency Visualizer

## Общее описание

Dependency Visualizer — это инструмент командной строки для визуализации графа зависимостей пакетов в Alpine Linux. Он использует файл APKINDEX для получения зависимостей пакетов и генерирует граф в формате PlantUML, который затем можно визуализировать с помощью внешней программы, такой как PlantUML.

## Описание всех функций и настроек

### Функции

- **fetch_apkindex**: Загружает APKINDEX.tar.gz и извлекает его содержимое.
- **parse_apkindex**: Парсит файл APKINDEX и извлекает зависимости пакетов.
- **create_dependency_graph**: Создаёт граф зависимостей в формате словаря.
- **visualize_graph**: Генерирует файл dependencies.puml для визуализации графа.
- **run**: Основной метод для выполнения всех шагов.

### Настройки

Конфигурационный файл `config.csv` содержит следующие параметры:

- `path_to_visualizer`: Путь к программе для визуализации графов (например, PlantUML).
- `package_name`: Имя анализируемого пакета.
- `max_depth`: Максимальная глубина анализа зависимостей.
- `repository_url`: URL-адрес репозитория.

## Описание команд для сборки проекта

### Установка зависимостей:

```sh
pip install -r requirements.txt
```

### Запуск инструмента:

```sh
python dependency_visualizer.py
```

## Примеры использования

### Скриншоты

![Снимок экрана 2024-12-15 025947](https://github.com/user-attachments/assets/42ca4eee-6884-4ba7-84c8-d57f0555f861)

![Снимок экрана 2024-12-15 025824](https://github.com/user-attachments/assets/e885e5a6-7e60-4fde-96d7-96bad17fc9c1)



## Результаты прогона тестов

Для прогона тестов используйте следующую команду:

```sh
python -m unittest discover
```

### Пример вывода тестов

```sh
.Fetching APKINDEX from http://example.com/APKINDEX.tar.gz
..Граф зависимостей сохранён в dependencies.puml
.Граф зависимостей сохранён в dependencies.puml
.
----------------------------------------------------------------------
Ran 5 tests in 0.006s

OK
```
