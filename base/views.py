""" Views for the base application """
from django.shortcuts import render
from django.http import HttpResponseRedirect
from base.models import Student
from base.forms import StudentForm
from base.utils import s3

# Create your views here.
def home(request):
    #read latest 10 students from 'slave' db
    latest_students_list = Student.objects.using('slave').all().order_by('-creation_date')[:10]

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
	    student = form.save(commit=False)
	    photo_url = s3.upload_file(request.FILES['student_photo'])# TODO - somehow take the 'name' of the photo from the request itself
	    student.photo_url = photo_url
    	    student.save()
    return HttpResponseRedirect('/') # Redirect home after POST

def delete_student(request, student_id):
    if request.method == 'GET':
        student = Student.objects.get(student_id=student_id)
	if student != None:
	    s3.delete_file(student.photo_url)
	    student.delete()
    return HttpResponseRedirect('/') # Redirect home after DELETE
