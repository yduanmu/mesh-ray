import numpy as np
from stl import mesh as m
from numpy import random

class K3DTree_Node: #K3D: 3-d tree (k-d tree)
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.dim = None
        self.val = None

class K3DTree:
    def __init__(self):
        self.root = None

#given a list of points, randomly selects the median out of 9 points (sort these 9 by given dimension)
#returns the index of the median point
#if <=k but >2 points, selects the median out of all of them
#if 2 points, select the first point
#if 1 point, just select it.
def choose_median(point_list, dim):
    selected_list = []
    point_index = []
    k = max(int(np.sqrt(len(point_list))), 30) #central limit theorem

    #select k or less points from which to calculate median
    if len(point_list) >= k:
        for i in range(k):
            point_index.append(random.randint(len(point_list)-1))
            selected_list.append(point_list[point_index[i]])
            np.delete(point_list, point_index[i])
    elif len(point_list) == 2 or len(point_list) == 1:
        return 0
    else:
        selected_list = np.array(point_list)
        for i in range(len(selected_list)):
            point_index.append(i)
    
    selected_nplist = np.array(selected_list)

    #calculate median based on dim
    sorted_list = selected_nplist[selected_nplist[:, dim].argsort()] #dim 0=x, 1=y, 2=z
    median = sorted_list[len(sorted_list)//2]
    print("median: ",median)

    #find which index that was (could optimize this with a dictionary but meh, <=30 points should be fast enough)
    for i in range(len(selected_nplist)):
        if median[0] == selected_nplist[i][0] and median[1] == selected_nplist[i][1] and median[2] == selected_nplist[i][2]:
            median_index = point_index[i]
    return median_index

def make_K3DTree(point_list, node, depth):\
    #choose the axis of this level and set current node value
    axis = depth % 3 #axis 0=x, 1=y, 2=z
    median = choose_median(point_list, axis)
    node.val = median
    node.dim = axis

    #left and right children
    before_list = [] #points before median
    after_list = [] #points after median
    node.left_child = make_K3DTree(before_list, K3DTree_Node(), depth+1)
    node.right_child = make_K3DTree(after_list, K3DTree_Node(), depth+1)

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

def parse_halfedges(mesh):
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
        mesh = m.Mesh.from_file('./mesh/'+file)
        point_list = np.unique(mesh.vectors.reshape(-1, 3), axis=0) #list of unique points in the mesh
        print(point_list)
        print(choose_median(point_list, 0))
        parse_halfedges(mesh)
        kdtree = make_K3DTree(point_list, 0)

        r_orig = str(input("x y z coordinates of ray origin: ")).split(" ")
        r_dir = str(input("x y z coordinates of ray direction: ")).split(" ")
        
        print("------------------------------------------------------------------")
main()