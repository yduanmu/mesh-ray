import numpy as np
from stl import mesh as m

def main():
    while True:
        print("\n------------------------------------------------------------------")
        file = str(input("File: "))
        if file == "quit":
            break
        mesh = m.Mesh.from_file('./mesh/'+file)
        point_list = np.unique(mesh.vectors.reshape(-1, 3), axis=0) #list of unique points in the mesh
        # print(point_list)

        r_orig_str = str(input("x y z coordinates of ray origin: ")).split(" ")
        r_orig = [float(i) for i in r_orig_str]
        r_dir_str = str(input("x y z coordinates of ray direction: ")).split(" ")
        r_dir = [float(i) for i in r_dir_str]
        
        print("------------------------------------------------------------------")
main()