if __name__ == '__main__':
    import unittest
    from dependency_visualizer.dependency_visualizer import DependencyVisualizer

    class TestDependencyVisualizer(unittest.TestCase):

        def setUp(self):
            """Настраивает тестовые данные."""
            self.visualizer = DependencyVisualizer('config.csv')
            self.visualizer.dependencies = {
                'example-package': ['dep1', 'dep2'],
                'dep1': ['subdep1'],
                'dep2': [],
                'subdep1': []
            }

        def test_load_config(self):
            """Тестирует загрузку конфигурации."""
            self.assertEqual(self.visualizer.package_name, 'example-package')
            self.assertEqual(self.visualizer.max_depth, 3)

        def test_get_dependencies(self):
            """Тестирует получение зависимостей."""
            result = self.visualizer.get_dependencies('example-package')
            self.assertIn('dep1', result)
            self.assertIn('dep2', result)
            self.assertIn('subdep1', result)

        def test_generate_plantuml(self):
            """Тестирует генерацию PlantUML."""
            plantuml_code = self.visualizer.generate_plantuml()
            self.assertIn('@startuml', plantuml_code)
            self.assertIn('example-package --> dep1', plantuml_code)
            self.assertIn('@enduml', plantuml_code)

    unittest.main()