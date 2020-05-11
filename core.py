import json
import os
from helpers import (
    MissingDataException,
    FileMissing
) 

class Index:
    def __init__(self):
        pass

class Table:
    def __init__(self,db_loc,file_name,index_file_name):
        try:
            self.file=open(db_loc+file_name,"a+")
        except FileNotFoundError:
            raise FileMissing("Kindly declare Tables before invocation.")
        try:
            self.index_file=open(db_loc+index_file_name,"a+")
        except FileNotFoundError:
            raise FileMissing("Kindly declare Tables before invocation.")
    def insert(self,data):
        #step 1:insert record in table file
        #step 1:insert key in index file
        pass

    def search(self,key):
        #step1: retrieve the address of key from index
        #step2: goto address from above and retrieve from above
        pass

    def delete(self,key):
        #step1: search the key
        #step2: delete the record
        #step3 delete the key from index
        pass
    def pack(self,data_dict):
        #pack the data in order to put it onto file
        pass
    def unpack(self,data):
        #unpack the data string and wrap it as a dict
        pass


class NaiveDB:

    @staticmethod
    def create_db(name='database',loc='./',tables=None,):
        if not tables:
            raise MissingDataException("Database without tables cannot be created.")
        db_meta={
            "name":name,
            "tables":tables
        }
        db_path=os.path.join(loc,"naivedb")
        os.umask(0)
        os.mkdir(db_path)
        with open(loc+"naivedb/meta.json", 'w') as outfile:
            json.dump(db_meta,outfile)
        
        return 

    def __init__(self,):
        pass
