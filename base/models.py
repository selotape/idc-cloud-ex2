from django.db import models
from datetime import datetime

""" Basic models, such as user profile """
class Student(models.Model):

    def __unicode__(self):
        return self.name + ', ' + str(self.student_id) + ', ' + \
		self.faculty + ', ' + self.photo_url

    student_id = models.IntegerField( primary_key=True )
    country = models.CharField( max_length=50 )
    city = models.CharField( max_length=50 )
    name = models.CharField( max_length=50 )
    age = models.IntegerField( max_length=2 )
    faculty = models.CharField( max_length=50 )
    creation_date = models.DateTimeField( auto_now=True )
    photo_url = models.URLField() # TODO fix bug of large/longnamed photos not being saved
				  # possible tests: 
				  # upload large file but with short name and vice versa
				  # create Student model in shell and instantiate photo_url in different ways
