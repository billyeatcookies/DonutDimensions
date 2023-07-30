import tkinter as tk
import math

class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.initial_position = (x, y, z)
        self.current_position = (x, y, z)

class GraphEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Editor")

        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack(expand=True, fill='both')

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

        # Create a new vertex with z-data based on rotation
        vertex = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')
        x, y, z = self.screen_to_world(x, y)
        new_vertex = Vertex(x, y, z)
        new_vertex.display = vertex
        self.vertices.append(new_vertex)

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
            x, y, z = vertex.initial_position
            x, y = self.rotate_point(x, y, self.rotation_z_angle)
            x, z = self.rotate_point(x, z, self.rotation_x_angle)
            y, z = self.rotate_point(y, z, self.rotation_y_angle)
            x = x * math.cos(math.radians(self.rotation_z_angle)) - y * math.sin(math.radians(self.rotation_z_angle))
            y = x * math.sin(math.radians(self.rotation_z_angle)) + y * math.cos(math.radians(self.rotation_z_angle))
            vertex.current_position = (x, y, z)

            # Get canvas coordinates based on the current 3D position
            x, y = self.world_to_screen(x, y, z)
            vertex.display = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')
            # Display the z-coordinate as text near the vertex
            self.canvas.create_text(x + 10, y - 10, text=f"({vertex.x:.2f}, {vertex.y:.2f}, {vertex.z:.2f})")

        # Draw connections with 3D rotations
        for vertex1, vertex2 in self.connections:
            x1, y1, z1 = vertex1.current_position
            x2, y2, z2 = vertex2.current_position
            x1, y1 = self.world_to_screen(x1, y1, z1)
            x2, y2 = self.world_to_screen(x2, y2, z2)
            self.canvas.create_line(x1, y1, x2, y2)

    def screen_to_world(self, x, y):
        # Convert screen coordinates to world coordinates with z-data based on rotation
        x -= self.canvas.winfo_width() / 2
        y -= self.canvas.winfo_height() / 2
        x, y = self.rotate_point(x, y, self.rotation_z_angle)
        x, z = self.rotate_point(x, 0, self.rotation_x_angle)
        y, z = self.rotate_point(y, z, self.rotation_y_angle)

        # Adjust z-coordinate based on y-axis rotation angle
        if self.active_vertex:
            z += self.active_vertex.z

        return x, y, z

    def world_to_screen(self, x, y, z):
        # Convert world coordinates to screen coordinates
        x = x * math.cos(math.radians(self.rotation_z_angle)) + y * math.sin(math.radians(self.rotation_z_angle))
        y = -x * math.sin(math.radians(self.rotation_z_angle)) + y * math.cos(math.radians(self.rotation_z_angle))
        x = x * math.cos(math.radians(self.rotation_y_angle)) - z * math.sin(math.radians(self.rotation_y_angle))
        z = x * math.sin(math.radians(self.rotation_y_angle)) + z * math.cos(math.radians(self.rotation_y_angle))
        x = x * math.cos(math.radians(self.rotation_x_angle)) - z * math.sin(math.radians(self.rotation_x_angle))
        y = y * math.cos(math.radians(self.rotation_x_angle)) + z * math.sin(math.radians(self.rotation_x_angle))

        x += self.canvas.winfo_width() / 2
        y += self.canvas.winfo_height() / 2
        return x, y

    @staticmethod
    def rotate_point(x, y, angle):
        # Rotate point (x, y) by angle degrees around the origin
        angle_rad = math.radians(angle)
        new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
        return new_x, new_y

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphEditorApp(root)
    root.mainloop()
