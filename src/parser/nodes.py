from __future__ import annotations
from abc import ABC, abstractmethod
import datetime
from typing import List

class NodeError(Exception):
    """Error for the nodes"""
    pass

class Node(ABC):
    """Class for a basic node for the AST"""
    def __init__(self):
        self.children: List[Node] = []
    
    def addChild(self, child: Node):
        """Method to add a child to the node"""
        if not isinstance(child, Node):
            raise NodeError("Node.addChild() child is not a Node")
        self.children.append(child)

    def removeChild(self, pos: int = 0):
        if not len(self.children) >= pos + 1:
            raise IndexError("Node.removeChild() pos is larger than self.children")
        del self.children[pos]

    @abstractmethod
    def build(self):
        """Method to build the Node output"""
        pass

class AST:
    """Class for something resembling an AST, but not really"""
    def __init__(self, root: Node):
        self.root: Node = root

class TimeNode(Node):
    """Class for storing the Time data"""
    def __init__(self, contents: datetime.datetime):
        super().__init__()
        self.contents: datetime.datetime = contents
    
    def build(self):
        """Method to build the Time Node output"""
        pass

class ActivityNode(Node):
    """Class for storing the Activity data"""
    def __init__(self, contents: str):
        super().__init__()
        self.contents: str = contents
    
    def build(self):
        """Method to build the Activity Node output"""
        pass

class CommentNode(Node):
    """Class for storing the Comment data"""
    def __init__(self, contents: str):
        super().__init__()
        self.contents: str = contents
    
    def build(self):
        """Method to build the Comment Node output"""
        pass

