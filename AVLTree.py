from Node import Node, Key
from typing import List, Optional


class AVLTree:
    def __init__(self, vals: "Optional[List[Key]]" = None):
        if not vals:
            vals = []
        self.rootNode = None
        self.elements_count = 0
        self.rebalance_count = 0
        for v in vals:
            self.insert(v)

    def height(self) -> "int":
        if self.rootNode:
            return self.rootNode.height
        else:
            return -1

    def find_in_subtree(self, key: "Key", node: "Optional[Node]") -> "Optional[Node]":
        if node is None:
            return None
        elif key < node.key:
            return self.find_in_subtree(key, node.leftChild)
        elif key > node.key:
            return self.find_in_subtree(key, node.rightChild)
        else:
            return node

    def find(self, key: "Key", node: "Optional[Node]" = None) -> "Optional[Node]":
        if node is None:
            node = self.rootNode
        return self.find_in_subtree(key, node)

    def recompute_heights(self, startNode: "Optional[Node]") -> "None":
        changed = True
        node = startNode
        while node and changed:
            old_height = node.height
            node.height = node.max_children_height() + 1 if (node.rightChild or node.leftChild) else 0
            changed = node.height != old_height
            node = node.parent

    def find_biggest(self, start_node: "Node") -> "Node":
        node = start_node
        while node.rightChild:
            node = node.rightChild
        return node

    def find_smallest(self, start_node: "Node") -> "Node":
        node = start_node
        while node.leftChild:
            node = node.leftChild
        return node

    def as_list(self, traversal_type: "int" = 1) -> "List[Key]":
        """Returns keys of the tree in the specified traversal order.

        Args:
            traversal_type (int): Type of traversal: 0=preorder, 1=inorder, 2=postorder.

        Returns:
            list[Key]: List of keys in the specified traversal order.
        """
        if not self.rootNode:
            return []
        elif traversal_type == 0:
            return self.preorder(self.rootNode)
        elif traversal_type == 1:
            return self.inorder(self.rootNode)
        elif traversal_type == 2:
            return self.postorder(self.rootNode)
        else:
            assert False, f"Wrong traversal type value {traversal_type}!"

    def preorder(self, node: "Optional[Node]", retlst: "Optional[List[Key]]" = None) -> "List[Key]":
        if retlst is None:
            retlst = []
        if node:
            retlst.append(node.key)
        if node and node.leftChild:
            retlst = self.preorder(node.leftChild, retlst)
        if node and node.rightChild:
            retlst = self.preorder(node.rightChild, retlst)
        return retlst

    def inorder(self, node: "Optional[Node]", retlst: "Optional[List[Key]]" = None) -> "List[Key]":
        if retlst is None:
            retlst = []
        if node and node.leftChild:
            retlst = self.inorder(node.leftChild, retlst)
        if node:
            retlst.append(node.key)
        if node and node.rightChild:
            retlst = self.inorder(node.rightChild, retlst)
        return retlst

    def postorder(self, node: "Optional[Node]", retlst: "Optional[List[Key]]" = None) -> "List[Key]":
        if retlst is None:
            retlst = []
        if node and node.leftChild:
            retlst = self.postorder(node.leftChild, retlst)
        if node and node.rightChild:
            retlst = self.postorder(node.rightChild, retlst)
        if node:
            retlst.append(node.key)
        return retlst

    def add_as_child(self, parent_node: "Node", child_node: "Node") -> "None":
        node_to_rebalance: "Optional[Node]" = None
        parent_node.size += 1

        if child_node.key < parent_node.key:
            if not parent_node.leftChild:
                parent_node.leftChild = child_node
                child_node.parent = parent_node
                if parent_node.height == 0:  # in this case tree's height could change
                    node = parent_node
                    while node:
                        node.height = node.max_children_height() + 1
                        if not node.balance() in [-1, 0, 1]:
                            node_to_rebalance = node
                            break
                        node = node.parent
            else:
                self.add_as_child(parent_node.leftChild, child_node)
        else:
            if not parent_node.rightChild:
                parent_node.rightChild = child_node
                child_node.parent = parent_node
                if parent_node.height == 0:  # in this case tree's height could change
                    node = parent_node
                    while node:
                        node.height = node.max_children_height() + 1
                        if not node.balance() in [-1, 0, 1]:
                            node_to_rebalance = node
                            break
                        node = node.parent
            else:
                self.add_as_child(parent_node.rightChild, child_node)

        if node_to_rebalance:
            self.rebalance(node_to_rebalance)

    def insert(self, key: "Key") -> "None":
        new_node = Node(key)
        if not self.rootNode:
            self.rootNode = new_node
            assert self.elements_count == 0, "Wrong elements_count"
            self.elements_count += 1
        elif not self.find(key):
            self.elements_count += 1
            self.add_as_child(self.rootNode, new_node)

    def remove_branch(self, node: "Node") -> "None":
        parent = node.parent
        if parent:
            if parent.leftChild == node:
                parent.leftChild = node.rightChild or node.leftChild
            else:
                parent.rightChild = node.rightChild or node.leftChild
        else:
            self.rootNode = node.rightChild or node.leftChild

        if node.leftChild:
            node.leftChild.parent = parent
        else:
            node.rightChild.parent = parent
        self.recompute_heights(parent)

        del node

        # rebalance
        node = parent
        while node:
            self.resize(node)
            if node.balance() not in (-1, 0, 1):
                self.rebalance(node)
            node = node.parent

    def remove_leaf(self, node: "Node") -> "None":
        parent = node.parent
        if parent:
            if parent.leftChild == node:
                parent.leftChild = None
            else:
                parent.rightChild = None
            self.recompute_heights(parent)
        else:
            self.rootNode = None
        del node

        # rebalance
        node = parent
        while node:
            self.resize(node)
            if not node.balance() in [-1, 0, 1]:
                self.rebalance(node)
            node = node.parent

    def remove(self, key: "Key") -> "None":
        node = self.find(key)
        if node:
            self.elements_count -= 1
            if node.is_leaf():
                self.remove_leaf(node)
            elif (bool(node.leftChild)) ^ (bool(node.rightChild)):
                self.remove_branch(node)
            else:
                self.swap_with_successor_and_remove(node)

    def swap_with_successor_and_remove(self, node: "Node") -> "None":
        successor = self.find_smallest(node.rightChild)
        self.swap_nodes(node, successor)
        if node.height == 0:
            self.remove_leaf(node)
        else:
            self.remove_branch(node)

    def swap_nodes(self, node1: "Node", node2: "Node") -> "None":
        parent1 = node1.parent
        leftChild1 = node1.leftChild
        rightChild1 = node1.rightChild
        parent2 = node2.parent
        leftChild2 = node2.leftChild
        rightChild2 = node2.rightChild

        node1.height, node2.height = node2.height, node1.height
        node1.size, node2.size = node2.size, node1.size

        if parent1:
            if parent1.leftChild == node1:
                parent1.leftChild = node2
            else:
                parent1.rightChild = node2
            node2.parent = parent1
        else:
            self.rootNode = node2
            node2.parent = None

        node2.leftChild = leftChild1
        leftChild1.parent = node2

        node1.leftChild = leftChild2
        node1.rightChild = rightChild2
        if rightChild2:
            rightChild2.parent = node1

        if not (parent2 == node1):
            node2.rightChild = rightChild1
            rightChild1.parent = node2

            parent2.leftChild = node1
            node1.parent = parent2
        else:
            node2.rightChild = node1
            node1.parent = node2

    def resize(self, node: "Node") -> "None":
        node.size = 1
        if node.rightChild:
            node.size += node.rightChild.size
        if node.leftChild:
            node.size += node.leftChild.size

    def rebalance(self, node_to_rebalance: "Node") -> "None":
        self.rebalance_count += 1
        A = node_to_rebalance
        F = A.parent
        if node_to_rebalance.balance() == -2:
            if node_to_rebalance.rightChild.balance() <= 0:
                # rebalance, case RRC
                B = A.rightChild
                C = B.rightChild
                A.rightChild = B.leftChild
                if A.rightChild:
                    A.rightChild.parent = A
                B.leftChild = A
                A.parent = B
                if F is None:
                    self.rootNode = B
                    self.rootNode.parent = None
                else:
                    if F.rightChild == A:
                        F.rightChild = B
                    else:
                        F.leftChild = B
                    B.parent = F
                self.recompute_heights(A)
                self.resize(A)
                self.resize(B)
                self.resize(C)
            else:
                # rebalance, case RLC
                B = A.rightChild
                C = B.leftChild
                B.leftChild = C.rightChild
                if B.leftChild:
                    B.leftChild.parent = B
                A.rightChild = C.leftChild
                if A.rightChild:
                    A.rightChild.parent = A
                C.rightChild = B
                B.parent = C
                C.leftChild = A
                A.parent = C
                if F is None:
                    self.rootNode = C
                    self.rootNode.parent = None
                else:
                    if F.rightChild == A:
                        F.rightChild = C
                    else:
                        F.leftChild = C
                    C.parent = F
                self.recompute_heights(A)
                self.recompute_heights(B)
                self.resize(A)
                self.resize(B)
                self.resize(C)

        else:
            if node_to_rebalance.leftChild.balance() >= 0:
                # rebalance, case LLC
                B = A.leftChild
                C = B.leftChild
                A.leftChild = B.rightChild
                if A.leftChild:
                    A.leftChild.parent = A
                B.rightChild = A
                A.parent = B
                if F is None:
                    self.rootNode = B
                    self.rootNode.parent = None
                else:
                    if F.rightChild == A:
                        F.rightChild = B
                    else:
                        F.leftChild = B
                    B.parent = F
                self.recompute_heights(A)
                self.resize(A)
                self.resize(C)
                self.resize(B)
            else:
                # rebalance, case LRC
                B = A.leftChild
                C = B.rightChild
                A.leftChild = C.rightChild
                if A.leftChild:
                    A.leftChild.parent = A
                B.rightChild = C.leftChild
                if B.rightChild:
                    B.rightChild.parent = B
                C.leftChild = B
                B.parent = C
                C.rightChild = A
                A.parent = C
                if F is None:
                    self.rootNode = C
                    self.rootNode.parent = None
                else:
                    if F.rightChild == A:
                        F.rightChild = C
                    else:
                        F.leftChild = C
                    C.parent = F
                self.recompute_heights(A)
                self.recompute_heights(B)
                self.resize(A)
                self.resize(B)
                self.resize(C)

    def findkth(self, k: "int", root: "Optional[Node]" = None) -> "Optional[Node]":
        if root is None:
            root = self.rootNode
        assert k <= root.size, "Error, k more then the size of BST"
        leftsize = 0 if root.leftChild is None else root.leftChild.size
        if leftsize >= k:
            return self.findkth(k, root.leftChild)

        elif leftsize == k - 1:
            return root
        else:
            return self.findkth(k - leftsize - 1, root.rightChild)

    def __str__(self, start_node: "Optional[Node]" = None) -> "str":
        if start_node == None:
            if not self.rootNode:
                return "*empty tree*"
            else:
                start_node = self.rootNode
        space_symbol = r" "
        spaces_count = 4 * 2 ** (self.rootNode.height)
        out_string = r""
        initial_spaces_string = space_symbol * spaces_count + "\n"
        if not start_node:
            return "Tree is empty!"
        height = 2 ** (self.rootNode.height)
        level = [start_node]

        while len([i for i in level if (not i is None)]) > 0:
            level_string = initial_spaces_string
            for i in range(len(level)):
                j = int((2 * i + 1) * spaces_count / (2 * len(level)))
                level_string = level_string[:j] + (str(level[i]) if level[i] else space_symbol) + level_string[j + 1 :]
            out_string += level_string

            # create next level
            level_next = []
            for i in level:
                level_next += [i.leftChild, i.rightChild] if i else [None, None]

            # add connection to the next nodes
            for w in range(height - 1):
                level_string = initial_spaces_string
                for i in range(len(level)):
                    if not level[i] is None:
                        shift = spaces_count // (2 * len(level))
                        j = (2 * i + 1) * shift
                        level_string = (
                            level_string[: j - w - 1]
                            + ("/" if level[i].leftChild else space_symbol)
                            + level_string[j - w :]
                        )
                        level_string = (
                            level_string[: j + w + 1]
                            + ("\\" if level[i].rightChild else space_symbol)
                            + level_string[j + w :]
                        )
                out_string += level_string
            height = height // 2
            level = level_next

        return out_string
