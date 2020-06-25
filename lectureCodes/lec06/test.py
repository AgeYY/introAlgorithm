#import bst
#import avl
import rkt

keys = ['3', '2', '0', '7', '1', '6']
#tree = avl.AVL()
rktree = rkt.RKT()
for key in keys:
    rktree.insert(key)
print(rktree)
print(rktree.find('3').gamma)
print(rktree.rank('7'))
print(rktree.count('0', '7'))
print(rktree.list('6', '7'))
