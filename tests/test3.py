import math, random
import numpy as np
import tkinter as tk

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

        self.canvas_2d = tk.Canvas(root, width=500, height=500)
        self.canvas_2d.pack(side=tk.LEFT)

        self.canvas_3d = tk.Canvas(root, width=500, height=500)
        self.canvas_3d.pack(side=tk.LEFT)

        self.verticess = [
            (100, 100, 100),
            (100, 100, -100),
            (100, -100, 100),
            (100, -100, -100),
            (-100, 100, 100),
            (-100, 100, -100),
            (-100, -100, 100),
            (-100, -100, -100)
        ]

        self.edges = [
            (0, 1), (0, 2), (0, 4),
            (1, 3), (1, 5),
            (2, 3), (2, 6),
            (3, 7),
            (4, 5), (4, 6),
            (5, 7),
            (6, 7)
        ]

        self.faces = [
            (0, 2, 6, 4),
            (0, 1, 3, 2),
            (0, 4, 5, 1),
            (1, 5, 7, 3),
            (2, 3, 7, 6),
            (4, 6, 7, 5)
        ]

        self.draw_3d_mesh()

        self.vertices = []
        self.connections = []
        self.active_vertex = None
        self.line = None

        for x, y, z in self.verticess:
            vertex = self.canvas_2d.create_oval(0, 0, 0, 0, fill='black')
            new_vertex = Vertex(x, y, z)
            new_vertex.display = vertex
            self.vertices.append(new_vertex)

        for edge in self.edges:
            self.connections.append((self.vertices[edge[0]], self.vertices[edge[1]]))

        self.canvas_2d.bind("<Button-1>", self.on_canvas_left_click)
        self.canvas_2d.bind("<Button-3>", self.on_canvas_right_click)
        self.canvas_2d.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas_2d.bind("<ButtonRelease-1>", self.on_canvas_release)

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

    def rotate_x(self, theta):
        return [
            [1, 0, 0],
            [0, math.cos(theta), -math.sin(theta)],
            [0, math.sin(theta), math.cos(theta)]
        ]

    def rotate_y(self, theta):
        return [
            [math.cos(theta), 0, math.sin(theta)],
            [0, 1, 0],
            [-math.sin(theta), 0, math.cos(theta)]
        ]

    def rotate_z(self, theta):
        return [
            [math.cos(theta), -math.sin(theta), 0],
            [math.sin(theta), math.cos(theta), 0],
            [0, 0, 1]
        ]

    def perspective_projection(self, vertices, d=500):
        projected_vertices = []
        for vertex in vertices:
            x, y, z = vertex
            if z != 0:
                projected_x = x * d / (z + d)
                projected_y = y * d / (z + d)
                projected_vertices.append((projected_x, projected_y))
            else:
                projected_vertices.append((x, y))
        return projected_vertices

    def draw_3d_mesh(self):
        if not self.verticess:
            return
        
        light_source = [500, -500, 500]
        light_vector = np.array(light_source)
        distances = [(sum([np.dot(self.verticess[face[i]], light_vector) for i in range(len(face))])/3, face) for face in self.faces]
        distances.sort(reverse=True)

        for _, face in distances:
            v1 = np.array(self.verticess[face[0]])
            v2 = np.array(self.verticess[face[1]])
            v3 = np.array(self.verticess[face[2]])
            normal = np.cross(v2 - v1, v3 - v1)

            to_light = np.array(light_source) - v1
            cos_theta = np.dot(normal, to_light) / (np.linalg.norm(normal) * np.linalg.norm(to_light))

            shade = int(255 * (cos_theta + 1) / 2)
            color = '#{:02x}{:02x}{:02x}'.format(shade, shade, shade)

            coords = self.perspective_projection([self.verticess[i] for i in face if isinstance(i, int)])
            self.canvas_3d.create_polygon(coords, fill=color)

        for edge in self.edges:
            x1, y1, z1 = self.verticess[edge[0]]
            x2, y2, z2 = self.verticess[edge[1]]
            coords = self.perspective_projection([(x1, y1, z1), (x2, y2, z2)])
            x1, y1 = coords[0]
            x2, y2 = coords[1]
            self.canvas_3d.create_line(x1 + 250, y1 + 250, x2 + 250, y2 + 250)

        for vertex in self.verticess:
            x, y, z = vertex
            coords = self.perspective_projection([(x, y, z)])
            x, y = coords[0]
            r = 5
            self.canvas_3d.create_oval(x - r + 250, y - r + 250, x + r + 250, y + r + 250, fill='white')

        self.root.after(10, self.animate)

    def animate(self):
        rotation_matrix = np.dot(self.rotate_x(0.01), np.dot(self.rotate_y(0.02), self.rotate_z(0.03)))
        self.verticess = [np.dot(rotation_matrix, vertex) for vertex in self.verticess]

        self.canvas_3d.delete("all")

        self.draw_3d_mesh()

    def on_canvas_left_click(self, event):
        x, y = event.x, event.y
        for vertex in self.vertices:
            if abs(vertex.x - x) <= 5 and abs(vertex.y - y) <= 5:
                self.active_vertex = vertex
                self.line = self.canvas_2d.create_line(x, y, x, y)
                break

    def on_canvas_right_click(self, event):
        x, y = event.x, event.y

        vertex = self.canvas_2d.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')
        self.vertices.append(Vertex(x, y, 0))
        self.print_vertices_to_console()

    def on_canvas_drag(self, event):
        if self.line:
            x, y = event.x, event.y
            self.canvas_2d.coords(self.line, self.active_vertex.x, self.active_vertex.y, x, y)

    def on_canvas_release(self, event):
        if self.line:
            x, y = event.x, event.y
            self.canvas_2d.delete(self.line)
            self.line = None

            # Check if there's a vertex at the release point
            target_vertex = None
            for vertex in self.vertices:
                if abs(vertex.x - x) <= 5 and abs(vertex.y - y) <= 5:
                    target_vertex = vertex
                    break

            if target_vertex:
                self.canvas_2d.create_line(self.active_vertex.x, self.active_vertex.y, target_vertex.x, target_vertex.y)
                self.connections.append((self.active_vertex, target_vertex))
                self.print_connections_to_console()

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
        self.canvas_2d.delete("all")
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
            vertex.display = self.canvas_2d.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')
            # Display the z-coordinate as text near the vertex
            self.canvas_2d.create_text(x + 10, y - 10, text=f"({vertex.x:.2f}, {vertex.y:.2f}, {vertex.z:.2f})")

        # Draw connections with 3D rotations
        for vertex1, vertex2 in self.connections:
            x1, y1, z1 = vertex1.current_position
            x2, y2, z2 = vertex2.current_position
            x1, y1 = self.world_to_screen(x1, y1, z1)
            x2, y2 = self.world_to_screen(x2, y2, z2)
            self.canvas_2d.create_line(x1, y1, x2, y2)
    
    @staticmethod
    def rotate_point(x, y, angle):
        # Rotate point (x, y) by angle degrees around the origin
        angle_rad = math.radians(angle)
        new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
        return new_x, new_y

    def print_vertices_to_console(self):
        vertex_positions = [(vertex.x, vertex.y, vertex.z) for vertex in self.vertices]
        print("Vertex positions:")
        print(vertex_positions)

    def print_connections_to_console(self):
        connection_indices = []
        for vertex1, vertex2 in self.connections:
            index1 = self.vertices.index(vertex1)
            index2 = self.vertices.index(vertex2)
            connection_indices.append((index1, index2))
        print("Connections:")
        print(connection_indices)
    
    def screen_to_world(self, x, y):
        # Convert screen coordinates to world coordinates with z-data based on rotation
        x -= self.canvas_2d.winfo_width() / 2
        y -= self.canvas_2d.winfo_height() / 2
        x, y = self.rotate_point(x, y, self.rotation_z_angle)
        x, z = self.rotate_point(x, 0, self.rotation_x_angle)
        y, z = self.rotate_point(y, z, self.rotation_y_angle)

        # Adjust z-coordinate based on y-axis rotation angle
        if self.active_vertex:
            z += self.active_vertex.z

        return x, y, z


    def world_to_screen(self, x, y, z):
        # Convert world coordinates to screen coordinates with perspective projection and z-rotation
        distance = 500
        f = distance / (distance + z)  # Perspective scaling factor
        x, y = self.rotate_point(x, y, self.rotation_z_angle)  # Apply z-rotation
        x = x * f
        y = y * f

        # Adjust coordinates to make (0, 0) represent the center of the canvas
        x += self.canvas_2d.winfo_width() / 2
        y += self.canvas_2d.winfo_height() / 2
        return x, y

root = tk.Tk()
app = GraphEditorApp(root)
root.mainloop()
