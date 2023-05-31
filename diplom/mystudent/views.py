from datetime import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .models import *
from .forms import GradesForm, UserCreationForm, DeleteGradeForm, CourseForm, AttendanceForm, GradesChangeForm, \
    DeleteAttendanceForm


def main_page_for_stu(request):
    user = request.user
    if user.is_authenticated:
        if user.role == "STUDENT":
            user = request.user
            student = user.student
            grades = Grades.objects.filter(student=student)
            courses = {}
            for grade in grades:
                if grade.course.name not in courses:
                    courses[grade.course.name] = {'grades': [], 'avg_grade': None}
                courses[grade.course.name]['grades'].append(grade)

            for course in courses:
                total_grades = sum([grade.value for grade in courses[course]['grades']])
                num_of_grades = len(courses[course]['grades'])
                if num_of_grades > 0:
                    courses[course]['avg_grade'] = round(total_grades / num_of_grades, 2)
            context = {'student': student, 'courses': courses}
            return render(request, 'mystudent/home_student.html', context)

        elif user.role == "TEACHER":
            teacher = user.teacher
            courses = teacher.course_set.all()
            return render(request, 'mystudent/home_teacher.html', {'courses': courses,"teacher":teacher})
        else:
            return render(request, "mystudent/home_anonim.html")
    else:
        return render(request,"mystudent/home_anonim.html")


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            teacher = form.cleaned_data['teacher']
            course = Course.objects.create(name=name, teacher=teacher)
            students = Student.objects.all()
            for student in students:
                course.students.add(student)
            return redirect('home')
    else:
        form = CourseForm()
    return render(request, 'mystudent/add_course.html', {'form': form})


def add_mark(request):
    if request.method == "POST":
        form = GradesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            context = {
                'form': form
            }
            return render(request, 'mystudent/add_mark.html', context)
    form = GradesForm
    data = {
        "form":form
    }
    return render(request,"mystudent/add_mark.html",data)

def change_mark(request):
    if request.method == 'POST':
        form = GradesChangeForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            course = form.cleaned_data['course']
            date = form.cleaned_data['date']
            grade_type = form.cleaned_data['grade_type']
            value = form.cleaned_data['value']
            grade = Grades.objects.get(student=student, grade_type=grade_type, date=date, course=course,)
            grade.value = value
            grade.save()
            return redirect('home')
    else:
        form = GradesChangeForm()
    return render(request, 'mystudent/change_mark.html', {'form': form})

def delete_mark(request):
    if request.method == 'POST':
        form = DeleteGradeForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            course = form.cleaned_data['course']
            date = form.cleaned_data['date']
            grade_type = form.cleaned_data['grade_type']
            value = form.cleaned_data['value']
            grades = Grades.objects.filter(student=student, grade_type=grade_type, date=date, course=course, value = value)
            grades.delete()
            return redirect('home')  # перенаправляем на домашнюю страницу
    else:
        form = DeleteGradeForm()
    return render(request, 'mystudent/delete_mark.html', {'form': form})

def delete_attendance(request):
    if request.method == 'POST':
        form = DeleteAttendanceForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            course = form.cleaned_data['course']
            attendance_type = form.cleaned_data['attendance_type']
            date = form.cleaned_data['date']
            atten = Attendance.objects.filter(student=student, attendance_type=attendance_type, date=date, course=course)
            atten.delete()
            return redirect('home')
    else:
        form = DeleteAttendanceForm()
    return render(request, 'mystudent/delete_attendance.html', {'form': form})

def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            course = form.cleaned_data['course']
            date = form.cleaned_data['date']
            attendance_type = form.cleaned_data['attendance_type']
            Attendance.objects.create(
                date=date,
                course=course,
                student=student,
                attendance_type = attendance_type,
            )
            return redirect('home')
    else:
        form = AttendanceForm()
    return render(request, 'mystudent/add_attendance.html', {'form': form, })


def session_page(request):
    user = request.user
    student = user.student
    grades = Grades.objects.filter(student=student)
    courses = {}

    for grade in grades:
        if grade.course.name not in courses:
            courses[grade.course.name] = {'grades': [], 'avg_grade': None}
        courses[grade.course.name]['grades'].append(grade)

    for course in courses:
        total_grades = sum([grade.value for grade in courses[course]['grades']])
        num_of_grades = len(courses[course]['grades'])
        if num_of_grades > 0:
            courses[course]['avg_grade'] = round(total_grades / num_of_grades, 2)
    context = {'student': student, 'courses': courses}

    return render(request,"mystudent/session.html", context)

def attendance_page(request):
    student = request.user.student
    attendance_list = Attendance.objects.filter(student=student).order_by('-date')
    return render(request, 'mystudent/attendance.html', {'attendance_list': attendance_list})


class Register(View):
    template_name = 'registration/register.html'
    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            role = form.cleaned_data.get('role')
            if role == CustomUser.ROLE_STUDENT:
                student = Student.objects.create(user=user, name=username)
                user.is_student = True
                user.save()
                courses = Course.objects.all()
                for course in courses:
                    course.students.add(student)
            elif role == CustomUser.ROLE_TEACHER:
                teacher = Teacher.objects.create(user=user, name=username)
                user.is_teacher = True
                user.save()
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


