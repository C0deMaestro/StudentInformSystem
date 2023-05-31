from django.urls import path,include
from . import views
from .views import Register

urlpatterns = [
    path("",  views.main_page_for_stu, name="home"),
    path("register",  Register.as_view(), name="register"),
    path("",  include("django.contrib.auth.urls")),
    path("add_mark",  views.add_mark, name="add_mark"),
    path('change_mark',  views.change_mark, name="change_mark"),
    path("delete_mark",  views.delete_mark, name="delete_mark"),
    path("add_attendance",  views.add_attendance, name="add_attendance"),
    path("delete_attendance",  views.delete_attendance, name="delete_attendance"),
    path("add_course",views.add_course,name = "add_course"),
    path("attendance",  views.attendance_page, name="attendance"),
    path("session",  views.session_page, name="session"),
]