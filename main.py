import tkinter as tk

from database.database import Database
from controllers.main_controller import MainController
from views.main_view import MainView


def main():

    database = Database()

    controller = MainController(
        database
    )

    root = tk.Tk()

    MainView(
        root,
        controller
    )

    root.mainloop()


if __name__ == "__main__":
    main()