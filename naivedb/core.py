import json
import os
import shutil
from .helpers import (
    MissingDataException,
    FileMissing,
    NaiveDBException,
    printTree
)

from .index import ISAM

class Table:        
    def __init__(self,table_meta,db_path):
        self.name=table_meta["name"]
        self.file_name=table_meta["file_name"]
        self.loc=os.path.join(db_path,self.file_name)
        self.file=open(self.loc,"r+")
        self.fields=table_meta["fields"]
        self.index_file_name=db_path+table_meta["index_file_name"]
        self.index=ISAM(self.index_file_name)
        self.primary_key=table_meta["primary_key"]

    def fetch_all(self):
        rrns=printTree(self.index)
        records=[]
        for rrn in rrns:
            self.file.seek(int(rrn),0)
            record=self.file.readline()
            record=self.unpack(record)
            records.append(record)
        return records

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
        if (self.index.find(data[self.primary_key])) == -1:
            self.file.seek(0,2)
            rrn=self.file.tell()
            self.file.write(self.pack(data))
            self.file.flush()
            self.index.insert(data[self.primary_key],rrn)
            return True
        return False
    
    def unpack(self,data):
        items=data.split('|')
        packet={}
        for i,item in enumerate(self.fields):
            packet[item]=items[i]
        return packet

    def update(self,key,data):
        rrn=self.index.find(key)
        if rrn==-1:
            return False
        self.file.seek(int(rrn),0)
        self.file.write(self.pack(data))
        self.file.flush()
        return True
        
    def delete(self,key):
        rrn=self.index.find(key)
        print(rrn)
        if rrn==-1:
            return False
        self.file.seek(int(rrn),0)
        self.file.write("*")
        self.file.flush()
        self.index.delete(key,rrn)
        return True
        
    def search(self,key):
        rrn=self.index.find(key)
        if rrn==-1:
            return False
        self.file.seek(int(rrn),0)
        data=self.file.readline()
        return self.unpack(data)



class NaiveDB:

    @staticmethod
    def create_db(name='database',loc='.',tables=None,):
        db_path=os.path.join(loc,".naivedb")
        os.umask(0)
        os.mkdir(db_path)
        for table in tables:
            table["file_name"]=table["name"]+".txt"
            table["index_file_name"]=table["name"]+"_index.txt"
            open(os.path.join(db_path,table["name"]+".txt","x")).close()
            open(db_path+table["name"]+"_index.txt","x").close()
        db_meta={
            "name":name,
            "tables":tables,
            "db_loc":loc
        }
        with open(db_path+"/meta.json", 'w') as outfile:
            json.dump(db_meta,outfile)

    def __init__(self,db_loc):
        db_path=db_loc+"/.naivedb/"
        try:
            with open(db_path+"/meta.json","r") as meta_file:
                self.meta_data=json.load(meta_file)
        except FileNotFoundError:
            raise NaiveDBException("db_path")
        for table in self.meta_data["tables"]:
            table_obj=Table(table,db_path)
            setattr(self,table["name"],table_obj)

    def tear_down(self):
        shutil.rmtree(os.path.join(self.meta_data["db_loc"],".naivedb"))
    
def create_db(name='database',loc='.',tables=[],):
        db_path=os.path.join(loc,".naivedb")
        os.umask(0)
        os.mkdir(db_path)
        for table in tables:
            table["file_name"]=table["name"]+".txt"
            table["index_file_name"]=table["name"]+"_index.txt"
            open(os.path.join(db_path,table["name"]+".txt","x")).close()
            open(db_path+table["name"]+"_index.txt","x").close()
        db_meta={
            "name":name,
            "tables":tables,
            "db_loc":loc
        }
        with open(db_path+"/meta.json", 'w') as outfile:
            json.dump(db_meta,outfile)