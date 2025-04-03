import numpy as np
import trimesh as tm

def main():
    while True:
        print("\n------------------------------------------------------------------")
        file = str(input("File: "))
        if file == "quit":
            break
        
        mesh = tm.load('./mesh/' + file)
        r_orig = str(input("x y z coordinates of ray origin: ")).split(" ")
        r_dir = str(input("x y z coordinates of ray direction: ")).split(" ")
        
        print("------------------------------------------------------------------")
main()