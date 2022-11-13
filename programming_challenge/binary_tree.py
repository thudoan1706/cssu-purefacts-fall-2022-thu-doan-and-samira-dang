from __future__ import annotations

import random
from typing import Any, Optional
import math
import csv


class BinarySearchTree:
    """Binary Search Tree class.

    This class represents a binary tree satisfying the Binary Search Tree
    property: for every item, its value is >= all items stored in its left
    subtree, and <= all items stored in its right subtree.
    """
    # === Private Attributes ===
    # The item stored at the root of the tree, or None if the tree is empty.
    _root: Optional[Any]
    # The left subtree, or None if the tree is empty.
    _left: Optional[BinarySearchTree]
    # The right subtree, or None if the tree is empty.
    _right: Optional[BinarySearchTree]

    # === Representation Invariants ===
    #  - If self._root is None, then so are self._left and self._right.
    #    This represents an empty BST.
    #  - If self._root is not None, then self._left and self._right
    #    are BinarySearchTrees.
    #  - (BST Property) If self is not empty, then
    #    all items in self._left are <= self._root, and
    #    all items in self._right are >= self._root.

    def __init__(self, root: Optional[Any]) -> None:
        """Initialize a new BST containing only the given root value.

        If <root> is None, initialize an empty tree.

        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self) -> bool:
        """Return whether this BST is empty.

        >>> bst = BinarySearchTree(None)
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(10)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    def construct_BST(self, value):
        """
        Construct the BST based on the value of the distance.
        Note: the value given will be unsorted since it has a higher chance of
              creating balanced tree O(nlog(n))
        """
        if self.is_empty():
            self._root = value
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)
        elif self._root >= value:
            self._left.construct_BST(value)
        elif self._root < value:
            self._right.construct_BST(value)

    def extract_max(self) -> float:
        """Return the maximum item stored in this tree.

        Precondition: this tree is *non-empty*.
        """
        if self._right.is_empty():
            max_item = self._root
            return max_item
        else:
            return self._right.extract_max()

    def extract_min(self) -> float:
        """Return the maximum item stored in this tree.

        Precondition: this tree is *non-empty*.
        """
        if self._left.is_empty():
            min_item = self._root
            return min_item
        else:
            return self._left.extract_min()

    def _calculate_radius(self, curr_lb, maxd, n) -> float:
        """
        curr_lb: current lower bound
        n: number of remaining representative points
        Calculate the radius to find N numbers of representative points
        """
        r = (maxd - curr_lb) / n
        return math.ceil(r)

    def _find_all_points(self, lb, up, r, max_d, N, num_point):
        """
        Return the represented point within the range lower bound and upper bound
        """
        if num_point == 0 or up > max_d:
            return
        lower = lb
        upper = up
        rad = r
        returned_point = self._items_in_range(lower, upper)
        while returned_point is None:
            # None means there are no point in the radius regions, then
            # we need to update next bound and smaller radius
            rad = self._calculate_radius(upper, max_d, num_point)
            lower = upper
            upper += rad
            returned_point = self._items_in_range(lower, upper)

        dictionary[N].append(returned_point)
        lower = upper
        upper += rad
        self._find_all_points(lower, upper, rad, max_d, N, num_point-1)


    def _items_in_range(self, lower_bound: float, upper_bound: float) -> Optional[float]:
        """
        Return the root value that is in the range
        Return None if there is none in the range
        """

        if self.is_empty():
            return None
        elif lower_bound <= self._root < upper_bound:
            return self._root
        elif self._root < lower_bound:
            return self._right._items_in_range(lower_bound, upper_bound)
        elif self._root > upper_bound:
            return self._left._items_in_range(lower_bound, upper_bound)
        return None


if __name__ == "__main__":
    with open(__file__) as sourcefile:
        print(sourcefile.read())

    N = [10, 25, 63, 159, 380]
    x_list = []
    y_list = []
    coordinates = []
    distance_points = {}
    with open('input.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        first_row = next(reader)
        # random coordinates
        rc = (int(first_row[0]), int(first_row[1]))
        for row in reader:
            c = (int(row[0]), int(row[1]))
            x, y = int(row[0]), int(row[1])
            x_list.append(x)
            y_list.append(y)
            coordinates.append((x,y))

    min_x = min(x_list)
    max_x = max(x_list)
    min_y = min(y_list)
    max_y = max(y_list)


    dictionary = {10: [], 25: [], 63: [], 159: [], 380: []}

    for n in N:
        list_points = []
        bst = BinarySearchTree(None)
        ramdom_point_x = random.randint(min_x, max_x)
        ramdom_point_y = random.randint(min_y, max_y)
        for coordinate in coordinates:
            distance = math.sqrt((coordinate[0] - ramdom_point_x)**2 + (coordinate[1] - ramdom_point_y)**2)
            if distance not in distance_points:
                distance_points[distance] = (coordinate)
            bst.construct_BST(distance)

        min_distance = bst.extract_min()
        max_distance = bst.extract_max()
        dictionary[n].append(min_distance)
        dictionary[n].append(max_distance)
        lowb = min_distance
        radius = bst._calculate_radius(lowb, max_distance, n)
        upb = lowb + radius
        bst._find_all_points(lowb, upb, radius, max_distance, n, n-2)

        coordinate_list =[]
        distance_of_n = dictionary[n]
        for distance in distance_of_n:
            coordinate_list.append(distance_points[distance])
        dictionary[n] = coordinate_list
        with open(f'{n}.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            f.write(f'length of output {len(dictionary[n])} \n')
            writer.writerow(dictionary[n])
