from django.db import models
from datetime import datetime

""" Basic models, such as user profile """
class Student(models.Model):

    def __unicode__(self):
        return self.name + ', ' + str(self.student_id) + ', ' + self.faculty

    student_id = models.IntegerField( primary_key=True )
    country = models.CharField( max_length=50 )
    city = models.CharField( max_length=50 )
    name = models.CharField( max_length=50 )
    age = models.IntegerField( max_length=2 )
    faculty = models.CharField( max_length=50 )
    creation_date = models.DateTimeField( auto_now=True )
    photo_url = models.CharField( max_length=200 )

