import tkinter as tk


class TopPanel(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, height=40)
        self.app = app
        self._create_widgets()
        self.pack_propagate(False)

    def _create_widgets(self):
        self.config(bg="#f0f0f0")
        self.menus = {
            "Файл": ["Новый", "Открыть", "Сохранить"],
            "Правка": ["Вырезать", "Копировать", "Вставить"]
        }

        for menu_name, items in self.menus.items():
            menu = tk.Menubutton(self, text=menu_name, bg="#f0f0f0")
            menu.pack(side="left", padx=5)

            dropdown = tk.Menu(menu, tearoff=0)
            for item in items:
                dropdown.add_command(label=item)

            menu.config(menu=dropdown)
        self.logout_button = tk.Button(self, text="Выйти", command=self.logout)
        self.logout_button.pack(side="right", padx=5)

    def logout(self):
        self.app.switch_screen("login")