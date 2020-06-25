#!/usr/bin/env python
# A tree extends avl, which can quickly calculate 1. how many nodes between key l and h 2. list all nodes with keys between l and h. Please see the detail in Problem set 3, 6-006-fall-2011, MITOCW

import bst
import avl

def gamma(node):
    ''' the number of nodes of the subtree which rooted at node.'''
    if node is None:
        return 0
    else:
        return node.gamma

def update_gamma(node):
    node.gamma = gamma(node.left) + gamma(node.right) + 1

class RKT(avl.AVL):
    """
RankTree binary search tree implementation.
Supports insert, delete, find, find_min, next_larger, count_between, list_between each in O(lg n) time.
"""
    def left_rotate(self, x):
        y = x.right
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.right = y.left
        if x.right is not None:
            x.right.parent = x
        y.left = x
        x.parent = y
        avl.update_height(x)
        avl.update_height(y)
        update_gamma(x)
        update_gamma(y)

    def right_rotate(self, x):
        y = x.left
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.left = y.right
        if x.left is not None:
            x.left.parent = x
        y.right = x
        x.parent = y
        avl.update_height(x)
        avl.update_height(y)
        update_gamma(x)
        update_gamma(y)

    def rebalance(self, node):
        while node is not None:
            avl.update_height(node)
            update_gamma(node)
            if avl.height(node.left) >= 2 + avl.height(node.right):
                if avl.height(node.left.left) >= avl.height(node.left.right):
                    self.right_rotate(node)
                else:
                    self.left_rotate(node.left)
                    self.right_rotate(node)
            elif avl.height(node.right) >= 2 + avl.height(node.left):
                if avl.height(node.right.right) >= avl.height(node.right.left):
                    self.left_rotate(node)
                else:
                    self.right_rotate(node.right)
                    self.left_rotate(node)
            node = node.parent

    def rank(self, k):
        ''' find the rank of k in node.key in the whole tree'''
        r = 0
        node = self.root
        while node is not None:
            if k < node.key:
                node = node.left
            else:
                if node.left is not None:
                    r = r + 1 + node.left.gamma
                else:
                    r = r + 1
                if node.key == k:
                    return r
                node = node.right
        return r

    def count(self, l, h):
        ''' count how many nodes which have keys between l and h'''
        s = self.rank(h) - self.rank(l)
        if self.find(l):
            s = s + 1
        return s

    def list(self, l, h):
        '''list all keys between l and h'''
        lca = self._lca(l, h)
        result = []
        self._node_list(lca, l, h, result)
        return result

    def _node_list(self, node, l, h, result):
        if node is None:
            return 
        if l <= node.key and node.key <= h:
            result.append(node.key)
        if node.key >= l:
            self._node_list(node.left, l, h, result)
        if node.key <= h:
            self._node_list(node.right, l, h, result)

    def _lca(self, l, h):
        node = self.root
        while node is not None and (l > node.key or h < node.key):
            if l < node.key:
                node = node.left
            else:
                node = node.right
        return node
