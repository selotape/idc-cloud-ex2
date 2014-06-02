import redis
from pickle import dumps, loads

# TODO - turn cache into LRU store of students (instead of maintaining a list of students like a dummy)
class Cache:
    def __init__(self, conn_details):
        print 'connecting to Redis using details:' + str(conn_details)
        self.r = redis.Redis(host=conn_details['host'],
                                   port=conn_details['port'],
                                   db=conn_details['db'])

    def insert(self, student_id, student):
        print 'inserting <' + str(student) + '> into cache'
        self.r.lpush('student_ids', student_id) 
        # if student list is already of len 50, delete the last student from cache
        if self.r.llen('sudent_ids') == 51:
            self.r.brpop('student_ids') 
        return self.r.set(student_id, dumps(student))

    def get_by_id(self, student_id):
        print 'getting student ' + str(student_id) + ' from cache'
        cache_student = (self.r.get(student_id))
	if cache_student != None:	    
            return loads(cache_student)
	else:
	    print 'Cache Miss was performed on DB with student_id ' + str(student_id)
	    return None

    def get_latest(self, num):
        results = []
        for student_id in self.r.lrange('student_ids', 0, num):
            student = self.get_by_id(student_id)
            results.append(student)
        return results
                
    def remove(self, student_id):
        self.r.lrem('student_ids', 0, student_id)
        return self.r.delete(student_id)

    def _clear(self):
        for k in self.r.keys():
            r.delete(k)
    
def get_connection(connection_details):
    return Cache(connection_details)
