from datetime import datetime

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
class CustomUser(AbstractUser):
    ROLE_STUDENT = 'STUDENT'
    ROLE_TEACHER = 'TEACHER'
    ROLE_ADMIN = 'ADMIN'

    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student'),
        (ROLE_TEACHER, 'Teacher'),
        (ROLE_ADMIN, 'Admin')
    ]
    role = models.CharField(max_length=16, choices=ROLE_CHOICES)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student')
    name = models.CharField("ФИО студента", max_length=40)
    def __str__(self):
        return f"{self.name}"

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField("ФИО учителя",max_length=40)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"

class Course(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='courses')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

class Attendance(models.Model):
    LABORATORY = 'Лабораторная работа'
    SEMINAR = 'Семинар'
    LECTURE = 'Лекция'
    SESSION = "Сессия"
    EXAM = "Экзамен"
    TEST = "Зачет"
    GRADE_CHOICES = [
        (LABORATORY, 'Laboratory work'),
        (SEMINAR, 'Seminar'),
        (LECTURE, 'Lecture'),
        (SESSION, 'Session'),
        (EXAM, 'Exam'),
        (TEST, 'Test'),
    ]
    date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance_type = models.CharField(max_length=20, choices=GRADE_CHOICES,default='Семинар')

class Grades(models.Model):
    LABORATORY = 'Лабораторная работа'
    SEMINAR = 'Семинар'
    LECTURE = 'Лекция'
    SESSION = "Сессия"
    EXAM = "Экзамен"
    TEST = "Зачет"
    GRADE_CHOICES = [
        (LABORATORY, 'Laboratory work'),
        (SEMINAR, 'Seminar'),
        (LECTURE, 'Lecture'),
        (SESSION, 'Session'),
        (EXAM, 'Exam'),
        (TEST, 'Test'),
    ]
    value = models.DecimalField(decimal_places=2, max_digits=5)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField()
    grade_type = models.CharField(max_length=20, choices=GRADE_CHOICES,default='Семинар')
    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"