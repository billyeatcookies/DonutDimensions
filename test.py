import tkinter as tk
import math

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

        self.mode = None
        self.vertices = []
        self.connections = []
        self.active_vertex = None
        self.line = None

        self.canvas.bind("<Button-1>", self.on_canvas_left_click)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        self.rotation_x_slider = tk.Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, label="X-axis Rotation",
                                          command=self.on_x_slider_change)
        self.rotation_x_slider.pack()

        self.rotation_y_slider = tk.Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, label="Y-axis Rotation",
                                          command=self.on_y_slider_change)
        self.rotation_y_slider.pack()

        self.rotation_z_slider = tk.Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, label="Z-axis Rotation",
                                          command=self.on_z_slider_change)
        self.rotation_z_slider.pack()

        self.rotation_x_angle = 0
        self.rotation_y_angle = 0
        self.rotation_z_angle = 0

    def on_canvas_left_click(self, event):
        x, y = event.x, event.y
        for vertex in self.vertices:
            if abs(vertex.x - x) <= 5 and abs(vertex.y - y) <= 5:
                self.active_vertex = vertex
                self.line = self.canvas.create_line(x, y, x, y)
                break

    def on_canvas_right_click(self, event):
        x, y = event.x, event.y

        vertex = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')
        self.vertices.append(Vertex(x, y, 0))

    def on_canvas_drag(self, event):
        if self.line:
            x, y = event.x, event.y
            self.canvas.coords(self.line, self.active_vertex.x, self.active_vertex.y, x, y)

    def on_canvas_release(self, event):
        if self.line:
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
                self.connections.append((self.active_vertex, target_vertex))

            self.active_vertex = None

    def on_x_slider_change(self, value):
        self.rotation_x_angle = int(value)
        self.redraw_canvas()

    def on_y_slider_change(self, value):
        self.rotation_y_angle = int(value)
        self.redraw_canvas()

    def on_z_slider_change(self, value):
        self.rotation_z_angle = int(value)
        self.redraw_canvas()

    def redraw_canvas(self):
        self.canvas.delete("all")
        for vertex in self.vertices:
            # Apply 3D rotation using rotation matrices
            x = vertex.x
            y = vertex.y * math.cos(math.radians(self.rotation_y_angle)) - vertex.z * math.sin(math.radians(self.rotation_y_angle))
            z = vertex.y * math.sin(math.radians(self.rotation_y_angle)) + vertex.z * math.cos(math.radians(self.rotation_y_angle))
            y = vertex.y * math.cos(math.radians(self.rotation_x_angle)) - z * math.sin(math.radians(self.rotation_x_angle))
            z = vertex.y * math.sin(math.radians(self.rotation_x_angle)) + z * math.cos(math.radians(self.rotation_x_angle))
            x = x * math.cos(math.radians(self.rotation_z_angle)) - y * math.sin(math.radians(self.rotation_z_angle))
            y = x * math.sin(math.radians(self.rotation_z_angle)) + y * math.cos(math.radians(self.rotation_z_angle))
            vertex_display = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')
            vertex.display = vertex_display
            # Display the z-coordinate as text near the vertex
            self.canvas.create_text(x + 10, y - 10, text=f"({vertex.x}, {vertex.y}, {vertex.z})")

        # Draw connections with 3D rotations
        for vertex1, vertex2 in self.connections:
            x1 = vertex1.x
            y1 = vertex1.y * math.cos(math.radians(self.rotation_y_angle)) - vertex1.z * math.sin(math.radians(self.rotation_y_angle))
            z1 = vertex1.y * math.sin(math.radians(self.rotation_y_angle)) + vertex1.z * math.cos(math.radians(self.rotation_y_angle))
            y1 = vertex1.y * math.cos(math.radians(self.rotation_x_angle)) - z1 * math.sin(math.radians(self.rotation_x_angle))
            z1 = vertex1.y * math.sin(math.radians(self.rotation_x_angle)) + z1 * math.cos(math.radians(self.rotation_x_angle))
            x1 = x1 * math.cos(math.radians(self.rotation_z_angle)) - y1 * math.sin(math.radians(self.rotation_z_angle))
            y1 = x1 * math.sin(math.radians(self.rotation_z_angle)) + y1 * math.cos(math.radians(self.rotation_z_angle))

            x2 = vertex2.x
            y2 = vertex2.y * math.cos(math.radians(self.rotation_y_angle)) - vertex2.z * math.sin(math.radians(self.rotation_y_angle))
            z2 = vertex2.y * math.sin(math.radians(self.rotation_y_angle)) + vertex2.z * math.cos(math.radians(self.rotation_y_angle))
            y2 = vertex2.y * math.cos(math.radians(self.rotation_x_angle)) - z2 * math.sin(math.radians(self.rotation_x_angle))
            z2 = vertex2.y * math.sin(math.radians(self.rotation_x_angle)) + z2 * math.cos(math.radians(self.rotation_x_angle))
            x2 = x2 * math.cos(math.radians(self.rotation_z_angle)) - y2 * math.sin(math.radians(self.rotation_z_angle))
            y2 = x2 * math.sin(math.radians(self.rotation_z_angle)) + y2 * math.cos(math.radians(self.rotation_z_angle))

            self.canvas.create_line(x1, y1, x2, y2)

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphEditorApp(root)
    root.mainloop()
