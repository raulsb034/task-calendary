import unittest
from datetime import date, time, timedelta

from src.controllers import TaskCalendarController
from src.models import TaskPriority, TaskStatus


class TestFunctionalRegression(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = TaskCalendarController()

    def test_create_update_delete_task_flow(self):
        due_date = date.today() + timedelta(days=2)
        task = self.controller.add_task(
            title="Reunión de producto",
            description="Revisar backlog",
            due_date=due_date,
            due_time=time(14, 0),
            priority=TaskPriority.HIGH.value,
            category="Trabajo",
        )
        self.assertIn(task, self.controller.list_tasks())
        self.assertEqual(task.title, "Reunión de producto")

        updated = self.controller.update_task(
            task.id,
            title="Reunión de diseño",
            description="Ajustar prioridades",
            due_date=due_date,
            due_time=time(15, 0),
            priority=TaskPriority.MEDIUM.value,
            category="Estudio",
        )
        self.assertEqual(updated.title, "Reunión de diseño")
        self.assertEqual(updated.priority, TaskPriority.MEDIUM.value)
        self.assertEqual(updated.category.value, "Estudio")

        self.controller.delete_task(task.id)
        self.assertNotIn(task, self.controller.list_tasks())

    def test_search_filters_and_statistics(self):
        self.controller.add_task(
            title="Preparar informe funcional",
            description="Resumen mensual",
            due_date=date.today() + timedelta(days=1),
            due_time=time(10, 0),
            priority=TaskPriority.MEDIUM.value,
            category="Trabajo",
        )
        self.controller.add_task(
            title="Estudiar pruebas automáticas",
            description="Agregar casos de uso",
            due_date=date.today() + timedelta(days=1),
            due_time=time(11, 0),
            priority=TaskPriority.HIGH.value,
            category="Estudio",
        )
        results = self.controller.search_tasks(name="Preparar informe funcional", priority=None, category=None)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Preparar informe funcional")

        stats = self.controller.get_stats()
        self.assertGreaterEqual(stats["total"], 2)
        self.assertGreaterEqual(stats["pending"], 1)

    def test_seeded_tasks_are_present(self):
        self.assertGreaterEqual(len(self.controller.tasks), 3)
        today = date.today()
        for task in self.controller.tasks:
            self.assertTrue(task.due_date >= today)
            self.assertTrue(task.category.value in {"Estudio", "Trabajo", "Personal"})

    def test_regression_search_requires_at_least_one_criteria(self):
        with self.assertRaises(ValueError):
            self.controller.search_tasks(name=None, priority=None, category=None)

    def test_regression_update_rejects_past_due_date(self):
        task = self.controller.add_task(
            title="Prueba futura",
            description="",
            due_date=date.today() + timedelta(days=3),
            due_time=time(12, 0),
            priority=TaskPriority.MEDIUM.value,
            category="Trabajo",
        )
        with self.assertRaises(ValueError):
            self.controller.update_task(
                task.id,
                title="Prueba pasada",
                description="",
                due_date=date(2000, 1, 1),
                due_time=time(9, 0),
                priority=TaskPriority.MEDIUM.value,
                category="Trabajo",
            )
