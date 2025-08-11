"""Tkinter-based GUI for managing manuscript entries stored in a JSON file.

The GUI wraps :class:`manuscripts.ManuscriptDB` and exposes buttons to add,
edit, delete and filter entries. The "Fields" button lists all unique models,
datasets and metrics stored across entries. "Prompt" shows the JSON prompt to
ask ChatGPT for structured manuscript information.

The methods, datasets and metrics fields are expected to be JSON arrays that can
be pasted directly from a ChatGPT response following the provided prompt.
"""

from __future__ import annotations

import json
import tkinter as tk
from tkinter import messagebox, scrolledtext
from typing import Any, Dict, Optional

from manuscripts import ManuscriptDB, generate_prompt


class ManuscriptApp(tk.Tk):
    """Simple graphical interface for :class:`ManuscriptDB`."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Manuscript Manager")
        self.geometry("700x400")
        self.db = ManuscriptDB()
        self._create_widgets()
        self._refresh_list()

    # ------------------------------------------------------------------
    # GUI construction helpers
    def _create_widgets(self) -> None:
        self.listbox = tk.Listbox(self, width=80)
        self.listbox.grid(row=0, column=0, columnspan=6, sticky="nsew", padx=5, pady=5)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        btn_add = tk.Button(self, text="Add", command=self._add_entry)
        btn_edit = tk.Button(self, text="Edit", command=self._edit_entry)
        btn_delete = tk.Button(self, text="Delete", command=self._delete_entry)
        btn_filter = tk.Button(self, text="Filter", command=self._filter_entries)
        btn_fields = tk.Button(self, text="Fields", command=self._show_fields)
        btn_prompt = tk.Button(self, text="Prompt", command=self._show_prompt)

        for i, btn in enumerate([btn_add, btn_edit, btn_delete, btn_filter, btn_fields, btn_prompt]):
            btn.grid(row=1, column=i, sticky="ew", padx=2, pady=2)

    # ------------------------------------------------------------------
    # Utility methods
    def _refresh_list(self, entries: Optional[list[Dict[str, Any]]] = None) -> None:
        self.listbox.delete(0, tk.END)
        data = entries if entries is not None else self.db.list()
        for entry in data:
            self.listbox.insert(tk.END, entry.get("title", "<no title>"))

    def _selected_index(self) -> Optional[int]:
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Select", "Please select an entry first")
            return None
        return int(sel[0])

    # ------------------------------------------------------------------
    # CRUD operations
    def _add_entry(self) -> None:
        data = self._entry_dialog()
        if data:
            self.db.add(data)
            self._refresh_list()

    def _edit_entry(self) -> None:
        index = self._selected_index()
        if index is None:
            return
        current = self.db.list()[index]
        updates = self._entry_dialog(current)
        if updates:
            self.db.edit(index, updates)
            self._refresh_list()

    def _delete_entry(self) -> None:
        index = self._selected_index()
        if index is None:
            return
        if messagebox.askyesno("Confirm", "Delete selected entry?"):
            self.db.delete(index)
            self._refresh_list()

    # ------------------------------------------------------------------
    # Dialog helpers
    def _entry_dialog(self, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        top = tk.Toplevel(self)
        top.title("Entry")

        # Title
        tk.Label(top, text="Title").grid(row=0, column=0, sticky="e")
        e_title = tk.Entry(top, width=60)
        e_title.grid(row=0, column=1, pady=2)

        # Authors
        tk.Label(top, text="Authors (comma separated)").grid(row=1, column=0, sticky="e")
        e_auth = tk.Entry(top, width=60)
        e_auth.grid(row=1, column=1, pady=2)

        # Affiliations
        tk.Label(top, text="Affiliations (comma separated)").grid(row=2, column=0, sticky="e")
        e_aff = tk.Entry(top, width=60)
        e_aff.grid(row=2, column=1, pady=2)

        # Abstract
        tk.Label(top, text="Abstract").grid(row=3, column=0, sticky="ne")
        t_abs = scrolledtext.ScrolledText(top, width=60, height=4)
        t_abs.grid(row=3, column=1, pady=2)

        # Methods
        tk.Label(top, text="Methods JSON").grid(row=4, column=0, sticky="ne")
        t_methods = scrolledtext.ScrolledText(top, width=60, height=4)
        t_methods.grid(row=4, column=1, pady=2)

        # Datasets
        tk.Label(top, text="Datasets JSON").grid(row=5, column=0, sticky="ne")
        t_datasets = scrolledtext.ScrolledText(top, width=60, height=4)
        t_datasets.grid(row=5, column=1, pady=2)

        # Metrics
        tk.Label(top, text="Metrics JSON").grid(row=6, column=0, sticky="ne")
        t_metrics = scrolledtext.ScrolledText(top, width=60, height=4)
        t_metrics.grid(row=6, column=1, pady=2)

        # Populate with existing data if provided
        if data:
            e_title.insert(0, data.get("title", ""))
            e_auth.insert(0, ",".join(data.get("authors", [])))
            e_aff.insert(0, ",".join(data.get("affiliations", [])))
            t_abs.insert("1.0", data.get("abstract", ""))
            t_methods.insert("1.0", json.dumps(data.get("methods", []), ensure_ascii=False, indent=2))
            t_datasets.insert("1.0", json.dumps(data.get("datasets", []), ensure_ascii=False, indent=2))
            t_metrics.insert("1.0", json.dumps(data.get("metrics", []), ensure_ascii=False, indent=2))

        result: Dict[str, Any] = {}

        def on_ok() -> None:
            try:
                result.update({
                    "title": e_title.get().strip(),
                    "authors": [a.strip() for a in e_auth.get().split(",") if a.strip()],
                    "affiliations": [a.strip() for a in e_aff.get().split(",") if a.strip()],
                    "abstract": t_abs.get("1.0", tk.END).strip(),
                    "methods": json.loads(t_methods.get("1.0", tk.END).strip() or "[]"),
                    "datasets": json.loads(t_datasets.get("1.0", tk.END).strip() or "[]"),
                    "metrics": json.loads(t_metrics.get("1.0", tk.END).strip() or "[]"),
                })
            except json.JSONDecodeError as exc:  # pragma: no cover - GUI input
                messagebox.showerror("Invalid JSON", str(exc))
                return
            top.destroy()

        def on_cancel() -> None:
            top.destroy()

        btn_frame = tk.Frame(top)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=5)
        tk.Button(btn_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)

        top.transient(self)
        top.grab_set()
        self.wait_window(top)

        return result if result else None

    # ------------------------------------------------------------------
    def _filter_entries(self) -> None:
        data = self._filter_dialog()
        if data is None:
            return
        results = self.db.filter(**data)
        self._show_json_window("Filtered Entries", results)

    def _filter_dialog(self) -> Optional[Dict[str, Optional[str]]]:
        top = tk.Toplevel(self)
        top.title("Filter")

        tk.Label(top, text="Model").grid(row=0, column=0, sticky="e")
        e_model = tk.Entry(top)
        e_model.grid(row=0, column=1, pady=2)

        tk.Label(top, text="Dataset").grid(row=1, column=0, sticky="e")
        e_dataset = tk.Entry(top)
        e_dataset.grid(row=1, column=1, pady=2)

        tk.Label(top, text="Metric").grid(row=2, column=0, sticky="e")
        e_metric = tk.Entry(top)
        e_metric.grid(row=2, column=1, pady=2)

        result: Dict[str, Optional[str]] = {}

        def on_ok() -> None:
            result.update({
                "model": e_model.get().strip() or None,
                "dataset": e_dataset.get().strip() or None,
                "metric": e_metric.get().strip() or None,
            })
            top.destroy()

        def on_cancel() -> None:
            top.destroy()

        btn_frame = tk.Frame(top)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(btn_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)

        top.transient(self)
        top.grab_set()
        self.wait_window(top)

        return result if result else None

    # ------------------------------------------------------------------
    def _show_fields(self) -> None:
        fields = self.db.list_fields()
        self._show_json_window("Fields", fields)

    def _show_prompt(self) -> None:
        prompt = json.loads(generate_prompt())
        self._show_json_window("Prompt", prompt)

    def _show_json_window(self, title: str, data: Any) -> None:
        top = tk.Toplevel(self)
        top.title(title)
        txt = scrolledtext.ScrolledText(top, width=80, height=20)
        txt.pack(fill=tk.BOTH, expand=True)
        txt.insert("1.0", json.dumps(data, indent=2, ensure_ascii=False))
        txt.config(state=tk.DISABLED)
        top.transient(self)
        top.grab_set()


def main() -> None:  # pragma: no cover - GUI launch
    app = ManuscriptApp()
    app.mainloop()


if __name__ == "__main__":  # pragma: no cover - GUI launch
    main()

