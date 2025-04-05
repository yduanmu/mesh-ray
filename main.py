import numpy as np
from stl import mesh as m

class Halfedge:
    def __init__(self, start, end, next=None, twin=None):
        self.start = start #starting vertex
        self.end = end #ending vertex
        self.next = next
        self.twin = twin

#simple hash for vertex lookup
def vertexhash(v1, v2):
    v_arr = np.sort(np.array([v1, v2]))

def parse_halfedges(file):
    mesh = m.Mesh.from_file(file)
    facenum = mesh.vectors.shape[0]
    vertices = mesh.vectors #vertex class from numpy_stl: x, y, z
    halfedges = []

    #List of halfedges
    for i in range(facenum):
        face = vertices[i]
        hev_start, hev_end = face[0], face[1] #hev = half edge vertex
        halfedge = Halfedge(hev_start, hev_end)
        halfedge.next = Halfedge(hev_end, face[2], next=halfedge)
        halfedges.append(halfedge)
    
    #Setting twins

    return halfedges

def main():
    while True:
        print("\n------------------------------------------------------------------")
        file = str(input("File: "))
        if file == "quit":
            break
        parse_halfedges(file)

        r_orig = str(input("x y z coordinates of ray origin: ")).split(" ")
        r_dir = str(input("x y z coordinates of ray direction: ")).split(" ")
        
        print("------------------------------------------------------------------")
main()