from __future__ import annotations

import calendar
from datetime import date, time, timedelta
from typing import List, Optional

from .models import Event, Task, TaskCategory, TaskPriority, TaskStatus


class TaskCalendarController:
    def __init__(self) -> None:
        self._next_task_id = 1
        self._next_event_id = 1
        self.tasks: List[Task] = []
        self.events: List[Event] = []
        self._seed_sample_tasks()

    def _seed_sample_tasks(self) -> None:
        today = date.today()
        self.add_task(
            title="Reunión equipo",
            description="Planificar el sprint",
            due_date=today + timedelta(days=1),
            due_time=time(10, 0),
            priority=TaskPriority.HIGH.value,
            category="Trabajo",
        )
        self.add_task(
            title="Estudiar Tkinter",
            description="Repasar diseño de interfaz",
            due_date=today + timedelta(days=3),
            due_time=time(15, 0),
            priority=TaskPriority.MEDIUM.value,
            category="Estudio",
        )
        self.add_task(
            title="Llamada cliente",
            description="Seguimiento de proyecto",
            due_date=today + timedelta(days=5),
            due_time=time(11, 0),
            priority=TaskPriority.LOW.value,
            category="Personal",
        )

    def _next_task(self) -> int:
        current = self._next_task_id
        self._next_task_id += 1
        return current

    def _next_event(self) -> int:
        current = self._next_event_id
        self._next_event_id += 1
        return current

    def _normalize_category(self, category: str) -> TaskCategory:
        normalized = category.strip().lower()
        for candidate in TaskCategory:
            if candidate.value.lower() == normalized:
                return candidate
        raise ValueError("Categoría inválida")

    def _validate_priority(self, priority: int) -> int:
        return max(1, min(priority, TaskPriority.LOW.value))

    def _sort_tasks(self, tasks: List[Task]) -> List[Task]:
        return sorted(
            tasks,
            key=lambda task: (
                task.due_time if task.due_time is not None else time.min,
                task.priority,
            ),
        )

    def add_task(
        self,
        title: str,
        description: str,
        due_date: Optional[date],
        due_time: Optional[time],
        priority: int,
        category: str,
    ) -> Task:
        if not title.strip():
            raise ValueError("El título de la tarea no puede estar vacío")
        if due_date is None or due_time is None:
            raise ValueError("La fecha y la hora de la tarea son obligatorias")
        if due_date < date.today():
            raise ValueError("No se pueden crear tareas con fecha anterior a la actual")
        task = Task(
            id=self._next_task(),
            title=title.strip(),
            description=description.strip(),
            due_date=due_date,
            due_time=due_time,
            priority=self._validate_priority(priority),
            category=self._normalize_category(category),
        )
        self.tasks.append(task)
        return task

    def update_task(
        self,
        task_id: int,
        title: str,
        description: str,
        due_date: Optional[date],
        due_time: Optional[time],
        priority: int,
        category: str,
    ) -> Task:
        task = self.get_task(task_id)
        if not title.strip():
            raise ValueError("El título de la tarea no puede estar vacío")
        if due_date is None or due_time is None:
            raise ValueError("La fecha y la hora de la tarea son obligatorias")
        if due_date < date.today():
            raise ValueError("No se pueden modificar tareas con fecha anterior a la actual")
        task.title = title.strip()
        task.description = description.strip()
        task.due_date = due_date
        task.due_time = due_time
        task.priority = self._validate_priority(priority)
        task.category = self._normalize_category(category)
        return task

    def delete_task(self, task_id: int) -> None:
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def mark_task_completed(self, task_id: int) -> Task:
        task = self.get_task(task_id)
        task.mark_completed()
        return task

    def get_task(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"Tarea con id {task_id} no encontrada")

    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        if status is None:
            return list(self.tasks)
        return [task for task in self.tasks if task.status == status]

    def list_tasks_for_date(self, target_date: date) -> List[Task]:
        return self._sort_tasks([task for task in self.tasks if task.due_date == target_date])

    def get_tasks_for_month(
        self,
        year: int,
        month: int,
        name: Optional[str] = None,
        priority: Optional[int] = None,
        category: Optional[str] = None,
    ) -> List[Task]:
        filtered = []
        for task in self.tasks:
            if task.due_date is None:
                continue
            if task.due_date.year != year or task.due_date.month != month:
                continue
            if name and name.strip().lower() not in task.title.lower():
                continue
            if priority is not None and task.priority != priority:
                continue
            if category and category.strip().lower() != task.category.value.lower():
                continue
            filtered.append(task)
        return self._sort_tasks(filtered)

    def search_tasks(
        self,
        name: Optional[str] = None,
        priority: Optional[int] = None,
        category: Optional[str] = None,
    ) -> List[Task]:
        if not (name and name.strip()) and priority is None and not (category and category.strip()):
            raise ValueError("Debe proporcionar al menos un criterio de búsqueda")
        search_name = name.strip().lower() if name and name.strip() else None
        search_category = category.strip().lower() if category and category.strip() else None
        result = []
        for task in self.tasks:
            if search_name and search_name not in task.title.lower():
                continue
            if priority is not None and task.priority != priority:
                continue
            if search_category and search_category != task.category.value.lower():
                continue
            result.append(task)
        return self._sort_tasks(result)

    def get_stats(self) -> dict[str, int]:
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.status == TaskStatus.COMPLETED)
        pending = sum(1 for task in self.tasks if task.status == TaskStatus.PENDING)
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
        }

    def add_event(
        self,
        title: str,
        event_date: date,
        start_time: time,
        end_time: time,
        description: str = "",
    ) -> Event:
        if not title.strip():
            raise ValueError("El título del evento no puede estar vacío")
        if start_time >= end_time:
            raise ValueError("La hora de inicio debe ser anterior a la hora de fin")
        event = Event(
            id=self._next_event(),
            title=title.strip(),
            event_date=event_date,
            start_time=start_time,
            end_time=end_time,
            description=description.strip(),
        )
        self.events.append(event)
        return event

    def delete_event(self, event_id: int) -> None:
        self.events = [event for event in self.events if event.id != event_id]

    def list_events_for_date(self, target_date: date) -> List[Event]:
        return [event for event in self.events if event.event_date == target_date]
