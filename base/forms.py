import forms
from django import forms
from base.models import Student

# Create the form class.
class MySqlStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id', 'country', 'city', 'age', 'faculty']

class DynamoStudentForm(forms.Form):
    name = forms.CharField(max_length=100)
    student_id = forms.IntegerField()
    country = forms.CharField(max_length=100)
    city =  forms.CharField(max_length=100)
    age = forms.IntegerField()
    faculty = forms.CharField(max_length=100)
    
    def to_student(self):
        student = Student()
        student.student_id = self.cleaned_data['student_id']
        student.country = self.cleaned_data['country']
        student.city = self.cleaned_data['city']
        student.name = self.cleaned_data['name']
        student.age = self.cleaned_data['age']
        student.faculty = self.cleaned_data['faculty']
        return student
