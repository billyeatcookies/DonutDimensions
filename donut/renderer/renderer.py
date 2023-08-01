import math
import random
import numpy as np
import tkinter as tk

class Renderer:
    def __init__(self):
        self.vertices = [
            # (100, 100, 100),
            # (100, 100, -100),
            # (100, -100, 100),
            # (100, -100, -100),
            # (-100, 100, 100),
            # (-100, 100, -100),
            # (-100, -100, 100),
            # (-100, -100, -100)
        ]

        self.edges = [
        #     (0, 1), (0, 2), (0, 4),
        #     (1, 3), (1, 5),
        #     (2, 3), (2, 6),
        #     (3, 7),
        #     (4, 5), (4, 6),
        #     (5, 7),
        #     (6, 7)
        ]

        self.faces = [
            # (0, 2, 6, 4),
            # (0, 1, 3, 2),
            # (0, 4, 5, 1),
            # (1, 5, 7, 3),
            # (2, 3, 7, 6),
            # (4, 6, 7, 5)
        ]

        self.load_obj('horror.obj')
        print(self.vertices, self.faces)

        self.rotation_matrix = np.eye(3)
        self.light_source = [200, -200, 200]

        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        self.d = 500 

        self.slider = tk.Scale(self.root, from_=1, to=500, orient=tk.HORIZONTAL,
                                    command=self.on_zoom_change)
        self.slider.set(500)
        self.slider.pack(side=tk.LEFT)

        self.wireframe = False
        tk.Button(self.root, text="wireframe", command=self.wireframe_toggle).pack()
    
    def wireframe_toggle(self):
        self.wireframe = not self.wireframe
    
    def load_obj(self, file_path):
        with open(file_path, 'r') as obj_file:
            for line in obj_file:
                if line.startswith('v '):
                    _, x, y, z = line.strip().split()
                    self.vertices.append((float(x)*100, float(y)*100, float(z)*100))
                elif line.startswith('f '): 
                    _, *face_indices = line.strip().split()
                    face_indices = [int(idx.split('/')[0]) - 1 for idx in face_indices]
                    self.faces.append(tuple(face_indices))
                    
    def on_zoom_change(self, _):
        self.d = int(self.slider.get())
        self.canvas.delete("all")
        self.draw_mesh()

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

    def project_vertex(self, vertex):
        transformed_vertex = np.dot(self.rotation_matrix, vertex)
        x, y, z = transformed_vertex
        if z != 0:
            projected_x = x * self.d / (z + self.d)
            projected_y = y * self.d / (z + self.d)
            return projected_x, projected_y
        else:
            return x, y

    def perspective_projection(self, vertices):
        projected_vertices = [self.project_vertex(vertex) for vertex in vertices]
        return projected_vertices

    def is_backfacing(self, face):
        v1 = np.array(self.vertices[face[0]])
        v2 = np.array(self.vertices[face[1]])
        v3 = np.array(self.vertices[face[2]])
        normal = np.cross(v2 - v1, v3 - v1)

        view_vector = np.array([0, 0, -1])  # towards me
        return np.dot(normal, view_vector) > 0

    def sort_faces(self):
        face_depths = []
        for face in self.faces:
            depth_sum = 0
            for vertex_index in face:
                x, y, z = self.vertices[vertex_index]
                depth_sum += z
            avg_depth = depth_sum / len(face)
            face_depths.append((face, avg_depth))

        sorted_faces = sorted(face_depths, key=lambda item: item[1], reverse=True)
        return [face for face, _ in sorted_faces]

    def draw_mesh(self):
        for face in self.sort_faces():
            if self.is_backfacing(face):  # skip backfacing faces
                continue

            v1 = np.array(self.vertices[face[0]])
            v2 = np.array(self.vertices[face[1]])
            v3 = np.array(self.vertices[face[2]])
            normal = np.cross(v2 - v1, v3 - v1)

            to_light = np.array(self.light_source) - v1
            cos_theta = np.dot(normal, to_light) / (np.linalg.norm(normal) * np.linalg.norm(to_light))

            shade = int(255 * (cos_theta + 1) / 2)
            color = '#{:02x}{:02x}{:02x}'.format(shade, shade, shade)

            coords = self.perspective_projection([self.vertices[i] for i in face if isinstance(i, int)])
            coords = [(x + 250, y + 250) for x, y in coords]  # Offset the coordinates
            self.canvas.create_polygon(coords, fill=color if not self.wireframe else "", outline="black" if self.wireframe else "")

        # for edge in self.edges:
        #     x1, y1, z1 = self.vertices[edge[0]]
        #     x2, y2, z2 = self.vertices[edge[1]]
        #     coords = self.perspective_projection([(x1, y1, z1), (x2, y2, z2)])
        #     x1, y1 = coords[0]
        #     x2, y2 = coords[1]
        #     self.canvas.create_line(x1 + 250, y1 + 250, x2 + 250, y2 + 250)

        # for vertex in self.vertices:
        #     x, y, z = vertex
        #     coords = self.perspective_projection([(x, y, z)])
        #     x, y = coords[0]
        #     r = 5
        #     self.canvas.create_oval(x - r + 250, y - r + 250, x + r + 250, y + r + 250, fill='white')

    def animate(self):
        self.rotation_matrix = np.dot(self.rotate_x(0.01), np.dot(self.rotate_y(0.02), self.rotate_z(0.03)))
        self.vertices = [np.dot(self.rotation_matrix, vertex) for vertex in self.vertices]

        self.canvas.delete("all")
        self.draw_mesh()

        self.root.after(10, self.animate)

    def run(self):
        self.animate()
        self.root.mainloop()

if __name__ == "__main__":
    mesh = Renderer()
    mesh.run()
