from boto.dynamodb2.items import Item
from boto.dynamodb2.table import Table

from base.models import Student

import time
from datetime import datetime


class Db:
    def __init__(self, conn_details):
        self.table = Table(conn_details['table'])

    def insert(self, student_id, student):
        student_item = student_to_item(self.table, student)
        return student_item.save()

    def get_by_id(self, my_student_id):
        student_item = self.table.get_item(student_id=int(my_student_id))
        if student_item is not None: return item_to_student(student_item)
	else:
	    print 'DB lookup Miss was performed on DB with student_id ' + str(my_student_id)
	    return None

    """currently only supports attributes 'faculty'||'city'"""
    # TODO - support general column name
    def get_by_attribute(self, attribute, value):
        if attribute == 'faculty':
            items = self._get_items_by_faculty(value)
        if  attribute == 'city':
            items = self._get_items_by_city(value)

        students = []
        for item in items:
            students.append(item_to_student(item))
        return students

    def _get_items_by_faculty(self, faculty):
        return self.table.query(faculty__eq=faculty, index='faculty-index')

    def _get_items_by_city(self, city):
        return self.table.query(city__eq=city, index='city-index')

    def remove(self, student_id):
        student_item = self.get_by_id(student_id)
        return student_item.delete()

    def _clear(self):
        all_students_items = self.table.scan()
        for student_item in all_students_items:
            student_item.delete()

            
        
    
def student_to_item(table, student):
    student_item = Item(table, data={
        'student_id': student.student_id,
        'country': student.country,
        'city': student.city,
        'name': student.name,
        'age': student.age,
        'faculty': student.faculty,
        'creation_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'photo_url': student.photo_url,
        })
    return student_item

def item_to_student(item):
    student = Student()
    student.student_id = item['student_id']
    student.country = item['country']
    student.city = item['city']
    student.name = item['name']
    student.age = item['age']
    student.faculty = item['faculty']

    timestring = item['creation_date']
    timestamp = time.strptime(timestring, '%Y-%m-%d %H:%M')
    student.creation_date = datetime.fromtimestamp(time.mktime(timestamp))

    student.photo_url = item['photo_url']
    return student
	


def get_connection(connection_details):
    return Db(connection_details)
