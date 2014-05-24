from django.forms import ModelForm
from base.models import Student

# Create the form class.
class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id', 'country', 'city', 'age', 'faculty']
