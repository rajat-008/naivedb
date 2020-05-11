class NaiveDBException(Exception):
    def __init__(self,msg):
        self.msg=msg

class MissingDataException(NaiveDBException):
    pass

class FileMissing(NaiveDBException):
    pass
