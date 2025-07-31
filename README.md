AVLTree implementation with pretty print and built-in search for k-th element
---

To my surprise, I couldn't find on the Internet any implementation of AVLTree with a nice tree visualization. So I've decided to do it (and support of k-th statistics) myself. I used as a base the following [implementation](https://github.com/pgrafov/python-avl-tree/blob/master/pyavltree.py). Also for a complete understanding of all rotations and other operations, I advise reader to become familiar with the following [article](https://www.geeksforgeeks.org/avl-tree-set-1-insertion/).

# 📦 Installation
```bash
git clone https://github.com/zinchse/AVLTree
cd AVLTree
pip install sortedcontainers
python3 test.py
```

# 🧩 Interface

## 1. Basics
```python3
>>> from AVLTree import AVLTree
>>> tree = AVLTree([1,2,3,5,6])
>>> print(tree)
        2       
       / \        
      /   \       
     /     \      
    1       5   
           / \      
          3   6 

>>> tree.insert(4)
>>> print(tree)
        3       
       / \        
      /   \       
     /     \      
    2       5   
   /       / \      
  1       4   6 

>>> tree.remove(3)
>>> print(tree)
        4       
       / \        
      /   \       
     /     \      
    2       5   
   /         \      
  1           6 
```        

## 2. Search
```python3
>>> print(tree)
        4       
       / \        
      /   \       
     /     \      
    2       5   
   /         \      
  1           6 
>>> print(tree.findkth(2), type(tree.findkth(2)))
2 <class 'Node.Node'>
>>> print(tree.find(4), type(tree.findkth(4)))
4 <class 'Node.Node'>
>>> print(tree.find(-1), type(tree.find(-1)))
None <class 'NoneType'>       
```                

## 3. Traversal
```python3
>>> print(tree)
        4       
       / \        
      /   \       
     /     \      
    2       5   
   /         \      
  1           6 
>>> # traversal_type: 0=preorder, 1=inorder, 2=postorder
>>> print(tree.as_list(traversal_type=0))
[4, 2, 1, 5, 6]
>>> print(tree.as_list(traversal_type=1))
[1, 2, 4, 5, 6]
>>> print(tree.as_list(traversal_type=2))
[1, 2, 6, 5, 4]
```        

# 🗂️ File structure

```
+-- Node.py/ contains node implementation
+-- AVLTree.py/ contains an implementation of the AVLTree class based on the Node
+-- test.py/ is simple check of work of search of kth statistics 
and maintenance of height of the order of a logarithm
```
