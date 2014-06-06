import cache
import db

class Cache_Db:
    mycache = None
    def __init__(self, db_conn_details, cache_conn_details):
        self.mydb = db.get_connection(db_conn_details)
        self.mycache = cache.get_connection(cache_conn_details)

    
    def insert(self, student):
        print 'inserting <' + str(student) + '> into cache_db'
        if self.mydb.insert(student.student_id, student) and \
	   self.mycache.insert(student.student_id, student):
            return True
        else: return False
    
    def remove(self,student_id):
        if self.mydb.remove(student_id) and self.mycache.remove(student_id):
            return True
        else: 
            return False
    
    def get_by_id(self,student_id):
        student = self.mycache.get_by_id(student_id)
        if student == None:
            student = self.mydb.get_by_id(student_id)
            self.mycache.insert(student_id, student)
        return student
   
    """ Currently supports only cache!""" 
    def get_latest(self, num):
        students = self.mycache.get_latest(num)
        ## following code is needed only if we assume cache is not omnipotent
        #if len(students) < num:
        #    students = db.get_latest(num)
        #    cache.upsert(students)
        return students

    """ Currently supports only db!""" 
    def get_by_attribute(self, attribute, value):
        students = self.mydb.get_by_attribute(attribute, value)
        return students 

    def _clear(self):
        self.mydb._clear()
        self.mycache._clear()

def get_connection(db_conn_details, cache_conn_details):
    return Cache_Db(db_conn_details, cache_conn_details)
