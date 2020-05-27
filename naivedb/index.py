from .helpers import BplusTree

def unpack_index(record):
    return tuple(record.split(',',))

def pack_index(key,value):
    return key+','+str(value)+'\n'

class ISAM(BplusTree):
    
    def __init__(self,index_file_name):
        super().__init__(8)
        self.file_name=index_file_name
        self.target=open(index_file_name,"r")
        with open(index_file_name, 'r') as f:
            for line in f:
                record=unpack_index(line)
                if record[0][0]=="*":
                    continue
                super().insert(*record)    


    def insert(self,key,value):
        super().insert(key,value)
        file=open(self.file_name,"a")
        file.write(pack_index(key,value))
        file.close()

    def delete(self,key,rrn):
        file=open(self.file_name,"r+")
        irrn=file.tell()
        line=file.readline()
        while line:
            ikey,_=unpack_index(line)
            if ikey==key:
                break
            irrn=file.tell()
            line=file.readline()
            
        super().delete(key,rrn)
        file.seek(int(irrn),0)
        file.write("*")
        file.close()

    



def main():
    index=ISAM("index.txt")
    print(index.tree.find("naruto"))
    print(index.tree.find("4"))
    print(index.tree.find("7"))
    

if __name__=="__main__":
    main()
