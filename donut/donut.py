import tkinter as tk


class Donut(tk.Tk):
    """Donut class
    """
    def __init__(self, m, *a, **kw) -> None:
        super().__init__(m, *a, **kw)

    def run(self) -> None:
        self.mainloop()
