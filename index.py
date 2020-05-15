from helpers import *

def unpack_index(record):
    return tuple(record.split(',',))


class ISAM:
    
    def __init__(self,index_file_name):
        self.target=open(index_file_name,"r")
        self.tree=BplusTree(8)
        with open(index_file_name, 'r') as f:
            for line in f:
                record=unpack_index(line)
                self.tree.insert(*record)
        printTree(self.tree)

def main():
    index=ISAM("index.txt")
    print(index.tree.find("naruto"))
    print(index.tree.find("4"))
    print(index.tree.find("7"))
    

if __name__=="__main__":
    main()
