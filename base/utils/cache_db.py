import cache
import db

class Cache_Db:
    mycache = None
    def __init__(self, db_conn_details, cache_conn_details):
        #self.db = db.get_connection(db_conn_details)
        self.mycache = cache.get_connection(cache_conn_details)

    
    def insert(self, student):
        #print 'inserting ' + str(student) + ' into db'
        #if db.insert(student.student_id, student):
        print 'inserting ' + str(student) + ' into cache'
        return self.mycache.insert(student.student_id, student)
    
    def remove(self,student_id):
        #if db.remove(student_id):
        return self.mycache.remove(student_id)
    
    def get_by_id(self,student_id):
        student = self.mycache.get_by_id(student_id)
        #if student == None:
        #    student = db.get_by_id(student_id)
        return student
    
    def get_latest(self, num):
        students = self.mycache.get_latest(num)
        ## following code is needed only if we assume the cache is not omnipotent
        #if len(students) < num:
        #    students = db.get_latest(num)
        #    cache.upsert(students)
        return students

    def get_by_attribute(self, attribute, value):
        #students = db.get_by_attribute(attribute, value)
        #return students
        return None

def get_connection(db_conn_details, cache_conn_details):
    return Cache_Db(db_conn_details, cache_conn_details)
