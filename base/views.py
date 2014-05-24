""" Views for the base application """
from django.shortcuts import render
from django.http import HttpResponseRedirect
from base.models import Student
from base.forms import StudentForm

# Create your views here.
def home(request):
    latest_students_list = Student.objects.all().order_by('-creation_date')[:10]

    form = StudentForm()
    context = {
        'latest_students_list': latest_students_list,
        'form' : form,
    }
    return render(request, 'base/home.html', context)


def add_student(request):
    if request.method == 'POST': # If the form has been submitted...
        form = StudentForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
	    student = form.save(commit=False)
    	    student.save()
    return HttpResponseRedirect('/') # Redirect home after POST

def delete_student(request, student_id):
    if request.method == 'GET':
        student = Student.objects.get(student_id=student_id)
	if student != None:
	    student.delete()
    return HttpResponseRedirect('/') # Redirect home after DELETE
