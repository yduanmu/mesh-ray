import numpy as np
from stl import mesh as m

class Triangle:
    def __init__(self, index, v1, v2, v3):
        self.index = index
        self.v1 = np.array(v1)
        self.v2 = np.array(v2)
        self.v3 = np.array(v3)
        self.centroid = self.find_centroid(v1, v2, v3)
        self.maxp = np.maximum(np.maximum(self.v1, self.v2), self.v3)
        self.minp = np.minimum(np.minimum(self.v1, self.v2), self.v3)
    
    def find_centroid(self, p1, p2, p3):
        x = (p1[0] + p2[0] + p3[0])/3
        y = (p1[1] + p2[1] + p3[1])/3
        z = (p1[2] + p2[2] + p3[2])/3
        return np.array([x, y, z])

class Bounding_Box:
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.contained_triangles = None
        self.maxp = None
        self.minp = None

def merge_boxes(min1, max1, min2, max2):
    return np.minimum(min1, min2), np.maximum(max1, max2)

def make_box(triangle_arr, depth): #depth counts down
    if len(triangle_arr) == 0:
        return None
    
    bounding_box = Bounding_Box()
    
    box_min = triangle_arr[0].minp
    box_max = triangle_arr[0].maxp

    for tri in triangle_arr[1:]:
        box_min, box_max = merge_boxes(box_min, box_max, tri.minp, tri.maxp)
    
    bounding_box.minp = box_min
    bounding_box.maxp = box_max

    if depth == 0 or len(triangle_arr) <= 1: #leaf
        bounding_box.contained_triangles = triangle_arr
        print("min: ", bounding_box.minp, " max: ", bounding_box.maxp)
        return bounding_box
    else: #split triangle_arr based off centroids, lesser half into left child and greater half into right child
        median = [np.abs(bounding_box.maxp[0]) - np.abs(bounding_box.minp[0]),
                  np.abs(bounding_box.maxp[1]) - np.abs(bounding_box.minp[1]),
                  np.abs(bounding_box.maxp[2]) - np.abs(bounding_box.minp[2])]
        split_axis = median.index(max(median))
        triangle_arr.sort(key=lambda t: t.centroid[split_axis])
        left_arr = triangle_arr[:len(triangle_arr)//2]
        right_arr = triangle_arr[len(triangle_arr)//2:]
        
        bounding_box.left_child = make_box(left_arr, depth-1)
        bounding_box.right_child = make_box(right_arr, depth-1)
        return bounding_box

#slab method for AABB hit
def slab(r_orig, r_dir, b_min, b_max):
    epsilon = 1e-8
    safe_dir = np.where(np.abs(r_dir) < epsilon, epsilon, r_dir) #avoid div by 0
    inv_dir = 1.0 / safe_dir

    t_low = (b_min - r_orig) * inv_dir
    t_high = (b_max - r_orig) * inv_dir

    t_close = np.minimum(t_low, t_high)
    t_far = np.maximum(t_low, t_high)

    t_enter = np.max(t_close)
    t_exit = np.min(t_far)

    if t_enter > t_exit or t_exit < 0:
        return False
    return True

#given a triangle, returns the plane equation in an numpy array [A, B, C, D] meaning Ax + By + Cz + D = 0
def find_planeq(tri):
    P = tri.v1
    Q = tri.v2
    R = tri.v3
    
    #a, b: vectors between P->Q and P->R respectively
    a = np.array(Q) - np.array(P)
    b = np.array(R) - np.array(P)
    
    #cross product a x b in order to find the normal vector
    n = np.cross(a, b)
    
    #find the "equals"
    d = -np.dot(n, P)

    return np.append(n, d)

#does the ray hit the triangle, and if so, where?
def tri_hit(r_orig, r_dir, tri):
    #check if ray is parallel to plane
    plane_normal = find_planeq(tri)[:3]
    epsilon = 1e-8
    if(np.absolute(np.dot(plane_normal, r_dir)) < epsilon):
        return False
    
    #find intersection


    return [True, coords]

#given a list of candidates (array with [triangle, coords]), finds the nearest hit to ray origin
def closest_hit(r_orig, r_dir, tri_candidates):
    return [tri, coords]

#starting from the root of BVH, return list of triangles hit contained within the smallest box
#if no hit at any point, return FALSE
def box_search(r_orig, r_dir, node):
    if node is None:
        return False
    
    #no hit, no life
    if not slab(r_orig, r_dir, node.minp, node.maxp):
        return False
    
    #leaf
    if node.left_child is None and node.right_child is None:
        tri_candidates = []
        for tri in node.contained_triangles:
            tri_hit = tri_hit(r_orig, r_dir, tri)
            if tri_hit[0]:
                tri_candidates.append([tri, tri_hit[1]])
        
        #find and return nearest hit to ray origin
        return closest_hit(r_orig, r_dir, tri_candidates)

    #recursively check children
    box_search(r_orig, r_dir, node.left_child)
    box_search(r_orig, r_dir, node.right_child)

def main():
    file = str(input("File: "))
    mesh = m.Mesh.from_file('./mesh/'+file)
    # point_list = np.unique(mesh.vectors.reshape(-1, 3), axis=0) #list of unique points in the mesh

    #find centroids
    triangle_list = []
    tricount = 0
    for i in range(len(mesh.vectors)):
        triangle_list.append(Triangle(i, mesh.vectors[i][0], mesh.vectors[i][1], mesh.vectors[i][2]))
        tricount += 1
    print("Triangle count: ", tricount)

    #depth for BVH
    max_depth = int(np.floor(np.log2(tricount)))
    print("Depth of BVH (max:", max_depth, "): ", end="")
    depth = int(input(""))
    if depth > max_depth:
        depth = max_depth
    
    #create BVH
    BVH = make_box(triangle_list, depth)

    #traverse BVH and use slab method for hits
    box_search(r_orig, r_dir, BVH)

    #arbitrary ray REPL
    while True:
        r_orig_str = str(input("x y z coordinates of ray origin: "))
        if r_orig_str == "quit":
            break
        else:
            #get ray origin and direction
            r_orig_str = r_orig_str.split(" ")
            r_orig = [float(i) for i in r_orig_str]
            r_dir_str = str(input("x y z coordinates of ray direction: ")).split(" ")
            r_dir = [float(i) for i in r_dir_str]
            print("")

main()