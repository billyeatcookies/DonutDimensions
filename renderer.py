import math, random
import numpy as np
import tkinter as tk

vertices = [
    (100, 100, 100),
    (100, 100, -100),
    (100, -100, 100),
    (100, -100, -100),
    (-100, 100, 100),
    (-100, 100, -100),
    (-100, -100, 100),
    (-100, -100, -100)
]

edges = [
    (0, 1), (0, 2), (0, 4),
    (1, 3), (1, 5),
    (2, 3), (2, 6),
    (3, 7),
    (4, 5), (4, 6),
    (5, 7),
    (6, 7)
]

faces = [
    (0, 2, 6, 4),
    (0, 1, 3, 2),
    (0, 4, 5, 1),
    (1, 5, 7, 3),
    (2, 3, 7, 6),
    (4, 6, 7, 5)
]

def rotate_x(theta):
    return [
        [1, 0, 0],
        [0, math.cos(theta), -math.sin(theta)],
        [0, math.sin(theta), math.cos(theta)]
    ]

def rotate_y(theta):
    return [
        [math.cos(theta), 0, math.sin(theta)],
        [0, 1, 0],
        [-math.sin(theta), 0, math.cos(theta)]
    ]

def rotate_z(theta):
    return [
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
    ]

def perspective_projection(vertices, d=500):
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

def draw_mesh(vertices, edges, faces):
    light_source = [500, -500, 500]
    light_vector = np.array(light_source)
    distances = [(sum([np.dot(vertices[face[i]], light_vector) for i in range(len(face))])/3, face) for face in faces]
    distances.sort(reverse=True)

    for _, face in distances:
        v1 = np.array(vertices[face[0]])
        v2 = np.array(vertices[face[1]])
        v3 = np.array(vertices[face[2]])
        normal = np.cross(v2 - v1, v3 - v1)

        to_light = np.array(light_source) - v1
        cos_theta = np.dot(normal, to_light) / (np.linalg.norm(normal) * np.linalg.norm(to_light))

        shade = int(255 * (cos_theta + 1) / 2)
        color = '#{:02x}{:02x}{:02x}'.format(shade, shade, shade)

        coords = perspective_projection([vertices[i] for i in face if isinstance(i, int)])
        canvas.create_polygon(coords, fill=color)

    for edge in edges:
        x1, y1, z1 = vertices[edge[0]]
        x2, y2, z2 = vertices[edge[1]]
        coords = perspective_projection([(x1, y1, z1), (x2, y2, z2)])
        x1, y1 = coords[0]
        x2, y2 = coords[1]
        canvas.create_line(x1 + 250, y1 + 250, x2 + 250, y2 + 250)

    for vertex in vertices:
        x, y, z = vertex
        coords = perspective_projection([(x, y, z)])
        x, y = coords[0]
        r = 5
        canvas.create_oval(x - r + 250, y - r + 250, x + r + 250, y + r + 250, fill='white')

def animate():
    global vertices

    rotation_matrix = np.dot(rotate_x(0.01), np.dot(rotate_y(0.02), rotate_z(0.03)))
    vertices = [np.dot(rotation_matrix, vertex) for vertex in vertices]

    canvas.delete("all")

    draw_mesh(vertices, edges, faces)

    root.after(10, animate)

root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

animate()
root.mainloop()
