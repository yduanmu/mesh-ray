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
        # print("min: ", bounding_box.minp, " max: ", bounding_box.maxp)
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
    
    d = -np.dot(n, P)

    return np.append(n, d)

#does the ray hit the triangle, and if so, where?
def tri_hit(r_orig, r_dir, tri):
    planeq = find_planeq(tri)
    no_hit = [False, 0]

    #check if ray is parallel to plane
    plane_normal = planeq[:3]
    epsilon = 1e-8
    if np.absolute(np.dot(plane_normal, r_dir)) < epsilon:
        return no_hit
    

    #find intersection
    line_const = r_orig
    line_t = r_dir
    denominator = np.sum(plane_normal * line_t)

    if np.absolute(denominator) < epsilon:
        return no_hit
    
    t = (planeq[3] - np.dot(plane_normal, line_const)) / denominator
    
    intersection = line_const + (line_t * t)


    #check if intersection is in triangle (corners and edges count)
    #https://math.stackexchange.com/questions/4322/check-whether-a-point-is-within-a-3d-triangle
    tri_area = 0.5 * np.linalg.norm(np.cross(tri.v2 - tri.v1, tri.v3 - tri.v1))
    alpha = (np.linalg.norm(np.cross(tri.v2 - intersection, tri.v3 - intersection))) / (2 * tri_area)
    beta = (np.linalg.norm(np.cross(tri.v3 - intersection, tri.v1 - intersection))) / (2 * tri_area)
    gamma = 1 - alpha - beta
    minor_ep0 = 0 - epsilon
    major_ep1 = 1 + epsilon

    if not ((alpha >= minor_ep0 and alpha < major_ep1) and (beta >= minor_ep0 and beta < major_ep1) and (gamma >= minor_ep0 and gamma < major_ep1) and (np.absolute((alpha + beta + gamma) - 1.0) <= epsilon)):
        return no_hit
    

    #check if intersection is on ray
    if t < 0:
        return no_hit
    
    # print(f"[DEBUG] t: {t}, Intersection: {intersection}, Origin: {r_orig}")
    return [True, intersection]


#given two points np.array([x, y, z]), return the distance between the two
def calc_dist(p1, p2):
    return np.absolute(np.sqrt(np.sum(np.power(p1-p2, 2))))


#given a list of candidates (array with [triangle, intersection]), finds the nearest hit to ray origin
def closest_hit(r_orig, tri_candidates):
    closest_tri = tri_candidates[0][0]
    closest_coords = tri_candidates[0][1]
    closest_dist = calc_dist(tri_candidates[0][1], r_orig)
    # print(tri_candidates[0][0].index, ": ", closest_dist)

    for tri_can in tri_candidates[1:]:
        dist = calc_dist(tri_can[1], r_orig)
        if dist < closest_dist:
            closest_dist = dist
            closest_tri = tri_can[0]
            closest_coords = tri_can[1]
            # print(closest.index, ": ", closest_dist)

    return [closest_tri.index, closest_coords, closest_dist]


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
        # print("contained tri #: ", len(node.contained_triangles))
        for tri in node.contained_triangles:
            hit_result = tri_hit(r_orig, r_dir, tri)
            if hit_result[0]:
                tri_candidates.append([tri, hit_result[1]])
            # else:
            #     print("no hit")
        
        #find and return nearest hit to ray origin
        if len(tri_candidates) > 0:
            return closest_hit(r_orig, tri_candidates)
        else:
            return False

    #recursively check children
    left = box_search(r_orig, r_dir, node.left_child)
    right = box_search(r_orig, r_dir, node.right_child)

    if left and right:
        # print("left: ", left)
        if(type(left)==list and type(right)==list):
            if np.minimum(left[2], right[2]) == left[2]:
                return left
            else:
                return right
    elif left:
        return left
    elif right:
        return right
    else:
        return False


def main():
    file = str(input("File: "))
    mesh = m.Mesh.from_file('./mesh/'+file)
    # point_list = np.unique(mesh.vectors.reshape(-1, 3), axis=0) #list of unique points in the mesh

    #find centroids
    triangle_list = []
    tricount = 0
    for i in range(len(mesh.vectors)):
        triangle_list.append(Triangle(i, mesh.vectors[i][0], mesh.vectors[i][1], mesh.vectors[i][2]))
        # print(triangle_list[i].index)
        tricount += 1
    print("Triangle count: ", tricount)

    #depth for BVH
    max_depth = int(np.floor(np.log2(tricount)))
    print("Depth of BVH (max:", max_depth, "): ", end="")
    depth = int(input(""))
    if depth > max_depth or depth < 1:
        depth = max_depth
    
    #create BVH
    BVH = make_box(triangle_list, depth)

    #arbitrary ray REPL
    while True:
        r_orig_str = str(input("x y z coordinates of ray origin: "))
        if r_orig_str == "stop":
            break
        else:
            #get ray origin and direction
            r_orig_str = r_orig_str.split(" ")
            r_orig = np.array([float(i) for i in r_orig_str])
            r_dir_str = str(input("x y z coordinates of ray direction as a point: ")).split(" ")
            r_point = np.array([float(i) for i in r_dir_str])
            r_dir = r_point - r_orig
            r_dir = r_dir / np.linalg.norm(r_dir)

            #traverse BVH and use slab method for hits
            traverse = box_search(r_orig, r_dir, BVH)
            if traverse:
                print(f"Index: {traverse[0]}, Coordinates: {traverse[1]}")
            else:
                print("No valid intersection.")

            print("")

main()