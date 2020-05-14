from index import BPlusTreeIndex,printTree

class Table:        
    def __init__(self,file_name,table_meta):
        self.file_name=file_name
        self.file=open(file_name,"a+")
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


    def insert(self,data):
        buffer=''
        for field in self.fields:
            buffer+=data[field]
            buffer+='|'
        cn=len(buffer)
        buffer+=('|'*(45-cn))
        buffer+='\n'
        self.file.seek(0,2)
        rrn=self.file.tell()
        print(rrn)
        self.file.write(buffer)
        self.file.flush()
        self.index.tree.insert(data[self.primary_key],rrn)

    


    def search(self,key):
        rrn=self.index.tree.find(key)
        self.file.seek(int(rrn),0)
        return self.file.readline()
         
     

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
    print(an.search("boruto"))
main()