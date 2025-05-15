from ursina import *
from ursina.mesh import Mesh
import math

app = Ursina(borderless=False)

window.color = color.rgba(8, 12, 32, 255)  # SGI-style deep blue

# Helper for wire spheres (low poly for retro)
def wire_sphere(radius=1, rings=8, sectors=8, color=color.white, parent=None):
    verts = []
    edges = []
    for r in range(rings+1):
        phi = math.pi * r / rings
        for s in range(sectors):
            theta = 2 * math.pi * s / sectors
            x = radius * math.sin(phi) * math.cos(theta)
            y = radius * math.cos(phi)
            z = radius * math.sin(phi) * math.sin(theta)
            verts.append(Vec3(x, y, z))
    # connect longitude lines
    for r in range(rings+1):
        for s in range(sectors):
            start = r * sectors + s
            end = r * sectors + ((s+1)%sectors)
            edges.append((start, end))
    # connect latitude lines
    for r in range(rings):
        for s in range(sectors):
            start = r * sectors + s
            end = (r+1) * sectors + s
            edges.append((start, end))
    lines = []
    for start, end in edges:
        line = Entity(
            model=Mesh(vertices=[verts[start], verts[end]], mode='line', thickness=1.4),
            color=color,
            parent=parent
        )
        lines.append(line)
    return lines

class WireTetrahedron(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        v = [Vec3(1,1,1), Vec3(-1,-1,1), Vec3(-1,1,-1), Vec3(1,-1,-1)]
        edges = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
        for a,b in edges:
            Entity(
                model=Mesh(vertices=[v[a], v[b]], mode='line', thickness=1.4),
                color=color.lime,
                parent=self,
            )

class WireCube(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        v = [
            Vec3(-1,-1,-1), Vec3(-1,1,-1), Vec3(1,1,-1), Vec3(1,-1,-1),
            Vec3(-1,-1,1), Vec3(-1,1,1), Vec3(1,1,1), Vec3(1,-1,1)
        ]
        edges = [
            (0,1),(1,2),(2,3),(3,0), (4,5),(5,6),(6,7),(7,4),
            (0,4),(1,5),(2,6),(3,7)
        ]
        for a,b in edges:
            Entity(
                model=Mesh(vertices=[v[a], v[b]], mode='line', thickness=1.7),
                color=color.cyan,
                parent=self,
            )

# Entities
cube = WireCube()
cube.scale = 1.25
cube.position = (-2, 0, 0)

tetra = WireTetrahedron()
tetra.scale = 1.25
tetra.position = (2, 0, 0)

sphere_lines = wire_sphere(radius=1.1, rings=9, sectors=13, color=color.magenta)
sphere_center = Entity()
for l in sphere_lines:
    l.parent = sphere_center
sphere_center.position = (0, 0, 0)

# Fancy purple triangle in the background
triangle = Entity(model=Mesh(vertices=[Vec3(0,4,5), Vec3(-4,-3,5), Vec3(4,-3,5)], triangles=[(0,1,2)]),
                  color=color.rgba(140,40,255,70), scale=1.7)

def update():
    cube.rotation_y += 1.4
    cube.rotation_x += 0.7
    tetra.rotation_z += 1.8
    tetra.rotation_y += 1.3
    sphere_center.rotation_x += 1.1
    sphere_center.rotation_z += 0.9
    triangle.rotation_z += 0.2

EditorCamera()
Text("SGI Indy Tech Demo", y=0.45, color=color.lime, origin=(0,0), scale=1.5, background=True)

app.run()
