import redis
from pickle import dumps, loads

#conn = Redis.connect(host='', ...)

class Cache:
    def __init__(self, conn_details):
        # get a redis reference
        print 'connection to redis using details:' + str(conn_details)
        self.r = redis.Redis(host=conn_details['host'],
                                   port=conn_details['port'],
                                   db=conn_details['db'])

    def insert(self, student_id, student):
        self.r.lpush('student_ids', student_id) 
        # if student list is already of len 50, delete the last student from cache
        if self.r.llen('sudent_ids') == 51:
            self.r.brpop('student_ids') 
        return self.r.set(student_id, dumps(student))

    def get_by_id(self, student_id):
        print 'getting student ' + str(student_id) + ' from cache'
        return loads(self.r.get(student_id))

    def get_latest(self, num):
        results = []
        for student_id in self.r.lrange('student_ids', 0, num):
            student = self.get_by_id(student_id)
            results.append(student)
        return results
                
    def remove(self, student_id):
        self.r.lrem('student_ids', 0, student_id)
        return self.r.delete(student_id)
    
def get_connection(connection_details):
    return Cache(connection_details)
