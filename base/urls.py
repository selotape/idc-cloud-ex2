"""urlconf for the base application"""

from django.conf.urls import url, patterns


urlpatterns = patterns('base.views',
    url(r'^$', 'home', name='home'),
    url(r'^students/add$', 'add_student', name='add_student'),
    url(r'^students/delete/(?P<student_id>\w{0,50})$', 'delete_student', name='delete_student' ),
)
