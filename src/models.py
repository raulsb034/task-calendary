from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time
from enum import Enum
from typing import ClassVar, Dict, Optional


class TaskStatus(Enum):
    PENDING = "Pendiente"
    COMPLETED = "Completada"


class TaskCategory(Enum):
    ESTUDIO = "Estudio"
    TRABAJO = "Trabajo"
    PERSONAL = "Personal"


class TaskPriority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

    @classmethod
    def label(cls, value: int) -> str:
        labels = {
            cls.HIGH.value: "Alta",
            cls.MEDIUM.value: "Media",
            cls.LOW.value: "Baja",
        }
        return labels.get(value, "Media")

    @classmethod
    def color(cls, value: int) -> str:
        colors = {
            cls.HIGH.value: "#ff6b6b",
            cls.MEDIUM.value: "#4caf50",
            cls.LOW.value: "#2196f3",
        }
        return colors.get(value, "#2196f3")


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    category: TaskCategory = TaskCategory.TRABAJO
    status: TaskStatus = TaskStatus.PENDING
    priority: int = TaskPriority.MEDIUM.value
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def priority_label(self) -> str:
        return TaskPriority.label(self.priority)

    @property
    def priority_color(self) -> str:
        return TaskPriority.color(self.priority)

    @property
    def category_label(self) -> str:
        return self.category.value

    def mark_completed(self) -> None:
        self.status = TaskStatus.COMPLETED

    def is_overdue(self, current_date: Optional[date] = None) -> bool:
        if self.due_date is None:
            return False
        if current_date is None:
            current_date = date.today()
        return self.status == TaskStatus.PENDING and self.due_date < current_date


@dataclass
class Event:
    id: int
    title: str
    event_date: date
    start_time: time
    end_time: time
    description: str = ""

    def duration_minutes(self) -> int:
        start_minutes = self.start_time.hour * 60 + self.start_time.minute
        end_minutes = self.end_time.hour * 60 + self.end_time.minute
        return max(0, end_minutes - start_minutes)

    def overlaps(self, other: Event) -> bool:
        if self.event_date != other.event_date:
            return False
        return self.start_time < other.end_time and other.start_time < self.end_time
