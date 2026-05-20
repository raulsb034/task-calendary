import calendar
import tkinter as tk
from datetime import date, datetime, time
from tkinter import messagebox, ttk

from .controllers import TaskCalendarController
from .models import TaskCategory, TaskPriority, TaskStatus


class TaskCalendarView:
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M"
    PRIORITY_OPTIONS = {
        1: "Alta",
        2: "Media",
        3: "Baja",
    }
    PRIORITY_COLORS = {
        1: "#ff6b6b",
        2: "#4caf50",
        3: "#2196f3",
    }
    CATEGORY_OPTIONS = [value.value for value in TaskCategory]
    FILTER_BUTTON_COLOR = "#007bff"

    def __init__(self, controller: TaskCalendarController) -> None:
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Task Calendary")
        self.root.geometry("1000x650")
        self._selected_task_id: int | None = None
        self._selected_date: date | None = None
        self._current_month = date.today().replace(day=1)
        self.filtered_tasks = None
        self._build_interface()
        self._refresh_task_list()
        self._refresh_calendar_view()
        self._refresh_stats()

    def run(self) -> None:
        self.root.mainloop()

    def _build_interface(self) -> None:
        self.notebook = ttk.Notebook(self.root)
        self.task_tab = ttk.Frame(self.notebook)
        self.calendar_tab = ttk.Frame(self.notebook)
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.task_tab, text="Tareas")
        self.notebook.add(self.calendar_tab, text="Calendario")
        self.notebook.add(self.stats_tab, text="Estadísticas")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self._build_task_tab()
        self._build_calendar_tab()
        self._build_stats_tab()
        self._build_loading_overlay()

    def _build_task_tab(self) -> None:
        task_frame = ttk.Frame(self.task_tab, padding=12)
        task_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(task_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(left_frame, text="Lista de tareas").pack(anchor=tk.W)
        self.task_listbox = tk.Listbox(left_frame, height=24)
        self.task_listbox.pack(fill=tk.BOTH, expand=True, pady=4)
        self.task_listbox.bind("<<ListboxSelect>>", self._on_task_selected)

        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.pack(fill=tk.X, pady=6)
        ttk.Button(buttons_frame, text="Marcar completada", command=lambda: self._run_with_loading(self._complete_task)).pack(side=tk.LEFT, padx=3)
        ttk.Button(buttons_frame, text="Eliminar", command=lambda: self._run_with_loading(self._delete_task)).pack(side=tk.LEFT, padx=3)

        right_frame = ttk.Frame(task_frame, padding=(12, 0, 0, 0))
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(right_frame, text="Detalles de la tarea seleccionada").pack(anchor=tk.W)
        self.detail_text = tk.Text(right_frame, height=30, state=tk.DISABLED)
        self.detail_text.pack(fill=tk.BOTH, expand=True)

    def _build_calendar_tab(self) -> None:
        calendar_frame = ttk.Frame(self.calendar_tab, padding=12)
        calendar_frame.pack(fill=tk.BOTH, expand=True)

        filter_frame = ttk.Frame(calendar_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(filter_frame, text="Buscar nombre:").pack(side=tk.LEFT)
        self.filter_name_var = tk.StringVar()
        tk.Entry(filter_frame, textvariable=self.filter_name_var, width=22).pack(side=tk.LEFT, padx=4)

        ttk.Label(filter_frame, text="Prioridad:").pack(side=tk.LEFT, padx=(12, 0))
        self.filter_priority_var = tk.StringVar()
        self.filter_priority_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_priority_var,
            values=["", *self.PRIORITY_OPTIONS.values()],
            state="readonly",
            width=10,
        )
        self.filter_priority_combo.pack(side=tk.LEFT, padx=4)

        ttk.Label(filter_frame, text="Categoría:").pack(side=tk.LEFT, padx=(12, 0))
        self.filter_category_var = tk.StringVar()
        self.filter_category_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_category_var,
            values=["", *self.CATEGORY_OPTIONS],
            state="readonly",
            width=12,
        )
        self.filter_category_combo.pack(side=tk.LEFT, padx=4)

        tk.Button(
            filter_frame,
            text="Buscar",
            bg=self.FILTER_BUTTON_COLOR,
            fg="white",
            relief=tk.FLAT,
            command=lambda: self._run_with_loading(self._apply_filters),
        ).pack(side=tk.LEFT, padx=12)

        self.filter_message_label = ttk.Label(calendar_frame, text="", foreground="gray")
        self.filter_message_label.pack(fill=tk.X)

        month_frame = ttk.Frame(calendar_frame)
        month_frame.pack(fill=tk.X, pady=(0, 8))
        ttk.Button(month_frame, text="<", command=lambda: self._run_with_loading(self._prev_month)).pack(side=tk.LEFT)
        self.month_label = ttk.Label(month_frame, text="", font=(None, 12, "bold"))
        self.month_label.pack(side=tk.LEFT, padx=12)
        ttk.Button(month_frame, text=">", command=lambda: self._run_with_loading(self._next_month)).pack(side=tk.LEFT)

        self.calendar_grid_frame = ttk.Frame(calendar_frame)
        self.calendar_grid_frame.pack(fill=tk.BOTH, expand=True)

        self.calendar_cells = []
        for column, day_name in enumerate(["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]):
            header_label = tk.Label(self.calendar_grid_frame, text=day_name, borderwidth=1, relief=tk.RIDGE, bg="#f0f0f0")
            header_label.grid(row=0, column=column, sticky="nsew")
            self.calendar_grid_frame.columnconfigure(column, weight=1)

        for row_index in range(6):
            row_cells = []
            for col_index in range(7):
                cell_frame = tk.Frame(self.calendar_grid_frame, relief=tk.RIDGE, borderwidth=1, padx=4, pady=4, bg="white")
                cell_frame.grid(row=row_index + 1, column=col_index, sticky="nsew", padx=1, pady=1)
                self.calendar_grid_frame.rowconfigure(row_index + 1, weight=1)
                date_label = tk.Label(cell_frame, text="", anchor="nw", font=(None, 9, "bold"), bg="white")
                date_label.pack(anchor="nw")
                tasks_container = tk.Frame(cell_frame, bg="white")
                tasks_container.pack(fill=tk.BOTH, expand=True)
                cell_frame.bind("<Button-1>", lambda event, r=row_index, c=col_index: self._on_calendar_cell_clicked(r, c))
                date_label.bind("<Button-1>", lambda event, r=row_index, c=col_index: self._on_calendar_cell_clicked(r, c))
                row_cells.append({
                    "frame": cell_frame,
                    "date_label": date_label,
                    "tasks_container": tasks_container,
                    "day": None,
                })
            self.calendar_cells.append(row_cells)

        self.no_tasks_label = ttk.Label(calendar_frame, text="No hay tareas disponibles para tu búsqueda.", foreground="gray")
        self.no_tasks_label.pack(fill=tk.X, pady=(8, 0))
        self.no_tasks_label.pack_forget()

        details_frame = ttk.Frame(calendar_frame, padding=(0, 8, 0, 0))
        details_frame.pack(fill=tk.X)
        ttk.Label(details_frame, text="Estadísticas rápidas del calendario:").pack(anchor=tk.W)
        self.calendar_summary_text = tk.Text(details_frame, height=4, state=tk.DISABLED)
        self.calendar_summary_text.pack(fill=tk.BOTH, expand=False)

    def _build_stats_tab(self) -> None:
        stats_frame = ttk.Frame(self.stats_tab, padding=12)
        stats_frame.pack(fill=tk.BOTH, expand=True)

        self.stats_total_label = ttk.Label(stats_frame, text="Tareas totales: 0")
        self.stats_total_label.pack(anchor=tk.W)
        self.stats_pending_label = ttk.Label(stats_frame, text="Tareas pendientes: 0")
        self.stats_pending_label.pack(anchor=tk.W, pady=(4, 0))
        self.stats_completed_label = ttk.Label(stats_frame, text="Tareas completadas: 0")
        self.stats_completed_label.pack(anchor=tk.W, pady=(4, 0))

        stats_lists = ttk.Frame(stats_frame)
        stats_lists.pack(fill=tk.BOTH, expand=True, pady=(12, 0))

        pending_frame = ttk.Frame(stats_lists)
        pending_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        ttk.Label(pending_frame, text="Pendientes").pack(anchor=tk.W)
        self.pending_listbox = tk.Listbox(pending_frame)
        self.pending_listbox.pack(fill=tk.BOTH, expand=True)

        completed_frame = ttk.Frame(stats_lists)
        completed_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(6, 0))
        ttk.Label(completed_frame, text="Completadas").pack(anchor=tk.W)
        self.completed_listbox = tk.Listbox(completed_frame)
        self.completed_listbox.pack(fill=tk.BOTH, expand=True)

    def _build_loading_overlay(self) -> None:
        self.loading_window = None

    def _show_loading_modal(self) -> None:
        if self.loading_window is not None:
            return
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.transient(self.root)
        self.loading_window.grab_set()
        self.loading_window.title("Cargando")
        self.loading_window.geometry("260x100")
        self.loading_window.resizable(False, False)
        self.loading_window.configure(bg="#333333")
        self.loading_window.attributes("-topmost", True)

        tk.Label(
            self.loading_window,
            text="Cargando...",
            fg="white",
            bg="#333333",
            font=(None, 11, "bold"),
        ).pack(pady=(16, 4))
        progress = ttk.Progressbar(self.loading_window, mode="indeterminate")
        progress.pack(fill=tk.X, padx=12, pady=(0, 12))
        progress.start(10)
        self.root.update_idletasks()

    def _hide_loading_modal(self) -> None:
        if self.loading_window is not None:
            self.loading_window.destroy()
            self.loading_window = None

    def _run_with_loading(self, callback) -> None:
        self._show_loading_modal()

        def wrapper() -> None:
            try:
                callback()
            finally:
                self._hide_loading_modal()

        self.root.after(100, wrapper)

    def _get_priority_value(self, raw_value: str) -> int:
        for value, label in self.PRIORITY_OPTIONS.items():
            if label == raw_value:
                return value
        return 2

    def _refresh_task_list(self) -> None:
        self.task_listbox.delete(0, tk.END)
        for task in sorted(self.controller.list_tasks(), key=lambda data: (data.due_date or date.max, data.due_time or time.min, data.priority)):
            due_label = task.due_date.strftime(self.DATE_FORMAT) if task.due_date else "Sin fecha"
            time_label = task.due_time.strftime(self.TIME_FORMAT) if task.due_time else "--:--"
            self.task_listbox.insert(
                tk.END,
                f"{task.id}. {task.title} [{task.category_label}] {due_label} {time_label} - {task.priority_label}",
            )

    def _refresh_calendar_view(self) -> None:
        tasks = self._get_month_tasks()
        self._render_month(tasks)
        self._refresh_calendar_summary(tasks)

    def _refresh_calendar_summary(self, tasks) -> None:
        self.calendar_summary_text.config(state=tk.NORMAL)
        self.calendar_summary_text.delete("1.0", tk.END)
        if tasks:
            self.calendar_summary_text.insert(tk.END, f"Tareas en este mes: {len(tasks)}\n")
            pending = sum(1 for task in tasks if task.status == TaskStatus.PENDING)
            completed = sum(1 for task in tasks if task.status == TaskStatus.COMPLETED)
            self.calendar_summary_text.insert(tk.END, f"Pendientes: {pending}  Completadas: {completed}\n")
        else:
            self.calendar_summary_text.insert(tk.END, "No hay tareas visibles para el mes y filtro actual.\n")
        self.calendar_summary_text.config(state=tk.DISABLED)

    def _refresh_stats(self) -> None:
        stats = self.controller.get_stats()
        self.stats_total_label.config(text=f"Tareas totales: {stats['total']}")
        self.stats_pending_label.config(text=f"Tareas pendientes: {stats['pending']}")
        self.stats_completed_label.config(text=f"Tareas completadas: {stats['completed']}")

        self.pending_listbox.delete(0, tk.END)
        self.completed_listbox.delete(0, tk.END)
        for task in sorted(self.controller.list_tasks(), key=lambda task: (task.due_date or date.max, task.due_time or time.min, task.priority)):
            label = f"{task.title} ({task.due_date.strftime(self.DATE_FORMAT)} {task.due_time.strftime(self.TIME_FORMAT)} - {task.category_label})"
            if task.status == TaskStatus.COMPLETED:
                self.completed_listbox.insert(tk.END, label)
            else:
                self.pending_listbox.insert(tk.END, label)

    def _get_month_tasks(self):
        if self.filtered_tasks is not None:
            month_tasks = [
                task
                for task in self.filtered_tasks
                if task.due_date is not None
                and task.due_date.year == self._current_month.year
                and task.due_date.month == self._current_month.month
            ]
        else:
            month_tasks = self.controller.get_tasks_for_month(
                self._current_month.year,
                self._current_month.month,
            )
        return month_tasks

    def _render_month(self, tasks) -> None:
        self.month_label.config(text=self._current_month.strftime("%B %Y"))
        task_map = {}
        for task in tasks:
            if task.due_date is None:
                continue
            task_map.setdefault(task.due_date.day, []).append(task)

        first_weekday, days_in_month = calendar.monthrange(self._current_month.year, self._current_month.month)
        first_weekday = (first_weekday + 1) % 7

        day_number = 1
        for row in range(6):
            for col in range(7):
                cell = self.calendar_cells[row][col]
                for child in cell["tasks_container"].winfo_children():
                    child.destroy()
                cell["day"] = None
                cell["date_label"].config(text="")
                cell["frame"].configure(bg="white")
                if row == 0 and col < first_weekday:
                    continue
                if day_number > days_in_month:
                    continue
                cell_date = date(self._current_month.year, self._current_month.month, day_number)
                cell["day"] = cell_date
                cell["date_label"].config(text=str(day_number))
                day_tasks = sorted(task_map.get(day_number, []), key=lambda task: (task.due_time or time.min, task.priority))
                for task in day_tasks:
                    label_text = f"{task.due_time.strftime(self.TIME_FORMAT)} {task.title}"
                    task_label = tk.Label(
                        cell["tasks_container"],
                        text=label_text,
                        anchor="w",
                        justify="left",
                        bg=self.PRIORITY_COLORS.get(task.priority, "#2196f3"),
                        fg="white",
                        wraplength=120,
                    )
                    task_label.pack(fill=tk.X, pady=1)
                    def _task_click(event, task_id=task.id):
                        self._on_task_label_clicked(task_id)
                        return "break"
                    task_label.bind("<Button-1>", _task_click)
                day_number += 1

        if tasks:
            self.no_tasks_label.pack_forget()
        else:
            self.no_tasks_label.pack(fill=tk.X, pady=(8, 0))

    def _on_task_selected(self, event: tk.Event) -> None:
        selection = self.task_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        tasks = sorted(self.controller.list_tasks(), key=lambda data: (data.due_date or date.max, data.due_time or time.min, data.priority))
        if index >= len(tasks):
            return
        task = tasks[index]
        self._selected_task_id = task.id
        self._populate_task_detail(task)

    def _on_calendar_cell_clicked(self, row: int, col: int) -> None:
        cell = self.calendar_cells[row][col]
        if not cell["day"]:
            return
        self._selected_date = cell["day"]
        self._open_task_modal(date=cell["day"])

    def _on_task_label_clicked(self, task_id: int) -> None:
        try:
            task = next(task for task in self.controller.list_tasks() if task.id == task_id)
        except StopIteration:
            return
        self._selected_task_id = task.id
        self._populate_task_detail(task)
        self._open_task_modal(task=task)

    def _populate_task_detail(self, task) -> None:
        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert(tk.END, f"Título: {task.title}\n")
        self.detail_text.insert(tk.END, f"Descripción: {task.description.strip()}\n")
        self.detail_text.insert(tk.END, f"Fecha: {task.due_date.strftime(self.DATE_FORMAT) if task.due_date else 'Sin fecha'}\n")
        self.detail_text.insert(tk.END, f"Hora: {task.due_time.strftime(self.TIME_FORMAT) if task.due_time else '--:--'}\n")
        self.detail_text.insert(tk.END, f"Prioridad: {task.priority_label}\n")
        self.detail_text.insert(tk.END, f"Categoría: {task.category_label}\n")
        self.detail_text.insert(tk.END, f"Estado: {task.status.value}\n")
        self.detail_text.config(state=tk.DISABLED)

    def _open_task_modal(self, date: date | None = None, task=None) -> None:
        if task:
            self._open_edit_task_modal(task)
            return
        if date is None:
            return

        modal = tk.Toplevel(self.root)
        modal.title("Crear tarea")
        modal.transient(self.root)
        modal.grab_set()
        modal.geometry("420x430")
        modal.resizable(False, False)

        tk.Label(modal, text=f"Crear tarea: {date.strftime(self.DATE_FORMAT)}", font=(None, 12, "bold")).pack(pady=(12, 8))

        title_var = tk.StringVar()
        time_var = tk.StringVar(value="09:00")
        priority_var = tk.StringVar(value=self.PRIORITY_OPTIONS[2])
        category_var = tk.StringVar(value=self.CATEGORY_OPTIONS[0])

        ttk.Label(modal, text="Título:").pack(anchor=tk.W, padx=12)
        title_entry = ttk.Entry(modal, textvariable=title_var)
        title_entry.pack(fill=tk.X, padx=12, pady=(0, 8))

        ttk.Label(modal, text="Descripción:").pack(anchor=tk.W, padx=12)
        description_text = tk.Text(modal, height=5)
        description_text.pack(fill=tk.BOTH, padx=12, pady=(0, 8))

        ttk.Label(modal, text="Hora (HH:MM):").pack(anchor=tk.W, padx=12)
        ttk.Entry(modal, textvariable=time_var).pack(fill=tk.X, padx=12, pady=(0, 8))

        ttk.Label(modal, text="Prioridad:").pack(anchor=tk.W, padx=12)
        ttk.Combobox(modal, textvariable=priority_var, values=list(self.PRIORITY_OPTIONS.values()), state="readonly").pack(fill=tk.X, padx=12, pady=(0, 8))

        ttk.Label(modal, text="Categoría:").pack(anchor=tk.W, padx=12)
        ttk.Combobox(modal, textvariable=category_var, values=self.CATEGORY_OPTIONS, state="readonly").pack(fill=tk.X, padx=12, pady=(0, 8))

        button_frame = ttk.Frame(modal)
        button_frame.pack(fill=tk.X, padx=12, pady=12)
        ttk.Button(button_frame, text="Guardar", command=lambda: self._create_task_from_modal(modal, date, title_var, description_text, time_var, priority_var, category_var)).pack(side=tk.LEFT, padx=4)
        ttk.Button(button_frame, text="Cancelar", command=modal.destroy).pack(side=tk.RIGHT, padx=4)

    def _open_edit_task_modal(self, task) -> None:
        modal = tk.Toplevel(self.root)
        modal.title("Editar tarea")
        modal.transient(self.root)
        modal.grab_set()
        modal.geometry("420x430")
        modal.resizable(False, False)

        title_var = tk.StringVar(value=task.title)
        time_var = tk.StringVar(value=task.due_time.strftime(self.TIME_FORMAT) if task.due_time else "09:00")
        priority_var = tk.StringVar(value=task.priority_label)
        category_var = tk.StringVar(value=task.category_label)

        ttk.Label(modal, text="Título:").pack(anchor=tk.W, padx=12)
        title_entry = ttk.Entry(modal, textvariable=title_var)
        title_entry.pack(fill=tk.X, padx=12, pady=(0, 8))

        ttk.Label(modal, text="Descripción:").pack(anchor=tk.W, padx=12)
        description_text = tk.Text(modal, height=5)
        description_text.insert(tk.END, task.description)
        description_text.pack(fill=tk.BOTH, padx=12, pady=(0, 8))

        ttk.Label(modal, text="Hora (HH:MM):").pack(anchor=tk.W, padx=12)
        ttk.Entry(modal, textvariable=time_var).pack(fill=tk.X, padx=12, pady=(0, 8))

        ttk.Label(modal, text="Prioridad:").pack(anchor=tk.W, padx=12)
        ttk.Combobox(modal, textvariable=priority_var, values=list(self.PRIORITY_OPTIONS.values()), state="readonly").pack(fill=tk.X, padx=12, pady=(0, 8))

        ttk.Label(modal, text="Categoría:").pack(anchor=tk.W, padx=12)
        ttk.Combobox(modal, textvariable=category_var, values=self.CATEGORY_OPTIONS, state="readonly").pack(fill=tk.X, padx=12, pady=(0, 8))

        button_frame = ttk.Frame(modal)
        button_frame.pack(fill=tk.X, padx=12, pady=12)
        ttk.Button(button_frame, text="Actualizar", command=lambda: self._update_task_from_modal(modal, task.id, task.due_date, title_var, description_text, time_var, priority_var, category_var)).pack(side=tk.LEFT, padx=4)
        ttk.Button(button_frame, text="Eliminar", command=lambda: self._confirm_delete_task(modal)).pack(side=tk.LEFT, padx=4)
        ttk.Button(button_frame, text="Cerrar", command=modal.destroy).pack(side=tk.RIGHT, padx=4)

    def _create_task_from_modal(self, modal, due_date, title_var, description_text, time_var, priority_var, category_var) -> None:
        try:
            task = self.controller.add_task(
                title=title_var.get(),
                description=description_text.get("1.0", tk.END),
                due_date=due_date,
                due_time=self._parse_time(time_var.get()),
                priority=self._get_priority_value(priority_var.get()),
                category=category_var.get(),
            )
            self._selected_task_id = task.id
            self._refresh_task_list()
            self._refresh_calendar_view()
            self._refresh_stats()
            messagebox.showinfo("Tarea creada", "La tarea se creó correctamente")
            modal.destroy()
        except ValueError as error:
            messagebox.showerror("Error al crear tarea", str(error))

    def _update_task_from_modal(self, modal, task_id, due_date, title_var, description_text, time_var, priority_var, category_var) -> None:
        try:
            self.controller.update_task(
                task_id=task_id,
                title=title_var.get(),
                description=description_text.get("1.0", tk.END),
                due_date=due_date,
                due_time=self._parse_time(time_var.get()),
                priority=self._get_priority_value(priority_var.get()),
                category=category_var.get(),
            )
            self._refresh_task_list()
            self._refresh_calendar_view()
            self._refresh_stats()
            messagebox.showinfo("Tarea actualizada", "La tarea se actualizó correctamente")
            modal.destroy()
        except ValueError as error:
            messagebox.showerror("Error al actualizar tarea", str(error))

    def _confirm_delete_task(self, modal: tk.Toplevel) -> None:
        confirm = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar la tarea?")
        if not confirm:
            return
        try:
            self.controller.delete_task(self._selected_task_id)
            self._selected_task_id = None
            self.detail_text.config(state=tk.NORMAL)
            self.detail_text.delete("1.0", tk.END)
            self.detail_text.config(state=tk.DISABLED)
            self._refresh_task_list()
            self._refresh_calendar_view()
            self._refresh_stats()
            messagebox.showinfo("Tarea eliminada", "Se ha eliminado la tarea correctamente")
            modal.destroy()
        except ValueError as error:
            messagebox.showerror("Error al eliminar tarea", str(error))

    def _delete_task(self) -> None:
        if self._selected_task_id is None:
            messagebox.showwarning("Seleccionar tarea", "Selecciona primero una tarea de la lista")
            return
        try:
            self.controller.delete_task(self._selected_task_id)
            self._selected_task_id = None
            self.detail_text.config(state=tk.NORMAL)
            self.detail_text.delete("1.0", tk.END)
            self.detail_text.config(state=tk.DISABLED)
            self._refresh_task_list()
            self._refresh_calendar_view()
            self._refresh_stats()
            messagebox.showinfo("Tarea eliminada", "Se ha eliminado la tarea correctamente")
        except ValueError as error:
            messagebox.showerror("Error al eliminar tarea", str(error))

    def _complete_task(self) -> None:
        if self._selected_task_id is None:
            messagebox.showwarning("Seleccionar tarea", "Selecciona primero una tarea de la lista")
            return
        try:
            self.controller.mark_task_completed(self._selected_task_id)
            self._refresh_task_list()
            self._refresh_calendar_view()
            self._refresh_stats()
            messagebox.showinfo("Tarea completada", "La tarea se ha marcado como completada")
        except ValueError as error:
            messagebox.showerror("Error al completar tarea", str(error))

    def _parse_time(self, raw_time: str) -> time | None:
        trimmed = raw_time.strip()
        if not trimmed:
            return None
        try:
            return datetime.strptime(trimmed, self.TIME_FORMAT).time()
        except ValueError:
            raise ValueError("El formato de hora debe ser HH:MM")

    def _apply_filters(self) -> None:
        name = self.filter_name_var.get().strip()
        priority_label = self.filter_priority_var.get().strip()
        category = self.filter_category_var.get().strip()
        priority = self._get_priority_value(priority_label) if priority_label else None
        try:
            self.filtered_tasks = self.controller.search_tasks(name or None, priority, category or None)
            self.filter_message_label.config(text=f"Filtrado: {len(self.filtered_tasks)} tareas encontradas")
            self._refresh_calendar_view()
        except ValueError as error:
            self.filter_message_label.config(text=str(error))

    def _prev_month(self) -> None:
        year = self._current_month.year
        month = self._current_month.month - 1
        if month < 1:
            month = 12
            year -= 1
        self._current_month = self._current_month.replace(year=year, month=month, day=1)
        self._refresh_calendar_view()

    def _next_month(self) -> None:
        year = self._current_month.year
        month = self._current_month.month + 1
        if month > 12:
            month = 1
            year += 1
        self._current_month = self._current_month.replace(year=year, month=month, day=1)
        self._refresh_calendar_view()
