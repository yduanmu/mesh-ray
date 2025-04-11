import numpy as np
from stl import mesh as m

class Triangle:
    def __init__(self, index, v1, v2, v3):
        self.index = index
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.centroid = self.find_centroid(v1, v2, v3)
        self.max = find_max([v1, v2, v3])
        self.min = find_min([v1, v2, v3])
    
    def find_centroid(self, p1, p2, p3):
        x = (p1[0] + p2[0] + p3[0])/3
        y = (p1[1] + p2[1] + p3[1])/3
        z = (p1[2] + p2[2] + p3[2])/3
        return [x, y, z]

def find_min(point_arr):
    min = [np.nan, np.nan, np.nan]
    for i in range(len(point_arr)):
        for j in range(3):
            if np.isnan(min[j]) or min[j] > point_arr[i][j]:
                min[j] = point_arr[i][j]
    return min

def find_max(point_arr):
    max = [np.nan, np.nan, np.nan]
    for i in range(len(point_arr)):
        for j in range(3):
            if np.isnan(max[j]) or max[j] < point_arr[i][j]:
                max[j] = point_arr[i][j]
    return max

class Bounding_Box:
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.contained_triangles = None
        self.max = None
        self.min = None

def make_box(triangle_arr, bounding_box, depth): #depth counts down
    bounding_box.min = find_min(triangle_arr)
    bounding_box.max = find_max(triangle_arr)
    bounding_box.contained_triangles = triangle_arr

    #split triangle_arr based off centroids, lesser half into left child and greater half into right child
    


def main():
    # tri = Triangle(1, [0, 0, 0], [1, 2, 0], [2, 1, 0])
    # print(tri.max)
    # print(tri.min)
    print("\n------------------------------------------------------------------")
    file = str(input("File: "))
    mesh = m.Mesh.from_file('./mesh/'+file)
    point_list = np.unique(mesh.vectors.reshape(-1, 3), axis=0) #list of unique points in the mesh
    # print(point_list)


    #find centroids
    triangle_list = []
    tricount = 0
    for i in range(len(mesh.vectors)):
        triangle_list.append(Triangle(i, mesh.vectors[i][0], mesh.vectors[i][1], mesh.vectors[i][2]))
        tricount += 1
    triangle_arr = np.array(triangle_list)
    print(tricount)

    #depth BVH
    max_depth = int(np.floor(np.log2(tricount)))
    print("Depth of BVH (max:", max_depth, "): ", end="")
    depth = int(input(""))
    if depth > max_depth:
        depth = max_depth

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

            
    
    print("------------------------------------------------------------------")
main()