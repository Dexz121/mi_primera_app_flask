#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To-Do (Tkinter) — cumple: componentes, widgets, grid responsive, eventos, buenas prácticas.
Requisito en Linux/WSL: sudo apt install -y python3-tk
"""

import json, sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


# ------------------------- Modelo ------------------------- #
class TaskModel:
    """Gestiona lista y persistencia en JSON."""
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.tasks = []   # {"id": int, "text": str, "done": bool}
        self._next_id = 1
        self.load()

    def load(self):
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self.tasks = data.get("tasks", [])
                if self.tasks:
                    self._next_id = max(t["id"] for t in self.tasks) + 1
            except Exception:
                self.tasks, self._next_id = [], 1

    def save(self):
        self.storage_path.write_text(
            json.dumps({"tasks": self.tasks}, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def add_task(self, text: str):
        text = text.strip()
        if not text:
            return None
        task = {"id": self._next_id, "text": text, "done": False}
        self._next_id += 1
        self.tasks.append(task)
        self.save()
        return task

    def delete_task(self, task_id: int):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.save()

    def toggle_task(self, task_id: int):
        for t in self.tasks:
            if t["id"] == task_id:
                t["done"] = not t["done"]
                break
        self.save()

    def update_text(self, task_id: int, new_text: str):
        new_text = new_text.strip()
        for t in self.tasks:
            if t["id"] == task_id and new_text:
                t["text"] = new_text
                break
        self.save()

    def clear_completed(self):
        self.tasks = [t for t in self.tasks if not t["done"]]
        self.save()

    def get_filtered(self, key: str):
        if key == "Activas":
            return [t for t in self.tasks if not t["done"]]
        if key == "Completadas":
            return [t for t in self.tasks if t["done"]]
        return list(self.tasks)


# ------------------------- Vista ------------------------- #
class TaskView(ttk.Frame):
    """UI con ttk y grid; expone callbacks que inyecta el controlador."""
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.master.title("Lista de Tareas — Tkinter")
        self.master.geometry("720x480")
        self.master.minsize(560, 360)

        # Estilo
        self.style = ttk.Style()
        try: self.style.theme_use("clam")
        except Exception: pass
        self.style.configure("TButton", padding=6)
        self.style.configure("TEntry", padding=4)

        # Menú
        self._build_menubar()

        # Entrada + botones
        self.input_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.input_var)
        self.btn_add = ttk.Button(self, text="Agregar (Enter)")
        self.btn_toggle = ttk.Button(self, text="Marcar/Desmarcar")
        self.btn_delete = ttk.Button(self, text="Eliminar (Supr)")
        self.btn_clear_done = ttk.Button(self, text="Eliminar Completadas")

        # Filtro
        self.filter_var = tk.StringVar(value="Todas")
        self.filter_label = ttk.Label(self, text="Filtro:")
        self.filter_combo = ttk.Combobox(
            self, textvariable=self.filter_var,
            values=["Todas", "Activas", "Completadas"], state="readonly"
        )

        # Lista (Treeview)
        self.tree = ttk.Treeview(self, columns=("task","status","task_id"), show="headings", selectmode="browse")
        self.tree.heading("task", text="Tarea")
        self.tree.heading("status", text="Estado")
        self.tree.heading("task_id", text="ID")
        self.tree.column("task", width=420, anchor="w")
        self.tree.column("status", width=120, anchor="center")
        self.tree.column("task_id", width=0, stretch=False)
        self.scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll_y.set)

        # Status bar
        self.status_var = tk.StringVar(value="0 tareas")
        self.status = ttk.Label(self, textvariable=self.status_var, anchor="w", relief="sunken")

        # Layout
        self._layout()

        # Atajos y eventos
        self.master.bind("<Return>", lambda e: self.on_add and self.on_add())
        self.master.bind("<Delete>", lambda e: self.on_delete and self.on_delete())
        self.master.bind("<Control-n>", lambda e: (self.entry.focus_set(), self.input_var.set("")))
        self.tree.bind("<Double-1>", lambda e: self.on_edit and self.on_edit())
        self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self.on_filter and self.on_filter())

        # Callbacks (inyectadas)
        self.on_add = self.on_toggle = self.on_delete = self.on_clear_done = None
        self.on_filter = self.on_edit = self.on_about = None

        # Asociar botones
        self.btn_add.configure(command=lambda: self.on_add and self.on_add())
        self.btn_toggle.configure(command=lambda: self.on_toggle and self.on_toggle())
        self.btn_delete.configure(command=lambda: self.on_delete and self.on_delete())
        self.btn_clear_done.configure(command=lambda: self.on_clear_done and self.on_clear_done())

    def _build_menubar(self):
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Nueva (Ctrl+N)", command=lambda: self.entry.focus_set())
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.master.quit)
        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="Acerca de", command=lambda: self.on_about and self.on_about())
        menubar.add_cascade(label="Archivo", menu=file_menu)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        self.master.config(menu=menubar)

    def _layout(self):
        self.grid(row=0, column=0, sticky="nsew")
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        self.entry.grid(row=0, column=0, sticky="ew", padx=(0,8))
        btns = ttk.Frame(self); btns.grid(row=0, column=1, sticky="ew")
        for i in range(2): btns.columnconfigure(i, weight=1)
        self.btn_add.grid(in_=btns, row=0, column=0, padx=(0,6), pady=2, sticky="ew")
        self.btn_toggle.grid(in_=btns, row=0, column=1, pady=2, sticky="ew")
        self.btn_delete.grid(in_=btns, row=1, column=0, padx=(0,6), pady=(2,4), sticky="ew")
        self.btn_clear_done.grid(in_=btns, row=1, column=1, pady=(2,4), sticky="ew")

        filt = ttk.Frame(self); filt.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6,4))
        filt.columnconfigure(1, weight=1)
        ttk.Label(filt, text="Filtro:").grid(row=0, column=0, sticky="w")
        self.filter_combo.grid(in_=filt, row=0, column=1, sticky="w", padx=(8,0))

        self.tree.grid(row=3, column=0, sticky="nsew", pady=(4,4))
        self.scroll_y.grid(row=3, column=1, sticky="ns", padx=(6,0))
        self.status.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(6,0))

    # ---- utilidades ---- #
    def get_entry_text(self) -> str:
        return self.input_var.get()

    def clear_entry(self):
        self.input_var.set("")

    def get_selected_task_id(self):
        sel = self.tree.selection()
        if not sel: return None
        vals = self.tree.item(sel[0], "values")
        return int(vals[2]) if len(vals) >= 3 else None

    def populate(self, tasks):
        self.tree.delete(*self.tree.get_children())
        for t in tasks:
            status = "✔ Completada" if t["done"] else "Pendiente"
            self.tree.insert("", "end", iid=str(t["id"]), values=(t["text"], status, t["id"]))
        self.status_var.set(f"{len(tasks)} tareas (filtro: {self.filter_var.get()})")

    def prompt_edit_text(self, current_text: str):
        return simpledialog.askstring("Editar tarea", "Nuevo texto:", initialvalue=current_text, parent=self.master)

    def alert(self, msg: str, title="Info"):
        messagebox.showinfo(title, msg, parent=self.master)

    def confirm(self, msg: str, title="Confirmar") -> bool:
        return messagebox.askyesno(title, msg, parent=self.master)


# --------------------- Controlador --------------------- #
class TaskController:
    def __init__(self, root):
        base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        storage = base_dir / "tasks.json"
        self.model = TaskModel(storage)
        self.view = TaskView(root)

        self.view.on_add = self.add_task
        self.view.on_toggle = self.toggle_task
        self.view.on_delete = self.delete_task
        self.view.on_clear_done = self.clear_completed
        self.view.on_filter = self.apply_filter
        self.view.on_edit = self.edit_task
        self.view.on_about = self.about

        self.apply_filter()

    def current_filter(self):
        return self.view.filter_var.get()

    def apply_filter(self):
        self.view.populate(self.model.get_filtered(self.current_filter()))

    def add_task(self):
        text = self.view.get_entry_text()
        if self.model.add_task(text):
            self.view.clear_entry()
            self.apply_filter()
        else:
            self.view.alert("Escribe una tarea.", "Aviso")

    def toggle_task(self):
        task_id = self.view.get_selected_task_id()
        if task_id is None:
            self.view.alert("Selecciona una tarea.", "Aviso"); return
        self.model.toggle_task(task_id); self.apply_filter()

    def delete_task(self):
        task_id = self.view.get_selected_task_id()
        if task_id is None:
            self.view.alert("Selecciona una tarea.", "Aviso"); return
        if self.view.confirm("¿Eliminar la tarea seleccionada?"):
            self.model.delete_task(task_id); self.apply_filter()

    def clear_completed(self):
        if self.view.confirm("¿Eliminar TODAS las tareas completadas?"):
            self.model.clear_completed(); self.apply_filter()

    def edit_task(self):
        task_id = self.view.get_selected_task_id()
        if task_id is None: return
        curr = next((t["text"] for t in self.model.tasks if t["id"] == task_id), "")
        new_text = self.view.prompt_edit_text(curr)
        if new_text is not None:
            self.model.update_text(task_id, new_text); self.apply_filter()

    def about(self):
        self.view.alert(
            "To-Do (Tkinter)\n\n"
            "Enter: Agregar\nDoble clic: Editar\nSupr: Eliminar\nCtrl+N: Nueva tarea\n\n"
            "Filtro: Todas / Activas / Completadas",
            "Acerca de"
        )


def main():
    root = tk.Tk()
    TaskController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
