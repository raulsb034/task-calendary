import unittest
from datetime import date, time

from src.models import Event, Task, TaskCategory, TaskPriority, TaskStatus


class TestModels(unittest.TestCase):
    def test_task_mark_completed_and_overdue(self):
        task = Task(
            id=1,
            title="Comprar leche",
            due_date=date.today(),
            due_time=time(10, 0),
            category=TaskCategory.ESTUDIO,
            priority=TaskPriority.HIGH.value,
        )
        self.assertFalse(task.is_overdue(date.today()))
        task.mark_completed()
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertFalse(task.is_overdue(date.today()))

    def test_task_overdue_when_due_date_passed(self):
        task = Task(
            id=2,
            title="Reportar bug",
            due_date=date(2000, 1, 1),
            due_time=time(9, 0),
            category=TaskCategory.TRABAJO,
            priority=TaskPriority.MEDIUM.value,
        )
        self.assertTrue(task.is_overdue(date(2000, 1, 2)))

    def test_task_priority_labels_and_colors(self):
        task = Task(
            id=3,
            title="Prioridad alta",
            due_date=date.today(),
            due_time=time(8, 0),
            category=TaskCategory.PERSONAL,
            priority=TaskPriority.HIGH.value,
        )
        self.assertEqual(task.priority_label, "Alta")
        self.assertEqual(task.priority_color, "#ff6b6b")

    def test_event_duration_and_overlap(self):
        event1 = Event(
            id=1,
            title="Reunión",
            event_date=date(2025, 1, 1),
            start_time=time(9, 0),
            end_time=time(10, 0),
        )
        event2 = Event(
            id=2,
            title="Revisión",
            event_date=date(2025, 1, 1),
            start_time=time(9, 30),
            end_time=time(11, 0),
        )
        self.assertEqual(event1.duration_minutes(), 60)
        self.assertTrue(event1.overlaps(event2))

    def test_event_non_overlapping_different_day(self):
        event1 = Event(
            id=3,
            title="Capacitación",
            event_date=date(2025, 1, 1),
            start_time=time(14, 0),
            end_time=time(15, 0),
        )
        event2 = Event(
            id=4,
            title="Llamada",
            event_date=date(2025, 1, 2),
            start_time=time(14, 0),
            end_time=time(15, 0),
        )
        self.assertFalse(event1.overlaps(event2))
