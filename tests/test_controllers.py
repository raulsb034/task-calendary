import unittest
from datetime import date, time

from src.controllers import TaskCalendarController
from src.models import TaskPriority, TaskStatus


class TestController(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = TaskCalendarController()
        self.controller.tasks = []
        self.controller._next_task_id = 1
        self.controller.events = []
        self.controller._next_event_id = 1

    def test_add_and_retrieve_task(self):
        task = self.controller.add_task(
            title="Escribir código",
            description="Prueba",
            due_date=date.today(),
            due_time=time(10, 0),
            priority=TaskPriority.HIGH.value,
            category="Trabajo",
        )
        self.assertEqual(task.title, "Escribir código")
        self.assertEqual(task.priority, TaskPriority.HIGH.value)
        self.assertEqual(task.category.value, "Trabajo")
        self.assertEqual(len(self.controller.list_tasks()), 1)

    def test_update_task(self):
        task = self.controller.add_task(
            title="Original",
            description="",
            due_date=date.today(),
            due_time=time(9, 0),
            priority=TaskPriority.MEDIUM.value,
            category="Estudio",
        )
        updated = self.controller.update_task(
            task.id,
            title="Actualizado",
            description="Nuevo",
            due_date=date.today(),
            due_time=time(11, 0),
            priority=TaskPriority.LOW.value,
            category="Personal",
        )
        self.assertEqual(updated.title, "Actualizado")
        self.assertEqual(updated.priority, TaskPriority.LOW.value)
        self.assertEqual(updated.category.value, "Personal")

    def test_delete_task(self):
        task = self.controller.add_task(
            title="Eliminar",
            description="",
            due_date=date.today(),
            due_time=time(9, 0),
            priority=TaskPriority.MEDIUM.value,
            category="Trabajo",
        )
        self.controller.delete_task(task.id)
        self.assertEqual(len(self.controller.list_tasks()), 0)

    def test_mark_task_completed(self):
        task = self.controller.add_task(
            title="Completar",
            description="",
            due_date=date.today(),
            due_time=time(9, 0),
            priority=TaskPriority.MEDIUM.value,
            category="Estudio",
        )
        completed = self.controller.mark_task_completed(task.id)
        self.assertEqual(completed.status, TaskStatus.COMPLETED)

    def test_search_tasks_by_filters(self):
        self.controller.add_task(
            title="Revisión de proyecto",
            description="",
            due_date=date.today(),
            due_time=time(9, 0),
            priority=TaskPriority.HIGH.value,
            category="Trabajo",
        )
        self.controller.add_task(
            title="Estudiar Python",
            description="",
            due_date=date.today(),
            due_time=time(10, 0),
            priority=TaskPriority.MEDIUM.value,
            category="Estudio",
        )
        results = self.controller.search_tasks(name="Python", priority=None, category=None)
        self.assertEqual(len(results), 1)
        self.assertIn("Python", results[0].title)

    def test_search_tasks_without_criteria_raises(self):
        with self.assertRaises(ValueError):
            self.controller.search_tasks(name=None, priority=None, category=None)

    def test_get_stats_counts(self):
        self.controller.add_task(
            title="Pendiente",
            description="",
            due_date=date.today(),
            due_time=time(9, 0),
            priority=TaskPriority.MEDIUM.value,
            category="Trabajo",
        )
        task = self.controller.add_task(
            title="Completada",
            description="",
            due_date=date.today(),
            due_time=time(10, 0),
            priority=TaskPriority.LOW.value,
            category="Personal",
        )
        self.controller.mark_task_completed(task.id)
        stats = self.controller.get_stats()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["pending"], 1)

    def test_invalid_past_date_raises(self):
        with self.assertRaises(ValueError):
            self.controller.add_task(
                title="Antigua",
                description="",
                due_date=date(2000, 1, 1),
                due_time=time(9, 0),
                priority=TaskPriority.MEDIUM.value,
                category="Trabajo",
            )

    def test_invalid_category_raises(self):
        with self.assertRaises(ValueError):
            self.controller.add_task(
                title="Categoría mala",
                description="",
                due_date=date.today(),
                due_time=time(9, 0),
                priority=TaskPriority.MEDIUM.value,
                category="Otra",
            )

    def test_tasks_for_date_sorted_by_time_and_priority(self):
        self.controller.add_task(
            title="Tarea tarde",
            description="",
            due_date=date.today(),
            due_time=time(17, 0),
            priority=TaskPriority.LOW.value,
            category="Trabajo",
        )
        self.controller.add_task(
            title="Tarea mañana",
            description="",
            due_date=date.today(),
            due_time=time(9, 0),
            priority=TaskPriority.HIGH.value,
            category="Estudio",
        )
        tasks = self.controller.list_tasks_for_date(date.today())
        self.assertEqual(tasks[0].title, "Tarea mañana")
