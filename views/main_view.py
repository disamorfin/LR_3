import tkinter as tk

from tkinter import ttk
from tkinter import messagebox


class MainView:

    def __init__(
        self,
        root,
        controller
    ):

        self.root = root
        self.controller = controller

        self.root.title(
            "Центр мониторинга космического мусора"
        )

        self.root.geometry(
            "1400x800"
        )

        self.create_widgets()

        self.load_objects()

    def create_widgets(self):

        # ==========================
        # ЗАГОЛОВОК
        # ==========================

        title = tk.Label(
            self.root,
            text="Центр мониторинга космического мусора",
            font=("Arial", 18)
        )

        title.pack(
            pady=10
        )

        # ==========================
        # ФОРМА ДОБАВЛЕНИЯ
        # ==========================

        form = tk.LabelFrame(
            self.root,
            text="Добавление космического объекта",
            padx=10,
            pady=10
        )

        form.pack(
            pady=10
        )

        # Каталожный номер

        tk.Label(
            form,
            text="Каталожный номер"
        ).grid(
            row=0,
            column=0
        )

        self.catalog_entry = tk.Entry(
            form
        )

        self.catalog_entry.grid(
            row=0,
            column=1
        )

        # Международный ID

        tk.Label(
            form,
            text="Международный ID"
        ).grid(
            row=1,
            column=0
        )

        self.international_entry = tk.Entry(
            form
        )

        self.international_entry.grid(
            row=1,
            column=1
        )

        # Тип

        tk.Label(
            form,
            text="Тип"
        ).grid(
            row=2,
            column=0
        )

        self.type_entry = tk.Entry(
            form
        )

        self.type_entry.grid(
            row=2,
            column=1
        )

        # Размер

        tk.Label(
            form,
            text="Размер"
        ).grid(
            row=3,
            column=0
        )

        self.size_entry = tk.Entry(
            form
        )

        self.size_entry.grid(
            row=3,
            column=1
        )

        # ==========================
        # КООРДИНАТЫ
        # ==========================

        tk.Label(
            form,
            text="X (км)"
        ).grid(
            row=0,
            column=2
        )

        self.x_entry = tk.Entry(
            form
        )

        self.x_entry.grid(
            row=0,
            column=3
        )

        tk.Label(
            form,
            text="Y (км)"
        ).grid(
            row=1,
            column=2
        )

        self.y_entry = tk.Entry(
            form
        )

        self.y_entry.grid(
            row=1,
            column=3
        )

        tk.Label(
            form,
            text="Z (км)"
        ).grid(
            row=2,
            column=2
        )

        self.z_entry = tk.Entry(
            form
        )

        self.z_entry.grid(
            row=2,
            column=3
        )

        # ==========================
        # СКОРОСТЬ
        # ==========================

        tk.Label(
            form,
            text="VX (км/с)"
        ).grid(
            row=0,
            column=4
        )

        self.vx_entry = tk.Entry(
            form
        )

        self.vx_entry.grid(
            row=0,
            column=5
        )

        tk.Label(
            form,
            text="VY (км/с)"
        ).grid(
            row=1,
            column=4
        )

        self.vy_entry = tk.Entry(
            form
        )

        self.vy_entry.grid(
            row=1,
            column=5
        )

        tk.Label(
            form,
            text="VZ (км/с)"
        ).grid(
            row=2,
            column=4
        )

        self.vz_entry = tk.Entry(
            form
        )

        self.vz_entry.grid(
            row=2,
            column=5
        )

        # ==========================
        # КНОПКА ДОБАВЛЕНИЯ
        # ==========================

        add_button = tk.Button(
            form,
            text="Добавить объект",
            command=self.add_object
        )

        add_button.grid(
            row=4,
            column=0,
            columnspan=6,
            pady=10
        )

        # ==========================
        # ТАБЛИЦА ОБЪЕКТОВ
        # ==========================

        columns = (
            "id",
            "catalog",
            "international",
            "type",
            "size",
            "x",
            "y",
            "z",
            "vx",
            "vy",
            "vz",
            "status"
        )

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "catalog": "Каталожный номер",
            "international": "Международный ID",
            "type": "Тип",
            "size": "Размер",
            "x": "X",
            "y": "Y",
            "z": "Z",
            "vx": "VX",
            "vy": "VY",
            "vz": "VZ",
            "status": "Статус"
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=105,
                anchor="center"
            )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # ==========================
        # КНОПКИ
        # ==========================

        button_frame = tk.Frame(
            self.root
        )

        button_frame.pack(
            pady=10
        )

        lost_button = tk.Button(
            button_frame,
            text="Пометить как утерянный",
            command=self.mark_as_lost
        )

        lost_button.pack(
            side="left",
            padx=5
        )

        found_button = tk.Button(
            button_frame,
            text="Восстановить объект",
            command=self.mark_as_found
        )

        found_button.pack(
            side="left",
            padx=5
        )

        delete_button = tk.Button(
            button_frame,
            text="Удалить объект",
            command=self.delete_object
        )

        delete_button.pack(
            side="left",
            padx=5
        )

        conjunction_button = tk.Button(
            button_frame,
            text="Рассчитать сближения",
            command=self.calculate_conjunctions
        )

        conjunction_button.pack(
            side="left",
            padx=5
        )

        report_button = tk.Button(
            button_frame,
            text="Сформировать отчёт",
            command=self.show_report
        )

        report_button.pack(
            side="left",
            padx=5
        )

    # =====================================
    # ДОБАВЛЕНИЕ ОБЪЕКТА
    # =====================================

    def add_object(self):

        try:

            self.controller.add_space_object(
                self.catalog_entry.get(),
                self.international_entry.get(),
                self.type_entry.get(),
                self.size_entry.get(),
                self.x_entry.get(),
                self.y_entry.get(),
                self.z_entry.get(),
                self.vx_entry.get(),
                self.vy_entry.get(),
                self.vz_entry.get()
            )

            self.clear_entries()

            self.load_objects()

            messagebox.showinfo(
                "Успешно",
                "Объект добавлен"
            )

        except Exception as error:

            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    # =====================================
    # ОЧИСТКА ПОЛЕЙ
    # =====================================

    def clear_entries(self):

        entries = [
            self.catalog_entry,
            self.international_entry,
            self.type_entry,
            self.size_entry,
            self.x_entry,
            self.y_entry,
            self.z_entry,
            self.vx_entry,
            self.vy_entry,
            self.vz_entry
        ]

        for entry in entries:

            entry.delete(
                0,
                tk.END
            )

    # =====================================
    # ЗАГРУЗКА ОБЪЕКТОВ
    # =====================================

    def load_objects(self):

        for item in self.tree.get_children():

            self.tree.delete(
                item
            )

        objects = (
            self.controller
            .get_space_objects()
        )

        for obj in objects:

            self.tree.insert(
                "",
                "end",
                values=obj
            )

    # =====================================
    # ПОЛУЧЕНИЕ ID ВЫБРАННОГО ОБЪЕКТА
    # =====================================

    def get_selected_object_id(self):

        selected = (
            self.tree.selection()
        )

        if not selected:

            messagebox.showwarning(
                "Предупреждение",
                "Выберите объект"
            )

            return None

        item = self.tree.item(
            selected[0]
        )

        return item["values"][0]

    # =====================================
    # ПОМЕТКА КАК УТЕРЯННОГО
    # =====================================

    def mark_as_lost(self):

        object_id = (
            self.get_selected_object_id()
        )

        if object_id is None:
            return

        try:

            self.controller.mark_object_as_lost(
                object_id
            )

            self.load_objects()

        except Exception as error:

            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    # =====================================
    # ВОССТАНОВЛЕНИЕ ОБЪЕКТА
    # =====================================

    def mark_as_found(self):

        object_id = (
            self.get_selected_object_id()
        )

        if object_id is None:
            return

        try:

            self.controller.mark_object_as_found(
                object_id
            )

            self.load_objects()

        except Exception as error:

            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    # =====================================
    # УДАЛЕНИЕ ОБЪЕКТА
    # =====================================

    def delete_object(self):

        object_id = (
            self.get_selected_object_id()
        )

        if object_id is None:
            return

        answer = messagebox.askyesno(
            "Удаление объекта",
            "Вы уверены, что хотите удалить выбранный объект?"
        )

        if not answer:
            return

        try:

            self.controller.delete_space_object(
                object_id
            )

            self.load_objects()

            messagebox.showinfo(
                "Удаление",
                "Объект успешно удалён"
            )

        except Exception as error:

            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    # =====================================
    # РАСЧЁТ СБЛИЖЕНИЙ
    # =====================================

    def calculate_conjunctions(self):

        try:

            results = (
                self.controller
                .calculate_conjunctions()
            )

            if not results:

                messagebox.showinfo(
                    "Сближения",
                    "Недостаточно активных объектов для расчёта"
                )

                return

            self.show_conjunction_window(
                results
            )

        except Exception as error:

            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    # =====================================
    # ОКНО РЕЗУЛЬТАТОВ СБЛИЖЕНИЯ
    # =====================================

    def show_conjunction_window(
        self,
        results
    ):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Результаты расчёта сближений"
        )

        window.geometry(
            "900x500"
        )

        columns = (
            "object1",
            "object2",
            "time",
            "distance",
            "probability",
            "status"
        )

        tree = ttk.Treeview(
            window,
            columns=columns,
            show="headings"
        )

        tree.heading(
            "object1",
            text="Объект 1"
        )

        tree.heading(
            "object2",
            text="Объект 2"
        )

        tree.heading(
            "time",
            text="Через секунд"
        )

        tree.heading(
            "distance",
            text="Мин. расстояние"
        )

        tree.heading(
            "probability",
            text="Риск"
        )

        tree.heading(
            "status",
            text="Статус"
        )

        for column in columns:

            tree.column(
                column,
                width=140,
                anchor="center"
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        for result in results:

            probability = (
                result["probability"]
                * 100
            )

            status = (
                "ОПАСНО"
                if result["status"] == "dangerous"
                else "Безопасно"
            )

            tree.insert(
                "",
                "end",
                values=(
                    result["object1"],
                    result["object2"],
                    round(
                        result["time"],
                        2
                    ),
                    round(
                        result["distance"],
                        3
                    ),
                    f"{probability:.2f}%",
                    status
                )
            )

    # =====================================
    # ОТЧЁТ
    # =====================================

    def show_report(self):

        try:

            report = (
                self.controller
                .get_report()
            )

            text = (
                "ОТЧЁТ ЦЕНТРА МОНИТОРИНГА\n\n"
            )

            text += (
                "Количество объектов по типам:\n"
            )

            for object_type, count in report["objects"]:

                text += (
                    f"{object_type}: {count}\n"
                )

            text += (
                "\nКоличество рассчитанных сближений: "
                f"{report['conjunctions']}\n"
            )

            text += (
                "Опасных сближений: "
                f"{report['dangerous']}\n"
            )

            text += (
                "Утерянных объектов: "
                f"{len(report['lost'])}\n"
            )

            messagebox.showinfo(
                "Отчёт",
                text
            )

        except Exception as error:

            messagebox.showerror(
                "Ошибка",
                str(error)
            )