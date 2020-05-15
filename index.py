from helpers import *

def unpack_index(record):
    return tuple(record.split(',',))

def pack_index(key,value):
    return key+','+str(value)+'\n'

class ISAM:
    
    def __init__(self,index_file_name):
        self.file_name=index_file_name
        self.target=open(index_file_name,"r")
        self.tree=BplusTree(8)
        with open(index_file_name, 'r') as f:
            for line in f:
                record=unpack_index(line)
                self.tree.insert(*record)
        printTree(self.tree)
    
    def write(self,key,value):
        self.tree.insert(key,value)
        file=open(self.file_name,"a")
        file.write(pack_index(key,value))
        file.close()



def main():
    index=ISAM("index.txt")
    print(index.tree.find("naruto"))
    print(index.tree.find("4"))
    print(index.tree.find("7"))
    

if __name__=="__main__":
    main()
