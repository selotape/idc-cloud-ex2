from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("hello world, you're at students index")

def student(request, student_id):
    return HttpResponse("You're looking at student %s." % student_id)
