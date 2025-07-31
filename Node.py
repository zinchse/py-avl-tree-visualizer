from typing import Optional, TypeAlias

Key: "TypeAlias" = "int"


class Node:
    def __init__(self, key: "Key"):
        self.key: "Key" = key
        self.parent: "Optional[Node]" = None
        self.rightChild: "Optional[Node]" = None
        self.leftChild: "Optional[Node]" = None
        self.height: "int" = 0
        self.size: "int" = 1

    def __str__(self) -> "str":
        return str(self.key)

    def is_leaf(self) -> "bool":
        return self.height == 0

    def max_children_height(self) -> "int":
        if self.leftChild and self.rightChild:
            return max(self.leftChild.height, self.rightChild.height)
        elif self.leftChild:
            return self.leftChild.height
        elif self.rightChild:
            return self.rightChild.height
        else:
            return -1

    def balance(self) -> "int":
        return (self.leftChild.height if self.leftChild else -1) - (self.rightChild.height if self.rightChild else -1)
