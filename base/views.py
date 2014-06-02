from django.shortcuts import render
from django.http import HttpResponseRedirect
from base.models import Student
from base.forms import MySqlStudentForm, DynamoStudentForm
from base.utils import s3
from base.utils import cache_db
from base.utils.model_conversions import cache_to_model
from base.utils.model_conversions import db_to_model


def mysql(request):
    #read latest 10 students from 'slave' db
    latest_students_list = Student.objects.using('slave').all().order_by('-creation_date')[:10]

    form = MySqlStudentForm()
    context = {
	'app_name' : 'mysql',
        'latest_students_list': latest_students_list,
        'form' : form,
    }
    return render(request, 'base/mysql.html', context)

def mysql_add_student(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MySqlStudentForm(request.POST) # A form bound to the POST data
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




db_conn_details = {
    'table' : 'idc-cloud-ex2-dynamo-table',
    # credentials : in_boto_config,
}
cache_conn_details = { # TODO - move this to some config/properties file
    'host' : 'idc-cloud-ex2-cache.brlx8k.0001.use1.cache.amazonaws.com',
    'port' : 6379,
    'db'   : 0,
}

cache_db = cache_db.get_connection(db_conn_details, cache_conn_details)

def dynamo(request):
    print 'GET was made to dynamo'
    # read latest 10 students
    print 'getting latest students from cache_db'
    latest_students = cache_db.get_latest(10)
    
    # make them presentable and serve them to the client
    #latest_students = map(cache_to_model, latest_students)
    form = DynamoStudentForm()
    context = {
        'app_name' : 'dynamo',
        'latest_students_list': latest_students,
        'form' : form,
    }
    return render(request, 'base/dynamo.html', context)

def dynamo_by_attribute(request, attribute):
    value = request.GET.get('q', '')
    print 'GET was made to dynamo_by_attribute with parameter ' + attribute + '=' + value
    # read latest 10 students
    print 'getting students by attribute from cache_db'
    students = cache_db.get_by_attribute(attribute, value)
    
    # make them presentable and serve them to the client
    #latest_students = map(cache_to_model, latest_students)
    form = DynamoStudentForm()
    context = {
        'app_name' : 'dynamo',
        'latest_students_list': students,
        'form' : form,
    }
    return render(request, 'base/dynamo.html', context)
    

def dynamo_add_student(request):
    if request.method == 'POST': # If the form has been submitted...
        print 'Post was made to dynamo_add_student'
        form = DynamoStudentForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            print 'Post form was valid'
	    student = form.to_student()
            photo_url = s3.upload_file(request.FILES['student_photo'])# TODO - somehow take the 'name' of the photo from the request itself
	    student.photo_url = photo_url
    	    if  not cache_db.insert(student):
                raise Exception('failed inserting %s into cache_db', str(student))
        else:
            for field in form:
                print 'field error: ' + str(field.errors)
    return HttpResponseRedirect('/dynamo')

def dynamo_delete_student(request, student_id):
    print 'inside dynamo_delete_student'
    if request.method == 'GET':# TODO - change this to DELETE
        student = cache_db.get_by_id(student_id)
        print 'got student ' + str(student) + ' from cache_db'
	if student != None:
            print 'deleting ' + student.photo_url + ' from s3'
	    s3.delete_file(student.photo_url)
            print 'deleting ' + student.photo_url + ' from cache_db'
	    cache_db.remove(student_id)
    return HttpResponseRedirect('/dynamo')
