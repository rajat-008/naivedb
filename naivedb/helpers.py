class NaiveDBException(Exception):
    def __init__(self,msg):
        self.msg=msg

class MissingDataException(NaiveDBException):
    def __init__(self,loc):
        self.msg="database not found at location"+loc
class FileMissing(NaiveDBException):
    pass

import math


class Node:
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.values = []
        self.nextKey = None
        self.parent = None
        self.is_leaf = False

    def insertINLeaf(self, leaf, key, value):
        if (self.keys):
            temp1 = self.keys
            for i in range(len(temp1)):
                if (key == temp1[i]):
                    self.values[i].append(value)
                    break
                elif (key < temp1[i]):
                    self.keys = self.keys[:i] + [key] + self.keys[i:]
                    self.values = self.values[:i] + [[value]] + self.values[i:]
                    break
                elif (i + 1 == len(temp1)):
                    self.keys.append(key)
                    self.values.append([value])
                    break
        else:
            self.keys = [key]
            self.values = [[value]]


class BplusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.is_leaf = True

    def insert(self, key, value):
        key = str(key)
        old_node = self.search(key)
        old_node.insertINLeaf(old_node, key, value)

        if (len(old_node.keys) == old_node.order):
            node1 = Node(old_node.order)
            node1.is_leaf = True
            node1.parent = old_node.parent
            mid = int(math.ceil(old_node.order / 2)) - 1
            node1.keys = old_node.keys[mid + 1:]
            node1.values = old_node.values[mid + 1:]
            node1.nextKey = old_node.nextKey
            old_node.keys = old_node.keys[:mid + 1]
            old_node.values = old_node.values[:mid + 1]
            old_node.nextKey = node1
            self.insertINParent(old_node, node1.keys[0], node1)

    def search(self, key):
        current_node = self.root
        while(current_node.is_leaf is False):
            temp2 = current_node.keys
            for i in range(len(temp2)):
                if (key == temp2[i]):
                    current_node = current_node.values[i + 1]
                    break
                elif (key < temp2[i]):
                    current_node = current_node.values[i]
                    break
                elif (i + 1 == len(current_node.keys)):
                    current_node = current_node.values[i + 1]
                    break
        return current_node

    def find(self, key):
        l = self.search(key)
        for i, item in enumerate(l.keys):
            if item == key:
                return l.values[i][0]
        return -1

    def insertINParent(self, n, key, ndash):
        if (self.root == n):
            rootNode = Node(n.order)
            rootNode.keys = [key]
            rootNode.values = [n, ndash]
            self.root = rootNode
            n.parent = rootNode
            ndash.parent = rootNode
            return

        parentNode = n.parent
        temp3 = parentNode.values
        for i in range(len(temp3)):
            if (temp3[i] == n):
                parentNode.keys = parentNode.keys[:i] + \
                    [key] + parentNode.keys[i:]
                parentNode.values = parentNode.values[:i +
                                                  1] + [ndash] + parentNode.values[i + 1:]
                if (len(parentNode.values) > parentNode.order):
                    parentdash = Node(parentNode.order)
                    parentdash.parent = parentNode.parent
                    mid = int(math.ceil(parentNode.order / 2)) - 1
                    parentdash.keys = parentNode.keys[mid + 1:]
                    parentdash.values = parentNode.values[mid + 1:]
                    value_ = parentNode.keys[mid]
                    if (mid == 0):
                        parentNode.keys = parentNode.keys[:mid + 1]
                    else:
                        parentNode.keys = parentNode.keys[:mid]
                    parentNode.values = parentNode.values[:mid + 1]
                    for j in parentNode.values:
                        j.parent = parentNode
                    for j in parentdash.values:
                        j.parent = parentdash
                    self.insertINParent(parentNode, value_, parentdash)

    def delete(self, key, value):
        node_ = self.search(key)
        temp = 0
        for i, item in enumerate(node_.keys):
            if item == key:
                temp = 1

                if value in node_.values[i]:
                    if len(node_.values[i]) > 1:
                        node_.values[i].pop(node_.values[i].index(value))
                    elif node_ == self.root:
                        node_.keys.pop(i)
                        node_.values.pop(i)
                    else:
                        node_.values[i].pop(node_.values[i].index(value))
                        del node_.values[i]
                        node_.keys.pop(node_.keys.index(key))
                        self.deleteEntry(node_, key, value)
                else:
                    print("key not in value")
                    return
        if temp == 0:
            print("key not in Tree")
            return

    def deleteEntry(self, node_, key, value):

        if not node_.is_leaf:
            for i, item in enumerate(node_.values):
                if item == value:
                    node_.values.pop(i)
                    break
            for i, item in enumerate(node_.keys):
                if item == key:
                    node_.keys.pop(i)
                    break

        if self.root == node_ and len(node_.values) == 1:
            self.root = node_.values[0]
            node_.values[0].parent = None
            del node_
            return
        elif (len(node_.values) < int(math.ceil(node_.order / 2)) and node_.is_leaf is False) or (len(node_.keys) < int(math.ceil((node_.order - 1) / 2)) and node_.is_leaf is True):

            is_predecessor = 0
            parentNode = node_.parent
            PrevNode = -1
            NextNode = -1
            PrevK = -1
            PostK = -1
            for i, item in enumerate(parentNode.values):

                if item == node_:
                    if i > 0:
                        PrevNode = parentNode.values[i - 1]
                        PrevK = parentNode.keys[i - 1]

                    if i < len(parentNode.values) - 1:
                        NextNode = parentNode.values[i + 1]
                        PostK = parentNode.keys[i]

            if PrevNode == -1:
                ndash = NextNode
                value_ = PostK
            elif NextNode == -1:
                is_predecessor = 1
                ndash = PrevNode
                value_ = PrevK
            else:
                if len(node_.keys) + len(NextNode.keys) < node_.order:
                    ndash = NextNode
                    value_ = PostK
                else:
                    is_predecessor = 1
                    ndash = PrevNode
                    value_ = PrevK

            if len(node_.keys) + len(ndash.keys) < node_.order:
                if is_predecessor == 0:
                    node_, ndash = ndash, node_
                ndash.values += node_.values
                if not node_.is_leaf:
                    ndash.keys.append(value_)
                else:
                    ndash.nextKey = node_.nextKey
                ndash.keys += node_.keys

                if not ndash.is_leaf:
                    for j in ndash.values:
                        j.parent = ndash

                self.deleteEntry(node_.parent, value_, node_)
                del node_
            else:
                if is_predecessor == 1:
                    if not node_.is_leaf:
                        ndashpm = ndash.values.pop(-1)
                        ndashkm_1 = ndash.keys.pop(-1)
                        node_.values = [ndashpm] + node_.values
                        node_.keys = [value_] + node_.keys
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.keys):
                            if item == value_:
                                p.keys[i] = ndashkm_1
                                break
                    else:
                        ndashpm = ndash.values.pop(-1)
                        ndashkm = ndash.keys.pop(-1)
                        node_.values = [ndashpm] + node_.values
                        node_.keys = [ndashkm] + node_.keys
                        parentNode = node_.parent
                        for i, item in enumerate(p.keys):
                            if item == value_:
                                parentNode.keys[i] = ndashkm
                                break
                else:
                    if not node_.is_leaf:
                        ndashp0 = ndash.values.pop(0)
                        ndashk0 = ndash.keys.pop(0)
                        node_.values = node_.values + [ndashp0]
                        node_.keys = node_.keys + [value_]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.keys):
                            if item == value_:
                                parentNode.keys[i] = ndashk0
                                break
                    else:
                        ndashp0 = ndash.values.pop(0)
                        ndashk0 = ndash.keys.pop(0)
                        node_.values = node_.values + [ndashp0]
                        node_.keys = node_.keys + [ndashk0]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.keys):
                            if item == value_:
                                parentNode.keys[i] = ndash.keys[0]
                                break

                if not ndash.is_leaf:
                    for j in ndash.values:
                        j.parent = ndash
                if not node_.is_leaf:
                    for j in node_.values:
                        j.parent = node_
                if not parentNode.is_leaf:
                    for j in parentNode.values:
                        j.parent = parentNode


def printTree(tree):
    lst = [tree.root]
    level = [0]
    leaf = None
    flag = 0
    lev_leaf = 0

    node1 = Node(str(level[0]) + str(tree.root.keys))
    print("printing tree")
    while (len(lst) != 0):
        x = lst.pop(0)
        lev = level.pop(0)
        if (x.is_leaf is False):
            for i, item in enumerate(x.values):
                print(item.keys,item.values)
        else:
            for i, item in enumerate(x.values):
                print(x.keys[i],item)
            if (flag == 0):
                lev_leaf = lev
                leaf = x
                flag = 1
    print("done printing tree")