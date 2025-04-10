import numpy as np
from stl import mesh as m

class Triangle:
    def __init__(self, index, v1, v2, v3):
        self.index = index
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.centroid = self.find_centroid(v1, v2, v3)
        self.max = self.find_max(v1, v2, v3)
        self.min = self.find_min(v1, v2, v3)
    
    def find_centroid(p1, p2, p3):
        x = (p1[0] + p2[0] + p3[0])/3
        y = (p1[1] + p2[1] + p3[1])/3
        z = (p1[2] + p2[2] + p3[2])/3
        return [x, y, z]
    
    def find_min(p1, p2, p3):
        min = [np.nan, np.nan, np.nan]
        for i in range(2):
            if np.isnan(min[i]) or min[i] > p1[i]:
                min[i] = p1[i]
            if np.isnan(min[i]) or min[i] > p2[i]:
                min[i] = p2[i]
            if np.isnan(min[i]) or min[i] > p3[i]:
                min[i] = p3[i]
        return min
    
    def find_max(p1, p2, p3):
        max = [np.nan, np.nan, np.nan]
        for i in range(2):
            if np.isnan(max[i]) or max[i] > p1[i]:
                max[i] = p1[i]
            if np.isnan(max[i]) or max[i] > p2[i]:
                max[i] = p2[i]
            if np.isnan(max[i]) or max[i] > p3[i]:
                max[i] = p3[i]
        return max

class Bounding_Box:
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.contained_triangles = None

def make_box(triangle_arr, box, depth):
    #box is defined by its smallest(0) and greatest(1) points
    box = np.array([np.nan, np.nan])
    for i in range(len(triangle_arr)):
        if np.isnan(box[0]) or box[0] > triangle_arr[i].min:
            box[0] = triangle_arr[i].index
        if np.isnan(box[1]) or box[1] < triangle_arr[i].max:
            box[1] = triangle_arr[i].index

def main():
    print("\n------------------------------------------------------------------")
    file = str(input("File: "))
    mesh = m.Mesh.from_file('./mesh/'+file)
    point_list = np.unique(mesh.vectors.reshape(-1, 3), axis=0) #list of unique points in the mesh
    # print(point_list)

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



            # Create BVH

            #find centroids
            triangle_list = []
            for i in range(len(mesh.vectors)):
                triangle_list.append(Triangle(i, mesh.vectors[i][0], mesh.vectors[i][1], mesh.vectors[i][2]))
            triangle_arr = np.array(triangle_list)
            
            
    
    print("------------------------------------------------------------------")
main()