from index import BPlusTreeIndex,printTree

class Table:        
    def __init__(self,file_name,table_meta):
        self.name=table_meta["name"]
        self.file_name=file_name
        self.file=open(file_name,"r+")
        self.fields=table_meta["fields"]
        self.index_file_name=table_meta["index_file_name"]
        self.index=BPlusTreeIndex(self.index_file_name)
        self.primary_key=table_meta["primary_key"]
    
    def unpack_display(self):
        try:
            fhand = open('sample.txt','r')
        except:
            print('File cannot be opened:', "sample.txt")
            exit()
        fl =fhand.readlines()
        for x in fl:
            print(x)
        fhand.close()


    def pack(self,data):
        buffer=''
        for field in self.fields:
            buffer+=data[field]
            buffer+='|'
        cn=len(buffer)
        buffer+=('|'*(45-cn))
        buffer+='\n'
        return buffer


    def insert(self,data):
        if (self.index.tree.find(data[self.primary_key])) == -1:
            self.file.seek(0,2)
            rrn=self.file.tell()
            print(rrn)
            self.file.write(self.pack(data))
            self.file.flush()
            self.index.tree.insert(data[self.primary_key],rrn)
            return True
        return False

    
    def unpack(self,data):
        items=data.split('|')
        packet={}
        for i,item in enumerate(self.fields):
            packet[item]=items[i]
        return packet


    def update(self,key,data):
        rrn=self.index.tree.find(key)
        if rrn==-1:
            return False
        self.file.seek(int(rrn),0)
        self.file.write(self.pack(data))
        self.file.flush()
        return True
        
    def delete(self,key):
        rrn=self.index.tree.find(key)
        print(rrn)
        if rrn==-1:
            return False
        self.file.seek(rrn,0)
        self.file.write("*")
        self.file.flush()
        return True
        
    def search(self,key):
        rrn=self.index.tree.find(key)
        if rrn==-1:
            return False
        self.file.seek(int(rrn),0)
        data=self.file.readline()
        print(data)
        return self.unpack(data)
              

def main():
    anime_meta={
        "name":"anime",
        "fields":[
            "name",
            "genre",
            "author"
        ],
        "index_file_name":"index.txt",
        "primary_key":"name"
    }
    an=Table("anime.txt",anime_meta)
    an.insert({"name":"naruto","genre":"shonen","author":"masashi"})
    an.insert({"name":"boruto","genre":"shonen","author":"masashi"})
    an.insert({"name":"berserk","genre":"gore","author":"xyz"})
    printTree(an.index.tree)
    
    print(an.search("berserk"))
    
    an.update("boruto",{"name":"deathnote","genre":"gore","author":"xyzq"})
    an.delete("naruto")
main()
