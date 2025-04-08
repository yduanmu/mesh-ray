import numpy as np
from stl import mesh as m
from numpy import random

class K3DTree_Node: #K3D: 3-d tree (k-d tree)
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.dim = None
        self.val = None

class Sorted_Points:
    def __init__(self, unsorted_list=None, sorted_x_list=None, sorted_y_list = None, sorted_z_list=None):
        self.unsorted_list = unsorted_list

        if sorted_x_list is None:
            self.sorted_x_list = self.sort_points_list(unsorted_list, 0)
        else:
            self.sorted_x_list = sorted_x_list
        
        if sorted_y_list is None:
            self.sorted_y_list = self.sort_points_list(unsorted_list, 1)
        else:
            self.sorted_y_list = sorted_y_list
        
        if sorted_z_list is None:
            self.sorted_z_list = self.sort_points_list(unsorted_list, 2)
        else:
            self.sorted_z_list = sorted_z_list

    #given a point list, sorts based on dimension and returns sorted list
    def sort_points_list(self, point_list, dim):
        np_list = np.array(point_list)
        return np_list[np_list[:, dim].argsort()] #dim 0=x, 1=y, 2=z

#given a sorted point list, returns the value of the median
def choose_median(sorted_point_list):
    if len(sorted_point_list) == 2 or len(sorted_point_list) == 1:
        return sorted_point_list[0]
    else:
        return sorted_point_list[len(sorted_point_list)//2]

#given a set of Sorted_Points, node, and depth, recursively makes k-d tree
def make_K3DTree(sorted_points, node, depth):
    #choose the dimension of this level
    dim = depth % 3 #dim 0=x, 1=y, 2=z
    node.dim = dim

    #set current node value
    if dim == 0:
        sorted_dim_list = sorted_points.sorted_x_list
    elif dim == 1:
        sorted_dim_list = sorted_points.sorted_y_list
    else:
        sorted_dim_list = sorted_points.sorted_z_list
    median = choose_median(sorted_dim_list)
    node.val = median

    #recursively make k-d tree
    if len(sorted_dim_list) <= 1: #leaf
        return node
    elif len(sorted_dim_list) == 2:
        node.right_child = K3DTree_Node()
        node.right_child.val = sorted_dim_list[1]
        node.right_child.dim = (depth+1)%3
        return node
    else: #left and right children
        median_index = len(sorted_dim_list)//2
        #before median
        before_points = Sorted_Points(sorted_x_list=sorted_points.sorted_x_list[:median_index, 0:].copy(),
                                      sorted_y_list=sorted_points.sorted_y_list[:median_index, 0:].copy(),
                                      sorted_z_list=sorted_points.sorted_z_list[:median_index, 0:].copy())

        #after median
        after_points = Sorted_Points(sorted_x_list=sorted_points.sorted_x_list[median_index+1:, 0:].copy(),
                                     sorted_y_list=sorted_points.sorted_y_list[median_index+1:, 0:].copy(),
                                     sorted_z_list=sorted_points.sorted_z_list[median_index+1:, 0:].copy())

        node.left_child = make_K3DTree(before_points, K3DTree_Node(), depth+1)
        node.right_child = make_K3DTree(after_points, K3DTree_Node(), depth+1)
        return node

def preorder_K3DTree(node, indent=0):
    if node:
        print(" " * indent, node.val, " ", node.dim)
        preorder_K3DTree(node.left_child, indent+4)
        preorder_K3DTree(node.right_child, indent+4)

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
        parse_halfedges(mesh)

        sorted_points = Sorted_Points(unsorted_list=point_list)
        root = K3DTree_Node()
        kdtree = make_K3DTree(sorted_points, root, 0)
        print(type(kdtree))
        preorder_K3DTree(kdtree)

        r_orig = str(input("x y z coordinates of ray origin: ")).split(" ")
        r_dir = str(input("x y z coordinates of ray direction: ")).split(" ")
        
        print("------------------------------------------------------------------")
main()