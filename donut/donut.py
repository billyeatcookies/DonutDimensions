import tkinter as tk
from renderer import Renderer
from editor import Editor
from utils import setdark

class Donut(tk.Tk):
    """Donut class
    """
    def __init__(self, *a, **kw) -> None:
        super().__init__(*a, **kw)
        setdark(self)

        self.renderer = Renderer(self)
        self.editor = Editor(self, self.renderer)

        self.editor.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.renderer.pack(expand=True, fill=tk.BOTH)

    def run(self) -> None:
        self.mainloop()
