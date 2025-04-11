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

    #depth BVH
    max_depth = int(np.floor(np.log2(tricount)))
    print("Depth of BVH (max:", max_depth, "): ", end="")
    depth = int(input(""))
    if depth > max_depth:
        depth = max_depth
    
    BVH = make_box(triangle_list, depth)


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