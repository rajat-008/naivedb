import json
import os
from helpers import (
    MissingDataException,
    FileMissing,
    NaiveDBException
) 

from index import ISAM

class Table:        
    def __init__(self,table_meta,db_loc):
        self.name=table_meta["name"]
        self.loc=db_loc
        self.file_name=table_meta["file_name"]
        self.file=open(self.loc+self.file_name,"r+")
        self.fields=table_meta["fields"]
        self.index_file_name=db_loc+table_meta["index_file_name"]
        self.index=ISAM(self.index_file_name)
        self.primary_key=table_meta["primary_key"]

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
            self.index.write(data[self.primary_key],rrn)
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



class NaiveDB:

    @staticmethod
    def create_db(name='database',loc='./',tables=None,):
        if not tables:
            raise MissingDataException("Database without tables cannot be created.")
        for table in tables:
            table["file_name"]=table["name"]+".txt"
            table["index_file_name"]=table["name"]+"_index.txt"
        db_meta={
            "name":name,
            "tables":tables,
            "db_loc":loc
        }
        db_path=os.path.join(loc,"naivedb")
        os.umask(0)
        os.mkdir(db_path)
        with open(loc+"naivedb/meta.json", 'w') as outfile:
            json.dump(db_meta,outfile)
        for table in tables:
            open("naivedb/"+table["name"]+".txt","x").close()
            open("naivedb/"+table["name"]+"_index.txt","x").close()
        return 

    def __init__(self,db_loc):
        try:
            with open(db_loc+"meta.json","r") as meta_file:
                self.meta_data=json.load(meta_file)
        except FileNotFoundError:
            raise NaiveDBException("DataBase not found at the location")
        for table in self.meta_data["tables"]:
            table_obj=Table(table,db_loc)
            setattr(self,table["name"],table_obj)
    
def main():
    db=NaiveDB("naivedb/")
    print(db.meta_data)
    print(db.anime.insert({"name":"boruto","author":"masashi","genre":"shonen"}))

hello=[{"name":"anime","fields": ["name", "author", "genre"], "primary_key": "name"},{"name":"cast","fields": ["name", "anime", "gender"], "primary_key": "name"}]
if __name__ == "__main__":
    main()