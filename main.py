import numpy as np
from stl import mesh as m

class K3DTree_Node: #K3D: 3-d tree (k-d tree)
    def __init__(self):
        self.left = None
        self.right = None
        self.dim = None
        self.val = None

class K3DTree:
    def __init__(self):
        self.root = None

#given a list of points, randomly selects the median out of 9 points (sort these 9 by given dimension)
#if <=9 but >2 points, selects the median out of all of them
#if 2 points, select the first point
#if 1 point, just select it.
def choose_median(point_list, dim):

def make_K3DTree(point_list, depth):
    axis = depth % 3 # 0=x, 1=y, 2=z

class Halfedge:
    def __init__(self, start, end, next=None, twin=None):
        self.start = start #starting vertex
        self.end = end #ending vertex
        self.next = next
        self.twin = twin

#vertex pairs for vertex lookup in dictionary
def vertex_key(v1, v2):
    v_arr = np.round(np.array([v1, v2]), decimals=5)
    return str(v_arr[0])+str(v_arr[1])

def parse_halfedges(file):
    mesh = m.Mesh.from_file('./mesh/'+file)
    vertices = mesh.vectors #vertex class from numpy_stl: x, y, z
    halfedge_dict = {}

    #create list of halfedges
    for i in range(mesh.vectors.shape[0]): #shape=[number of faces, vertices per face, coords per vertex]
        face = vertices[i]

        he0 = Halfedge(face[0], face[1])
        he1 = Halfedge(face[1], face[2])
        he2 = Halfedge(face[2], face[0])
        he0.next = he1
        he1.next = he2
        he2.next = he0

        for he in (he0, he1, he2):
            he_key = vertex_key(he.start, he.end)
            twin_key = vertex_key(he.end, he.start)   
            halfedge_dict[he_key] = he   

            if twin_key in halfedge_dict:
                halfedge_dict[he_key].twin = halfedge_dict[twin_key]
                halfedge_dict[twin_key].twin = he

    return halfedge_dict

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