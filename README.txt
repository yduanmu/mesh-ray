python3 -m venv .gitignore/mesh-ray
source .gitignore/mesh-ray/bin/activate
deactivate

pip freeze > requirements.txt
pip install -r requirements.txt

stl2bin your_ascii_stl_file.stl new_binary_stl_file.stl
stl2ascii your_binary_stl_file.stl new_ascii_stl_file.stl
stl your_ascii_stl_file.stl new_binary_stl_file.stl


Algorithm:
1. Set up half-edge data structure (start, end, next, twin). Assumes manifold.

2. Check for the nearest vertex (point) to the origin of the ray. I used the
    k-d tree search and used squared distances to avoid calculating square roots.
    a. If the origin is equidistant between 2 and only 2 points, then it's at
        an edge. Only ray DIRECTION matters. Use the ray direction rather than
        the origin when doing half-edge traversing and guessing.
    b. If the origin is equidistant between 3 points, then we know for sure
        the closest plane. Skip all half-edge traversing and guessing.

3. Traverse the triangle fan of that vertex and find the plane equations for each.

4. Find the distance between each traversed plane and the origin of the ray. only
    remember the plane with the shortest distance.
    a. Here, I attempted to optimize the algorithm. I imagined that making
        multiple calculations per an arbitrarily large amount of planes (need to 
        find both plane equation and distance between point and plane) would be 
        terribly inefficient. I assumed that this would be inefficient enough that,
        even if there would be more vertices to compare than point-plane distances, 
        a NNS of the vertices would still be more optimal.

5. Find the parametric equation of the line containing the ray using two points 
    (ray origin and ray direction).

6. Calculate the point of intersection of the nearest plane and that line using the 
    plane equation and parametric equation of the line.

7. Check whether the intersection is within a triangle face.

8. Check whether the intersection is on the ray using the dot product of the 
    vectors origin->intersection and origin->direction

9. If valid, return the point of intersection and index of the face that contains it.


Limitations:
- The triangular mesh must be manifold.



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