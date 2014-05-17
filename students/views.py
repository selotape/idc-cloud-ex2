from django.shortcuts import render
from django.http import HttpResponse
from students.models import Student

# Create your views here.
def index(request):
    latest_students_list = Student.objects.all().order_by('-creation_date')[:10]
    context = {'latest_students_list': latest_students_list}
    return render(request, 'students/index.html', context)

def student(request, student_id):
    return HttpResponse("You're looking at student %s." % student_id)
