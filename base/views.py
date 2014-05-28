""" Views for the base application """
from django.shortcuts import render
from django.http import HttpResponseRedirect
from base.models import Student
from base.forms import StudentForm
from base.utils import s3
from base.utils import cache_db

def mysql(request):
    #read latest 10 students from 'slave' db
    latest_students_list = Student.objects.using('slave').all().order_by('-creation_date')[:10]

    form = StudentForm()
    context = {
	'app_name' : 'mysql',
        'latest_students_list': latest_students_list,
        'form' : form,
    }
    return render(request, 'base/mysql.html', context)

def mysql_add_student(request):
    if request.method == 'POST': # If the form has been submitted...
        form = StudentForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
	    student = form.save(commit=False)
	    photo_url = s3.upload_file(request.FILES['student_photo'])# TODO - somehow take the 'name' of the photo from the request itself
	    student.photo_url = photo_url
    	    student.save()
    return HttpResponseRedirect('/mysql') # Redirect home after POST

def mysql_delete_student(request, student_id):
    if request.method == 'GET':
        student = Student.objects.get(student_id=student_id)
	if student != None:
	    s3.delete_file(student.photo_url)
	    student.delete()
    return HttpResponseRedirect('/mysql') # Redirect home after DELETE




def dynamo(request):
    #read latest 10 students
    latest_students_list = cache_db.get_latest(10)

    form = StudentForm()
    context = {
	'app_name' : 'dynamo',
        'latest_students_list': latest_students_list,
        'form' : form,
    }
    return render(request, 'base/dynamo.html', context)

def dynamo_add_student(request):
#    if request.method == 'POST': # If the form has been submitted...
#        form = StudentForm(request.POST) # A form bound to the POST data
#        if form.is_valid(): # All validation rules pass
#	    student = form.to_student()
#	    photo_url = s3.upload_file(request.FILES['student_photo'])# TODO - somehow take the 'name' of the photo from the request itself
#	    student.photo_url = photo_url
#    	    cache_db.save(student)
    return HttpResponseRedirect('/dynamo')

def dynamo_delete_student(request, student_id):
#    if request.method == 'GET':
#        student = cache_db.get_by_id(student_id)
#	if student != None:
#	    s3.delete_file(student.photo_url)
#	    cache_db.delete(student_id)
    return HttpResponseRedirect('/dynamo')
