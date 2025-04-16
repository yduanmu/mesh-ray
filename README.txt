python3 -m venv .gitignore/mesh-ray
source .gitignore/mesh-ray/bin/activate
deactivate

pip freeze > requirements.txt
pip install -r requirements.txt


Mesh-ray algorithm:
1. Set up a bounding-volume hierarchy.
    a. Boxes are minimum and axis-aligned, but not necessarily cubes.
    b. Pick longest axis of current box and split at midpoint. Triangles belong 
        to whichever boxes their centroids do.
    c. The depth is defined by the user, to a maximum of floor log2(triangles).
2. Test the ray against smaller and smaller bounding boxes with the slab method.
    a. If both left and right boxes have no hits at all, RETURN NO HIT.
4. Once the smallest box is also confirmed a hit, test against all triangle faces
    inside that box.
    a. Check if ray is parallel to plane. (O: no hit, X: continue)
    b. Find intersection
    b. Use barycentric coordinates to check if intersection lies within the 
        triangle (O: continue, X: no hit)
    c. Check if intersection lies inside ray (O: continue, X: no hit)
5. Return the closest point of intersection and the index of the triangle.


Example output:

File: cat.stl
Triangle count:  386
Depth of BVH (max: 8 ): 5   
x y z coordinates of ray origin: -1 -1 -1
x y z coordinates of ray direction as a point: 100 100 100
Intersection at index: 374, coords: [0. 0. 0.]