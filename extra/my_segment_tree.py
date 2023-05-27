"""My implementation of segment trees and their min and sum variants, mostly for learning.
My code is probably not as efficient as the original so I'm not going to use it."""
from typing import Callable
class SegmentTree:
    def __init__(self, max_size:int, operation:Callable, neutral_value:float):
        """
        Implement segment tree.

        # Parameters 
        max_size: max n. of leaves (or size of array) Must be a power of two.
        operation: operation that iterates from leaves to root, taking 2 siblings input.
        neutral_value: a value that's neutral to the operation. eg: sum -> 0, min -> inf
        """
        # check if positive and power of two
        assert (max_size > 0 and max_size & (max_size - 1) == 0)
        ''' 
        why does this work?! well see this:
        >>> as_b = lambda n: "{:08b}".format(n)
        >>> as_b(35)
        '00100011'
        >>> as_b(35-1)
        '00100010'
        >>> as_b(35&35-1)
        '00100010'
        >>> as_b(35-1)
        >>> as_b(32) 
        '00100000'
        # note how, only for numbers that are powers of two, you
        # get a subtraction with the following pattern:
        >>> as_b(32-1)    
        '00011111'
        # so we can exploit that to know what numbers are ^2:
        >>> as_b(32&32-1) 
        '00000000'
        '''

        # note that max_size refers to the n. of leaves
        self.max_size = max_size
        self.nodes = [neutral_value for _ in range(2 * max_size)]
        self.operation = operation


    def _navigate(
        self, left, right, node, node_min, node_max,
    ):
        """
        The function that navigates up the tree. You can visualize each step
        as moving to children nodes (or climbing down the tree when returning).
        So at every time-step, there is a link with some `node`.

        # Parameters
        left: left-end to check for (minimum)
        right: right-end to check for (maximum)
        node: current node index, initialized at 1 for root node
        node_min and node_max correspond to the "span" of some parent node's branches.
        A node always has these 2 values that are to remain UNCHANGED for that tree structure.
        However, we calculate them on-demand # TODO find right word for this 
        node_min:  left end span of childrens of a node
        node_max:  right end span of childrens of a node
        
        NOTE: you may choose to index nodes starting at 0 or 1, either is fine. If you chose 0 you could
        branch from parent X to children Y, Z:
        Y = X*2+1
        Z = X*2+2
        and return the node:
        return self.nodes[node] # no need to correct
        """
        # print('---')
        # print('start', left)
        # print('end', right)
        # print('node', node)
        # print('node_start', node_min)
        # print('node_end', node_max)

        # we've reached the "ideal" node; return it
        if node_min == left and node_max == right:
            # print('return')
            return self.nodes[node]
        
        # miximum
        mid = (node_min + node_max) // 2

        if mid>=right:
            # left branch
            # print('left branch')
            return self._navigate(left, right, node*2, node_min, mid)
        if left>mid:
            # print('right branch')
            # right branch
            return self._navigate(left, right, node*2+1, mid+1, node_max)
        if left<=mid<right:
            # split, we'll need to apply operation between the 2 returning nodes
            # print('split')
            return self.operation(
                # order doesn't matter since operation MUST be commutative (aka order property)
                # left branch
                self._navigate(left, mid, node*2, node_min, mid),
                # right branch
                self._navigate(mid+1, right, node*2+1, mid+1, node_max)
            )

    def reduce(self, start=0, end=None):
        """return node or operation for query parameters [start, end]"""
        if end is None:
            end = self.max_size
        if end < 0:
            end += self.max_size

        return self._navigate(left=start, right=end, node=1, node_min=0, node_max=self.max_size-1)

            
    def __setitem__(self, idx, val):
        """Start from a leaf and recursively update down to the root."""
        # NOTE: we leave self.nodes[0] to be EMPTY, that is, we start indexing at 1,
        # so that it's easier to visualize.

        # leaf node
        node = self.max_size + idx
        self.nodes[node] = val
        # nodes: 3, 4 -> 
        # work down towards the root (from a upside-down perspective)
        node //= 2
        while node != 0:
            # alias
            parent_node = node
            sibling_node_left = node*2
            sibling_node_right = node*2+1
            self.nodes[parent_node] = self.operation(
                self.nodes[sibling_node_left],
                self.nodes[sibling_node_right]
            )
            node //= 2

    def __getitem__(self, idx):
        return self.nodes[self.capacity + idx]

class MinSegmentTree(SegmentTree):
    def __init__(self, capacity):
        super().__init__(
            max_size=capacity,
            operation=min,
            neutral_value=float('inf')
            )
    
    def min(self, start=0, end=None):
        return super().reduce(start, end)

class SumSegmentTree(SegmentTree):
    def __init(self, capacity):
        super().__init__(
            max_size=capacity,
            operation=operator.add,
            neutral_value=0.0
        )    
        pass

    def find_prefixsum_idx(self, prefixsum):
        node = 1
        assert 0 <= prefixsum < self.sum()
        assert 0 <= prefixsum < self.sum()
        # while not a leaf node 
        while node < self.max_size:
            curr_node_val = self.nodes[node]
            if curr_node_val == prefixsum:
                # we found the branch, now just keep going right until we hit leaf
                node = (node * 2) + 1
            if curr_node_val > prefixsum:
                # current value too high, branch left
                node *= 2
            if curr_node_val < prefixsum:
                # we "undershot" it, go to sibling's left branch
                # we go to its left branch because we know our sibling's total overshoots,
                # after all we already checked the parent!
                prefixsum -= self.nodes[node]
                node = (node + 1) * 2
            
        return node
    # TODO: implement SumSegmentTree
