import math
import tkinter as tk


class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class GraphEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Editor")

        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack()

        self.add_mode_btn = tk.Button(root, text="Add Mode", command=self.enable_add_mode)
        self.add_mode_btn.pack(side=tk.LEFT)

        self.connect_mode_btn = tk.Button(root, text="Connect Mode", command=self.enable_connect_mode)
        self.connect_mode_btn.pack(side=tk.LEFT)

        self.mode = None
        self.vertices = []
        self.active_vertex = None
        self.line = None

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        self.rotation_slider = tk.Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, label="Y-axis Rotation",
                                        command=self.on_slider_change)
        self.rotation_slider.pack()

        self.rotation_angle = 0

    def enable_add_mode(self):
        self.mode = "add"

    def enable_connect_mode(self):
        self.mode = "connect"

    def on_canvas_click(self, event):
        x, y = event.x, event.y

        if self.mode == "add":
            vertex = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')
            self.vertices.append(Vertex(x, y, 0))

        elif self.mode == "connect":
            self.active_vertex = Vertex(x, y, 0)
            self.line = self.canvas.create_line(x, y, x, y)

    def on_canvas_drag(self, event):
        if self.mode == "connect" and self.line:
            x, y = event.x, event.y
            self.canvas.coords(self.line, self.active_vertex.x, self.active_vertex.y, x, y)

    def on_canvas_release(self, event):
        if self.mode == "connect" and self.line:
            x, y = event.x, event.y
            self.canvas.delete(self.line)
            self.line = None

            # Check if there's a vertex at the release point
            target_vertex = None
            for vertex in self.vertices:
                if abs(vertex.x - x) <= 5 and abs(vertex.y - y) <= 5:
                    target_vertex = vertex
                    break

            if target_vertex:
                self.canvas.create_line(self.active_vertex.x, self.active_vertex.y, target_vertex.x, target_vertex.y)
                # Implement your logic here to handle connections between vertices

            self.active_vertex = None

    def on_slider_change(self, value):
        # Update the rotation angle
        self.rotation_angle = int(value)
        # Redraw the canvas with the new rotation angle
        self.redraw_canvas()

    def redraw_canvas(self):
        self.canvas.delete("all")
        for vertex in self.vertices:
            # Apply 3D rotation using rotation matrix
            x = vertex.x
            y = vertex.y * math.cos(math.radians(self.rotation_angle)) - vertex.z * math.sin(math.radians(self.rotation_angle))
            z = vertex.y * math.sin(math.radians(self.rotation_angle)) + vertex.z * math.cos(math.radians(self.rotation_angle))
            vertex_display = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')
            vertex.display = vertex_display
        for i, vertex in enumerate(self.vertices):
            for j in range(i+1, len(self.vertices)):
                self.canvas.create_line(vertex.x, vertex.y, self.vertices[j].x, self.vertices[j].y)

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphEditorApp(root)
    root.mainloop()
