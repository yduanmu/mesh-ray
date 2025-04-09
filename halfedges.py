'''Scrapped halfedge code'''

import numpy as np
from stl import mesh as m

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
