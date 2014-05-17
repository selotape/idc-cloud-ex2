from django.conf.urls import patterns, url
from students import views

urlpatterns = patterns('',
    # ex: /students/
    url(r'^$', views.index, name='index'),
    # ex: /students/5/
    url(r'^(?P<student_id>\d+)/$', views.student, name='student'),
)
