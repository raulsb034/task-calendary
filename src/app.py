import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.controllers import TaskCalendarController
from src.views import TaskCalendarView


def main() -> None:
    controller = TaskCalendarController()
    view = TaskCalendarView(controller)
    view.run()


if __name__ == "__main__":
    main()
