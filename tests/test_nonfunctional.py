import unittest
import time as time_module
from datetime import date, time, timedelta

from src.controllers import TaskCalendarController
from src.models import TaskPriority


class TestNonFunctional(unittest.TestCase):
    def test_get_tasks_for_month_performance(self):
        controller = TaskCalendarController()
        base_date = date.today() + timedelta(days=1)
        for index in range(300):
            controller.add_task(
                title=f"Tarea perfor-{index}",
                description="Carga de estrés",
                due_date=base_date,
                due_time=time(8 + (index % 8), 0),
                priority=TaskPriority.MEDIUM.value,
                category="Trabajo",
            )
        start = time_module.perf_counter()
        tasks = controller.get_tasks_for_month(base_date.year, base_date.month)
        elapsed = time_module.perf_counter() - start
        self.assertLess(elapsed, 0.5, f"El filtrado del mes tarda demasiado: {elapsed:.3f}s")
        self.assertGreaterEqual(len(tasks), 300)

    def test_priority_color_values(self):
        self.assertEqual(TaskPriority.HIGH.color(TaskPriority.HIGH.value), "#ff6b6b")
        self.assertEqual(TaskPriority.MEDIUM.color(TaskPriority.MEDIUM.value), "#4caf50")
        self.assertEqual(TaskPriority.LOW.color(TaskPriority.LOW.value), "#2196f3")

    def test_category_normalization_is_strict(self):
        controller = TaskCalendarController()
        with self.assertRaises(ValueError):
            controller.add_task(
                title="Categoría inválida",
                description="",
                due_date=date.today() + timedelta(days=1),
                due_time=time(9, 0),
                priority=TaskPriority.MEDIUM.value,
                category="Invalid",
            )
