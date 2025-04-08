'''
The main issue with this k-d tree is that it partitions incorrectly. It
partitions at the median's index in the previous dimension when it should
be partitioning at the median's index in the current dimension (lines 72-79).
'''

class K3DTree_Node: #K3D: 3-d tree (k-d tree)
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.dim = None
        self.val = None

class Sorted_Points:
    def __init__(self, unsorted_list=None, sorted_x_list=None, sorted_y_list = None, sorted_z_list=None):
        self.unsorted_list = unsorted_list

        if sorted_x_list is None:
            self.sorted_x_list = self.sort_points_list(unsorted_list, 0)
        else:
            self.sorted_x_list = sorted_x_list
        
        if sorted_y_list is None:
            self.sorted_y_list = self.sort_points_list(unsorted_list, 1)
        else:
            self.sorted_y_list = sorted_y_list
        
        if sorted_z_list is None:
            self.sorted_z_list = self.sort_points_list(unsorted_list, 2)
        else:
            self.sorted_z_list = sorted_z_list

    #given a point list, sorts based on dimension and returns sorted list
    def sort_points_list(self, point_list, dim):
        np_list = np.array(point_list)
        return np_list[np_list[:, dim].argsort()] #dim 0=x, 1=y, 2=z

#given a sorted point list, returns the value of the median
def choose_median(sorted_point_list):
    if len(sorted_point_list) == 2 or len(sorted_point_list) == 1:
        return sorted_point_list[0]
    else:
        return sorted_point_list[len(sorted_point_list)//2]

#given a set of Sorted_Points, node, and depth, recursively makes k-d tree
def make_K3DTree(sorted_points, node, depth):
    #choose the dimension of this level
    dim = depth % 3 #dim 0=x, 1=y, 2=z
    node.dim = dim

    #set current node value
    if dim == 0:
        sorted_dim_list = sorted_points.sorted_x_list
    elif dim == 1:
        sorted_dim_list = sorted_points.sorted_y_list
    else:
        sorted_dim_list = sorted_points.sorted_z_list
    median = choose_median(sorted_dim_list)
    node.val = median

    #recursively make k-d tree
    if len(sorted_dim_list) <= 1: #leaf
        return node
    elif len(sorted_dim_list) == 2:
        node.right_child = K3DTree_Node()
        node.right_child.val = sorted_dim_list[1]
        node.right_child.dim = (depth+1)%3
        return node
    else: #left and right children
        median_index = len(sorted_dim_list)//2
        #before median
        before_points = Sorted_Points(sorted_x_list=sorted_points.sorted_x_list[:median_index, 0:].copy(),
                                      sorted_y_list=sorted_points.sorted_y_list[:median_index, 0:].copy(),
                                      sorted_z_list=sorted_points.sorted_z_list[:median_index, 0:].copy())

        #after median
        after_points = Sorted_Points(sorted_x_list=sorted_points.sorted_x_list[median_index+1:, 0:].copy(),
                                     sorted_y_list=sorted_points.sorted_y_list[median_index+1:, 0:].copy(),
                                     sorted_z_list=sorted_points.sorted_z_list[median_index+1:, 0:].copy())

        node.left_child = make_K3DTree(before_points, K3DTree_Node(), depth+1)
        node.right_child = make_K3DTree(after_points, K3DTree_Node(), depth+1)
        return node

def preorder_K3DTree(node, indent=0):
    if node:
        print(" " * indent, node.val, " ", node.dim)
        preorder_K3DTree(node.left_child, indent+4)
        preorder_K3DTree(node.right_child, indent+4)