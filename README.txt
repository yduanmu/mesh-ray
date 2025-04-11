python3 -m venv .gitignore/mesh-ray
source .gitignore/mesh-ray/bin/activate
deactivate

pip freeze > requirements.txt
pip install -r requirements.txt

stl2bin your_ascii_stl_file.stl new_binary_stl_file.stl
stl2ascii your_binary_stl_file.stl new_ascii_stl_file.stl
stl your_ascii_stl_file.stl new_binary_stl_file.stl


Mesh-ray algorithm:
1. Set up BVH.
    a. Boxes are minimum and axis-aligned, but not necessarily cubes.
    b. Pick longest axis of current box and split at midpoint. Triangles belong 
        to whichever boxes their centroids do.
    c. The maximum depth is defined by the user, to a max of floor log2(triangles).
2. Supplied origin and direction, store the parametric equation of the line 
    containing the ray.
3. Test the line against smaller and smaller bounding boxes using the cube-ray 
    algorithm from before (see below).
    a. If no hit in cube at any point, return.
4. Once the smallest box is also confirmed a hit, test against all triangle faces
    inside that box using the Möller–Trumbore ray-triangle intersection algorithm.
    a. Check if ray is parallel to plane. (O: return FALSE, X: continue)
    b. Use equation of plane and parametric equation of line to calculate 
        intersection.
    c. Check if within triangle.
    d. Check if on ray.
5. Return the point of intersection and the index of the triangle.


Cube-ray algorithm:
1. Check for nearest 4 vertices to origin of the ray.
    a. If the origin is equidistant between 4 vertices or exactly at a vertex, check 
        for the nearest 4 vertices to the direction of the ray. This is because, in 
        these two cases, the ray is only guaranteed to intersect with a face of the 
        cube once.
2. If those 4 points describe a valid face of the cube, then it finds the plane 
    equation for the plane containing that face.
3. Möller–Trumbore ray-triangle intersection algorithm
    a. Check if ray is parallel to plane. (O: return FALSE, X: continue)
    b. Check if within the cube face.
    c. Check if on ray.
6. Return TRUE/FALSE depending on whether there is intersection or not.


Time complexity analysis:
- getting all triangles:
    - max and min per triangle: O(N log N)
    - finding centroids: O(N), where N = number of triangles per mesh
        - O(N) to make list, O(N) to convert to numpy array
- make_box:
    - O(N), but then recursively


Notes:
- Check whether intersection is on a ray using dot product of the vectors 
    origin->intersection and origin->direction
- Checking intersection of line against plane is the same reused code between the cubes
    and the triangles, but cube only cares whether there is intersection or not.


Limitations:
- 


Hi Melissa,

This is great, and your explanation is great.  Now to make this program more general, 
can I suggest an important relaxation of the problem.

What if we don't have a cube, but an arbitrary triangular mesh?  A triangular mesh is 
basically a bunch of triangles, and an extremely important task in computer graphics is 
to find the closest hit/intersection between a ray and a triangular mesh.  So can you 
extend your ray-cube intersection code to a ray-mesh intersection code?  This will be 
the foundation of our later investigations.

You are definitely right that the exact orientation of the cube doesn't matter, and it's 
great that you are solving the ray/plane intersection using the parametric equations --- 
exactly how I think it should be done.  It's also very good that you realized that you 
need two additional checks: 1) check whether the intersection is within a face, and 2) 
check whether the intersection is on the ray.

Now when you are implementing the ray-mesh intersection, the first check above becomes 
checking whether an intersection is inside a triangle or not; think about how to do that.  
You still need the second check of course.

Finally, out of curiosity are you familiar with Python and the numpy package?  Being 
able to code in C/C++ is very important and will serve you well, but I'd suggest using 
Python for this project because it can free you from dealing with low-level details and 
accelerate debugging, plus there are a ton of Python libraries that you can use for 
various purposes.

There are many formats a mesh can be stored, and you should google them.  It doesn't 
matter which mesh format you use, and you certainly don't need to implement the code 
that parses a particular format.  There are plenty of Python libraries that read a mesh 
file.  Use them.

Yuhao