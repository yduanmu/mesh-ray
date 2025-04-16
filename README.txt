python3 -m venv .gitignore/mesh-ray
source .gitignore/mesh-ray/bin/activate
deactivate

pip freeze > requirements.txt
pip install -r requirements.txt


Mesh-ray algorithm:
1. Set up BVH.
    a. Boxes are minimum and axis-aligned, but not necessarily cubes.
    b. Pick longest axis of current box and split at midpoint. Triangles belong 
        to whichever boxes their centroids do.
    c. The depth is defined by the user, to a maximum of floor log2(triangles).
2. Test the ray against smaller and smaller bounding boxes with the slab method.
    a. If any box has no hits at all, RETURN NO HIT.
4. Once the smallest box is also confirmed a hit, test against all triangle faces
    inside that box.
    a. Check if ray is parallel to plane. (O: no hit, X: continue)
    b. Find intersection
    b. Use barycentric coordinates to check if intersection lies within the 
        triangle (O: continue, X: no hit)
    c. Check if intersection lies inside ray (O: continue, X: no hit)
5. Return the point of intersection and the index of the triangle.