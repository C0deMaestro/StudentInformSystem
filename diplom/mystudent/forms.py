from datetime import timezone

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Student, Grades, CustomUser, Attendance, Teacher, Course
from django.forms import ModelForm, TextInput, Textarea, DateTimeInput, NumberInput, SelectDateWidget
from django import forms


User = get_user_model()

class UserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username","role")

class CourseForm(forms.Form):
    name = forms.CharField(max_length=100)
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())

class AttendanceForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    attendance_type = forms.ChoiceField(choices=Grades.GRADE_CHOICES, required=True)
    date = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'))
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'attendance_type',"date"]

class DeleteAttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'attendance_type',"date"]
    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        attendance_type = cleaned_data.get('attendance_type')
        date = cleaned_data.get('date')
        course = cleaned_data.get('course')
        if not Attendance.objects.filter(student=student, attendance_type=attendance_type, date=date, course=course).exists():
            raise forms.ValidationError("Посещения с такими параметрами не существует")
        return cleaned_data

class DeleteGradeForm(ModelForm):
    class Meta:
        model = Grades
        fields = ['value', 'grade_type', 'date', 'course', 'student']


    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        grade_type = cleaned_data.get('grade_type')
        date = cleaned_data.get('date')
        course = cleaned_data.get('course')
        value = cleaned_data.get("value")
        if not Grades.objects.filter(student=student, grade_type=grade_type, date=date, course=course, value = value).exists():
            raise forms.ValidationError("Оценки с такими параметрами не существует")
        return cleaned_data

class GradesForm(ModelForm):
    exist_grade_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    date = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'))
    grade_type = forms.ChoiceField(choices=Grades.GRADE_CHOICES, required=True)
    class Meta:
        model = Grades
        fields = ['value', 'course', 'student', 'grade_type',"date"]
    def clean_value(self):
        # Проверяем, что оценка в диапазоне от 2 до 4
        cleaned_data = super().clean()
        value = cleaned_data.get("value")
        if value < 1 or value > 5:
            raise forms.ValidationError("Оценка должна быть в диапазоне от 1 до 5")
        return value


class GradesChangeForm(forms.ModelForm):
    class Meta:
        model = Grades
        fields = ['value', 'grade_type', 'date', 'course', 'student']

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        grade_type = cleaned_data.get('grade_type')
        date = cleaned_data.get('date')
        course = cleaned_data.get('course')

        if not Grades.objects.filter(student=student, grade_type=grade_type, date=date, course=course).exists():
            raise forms.ValidationError("Оценки с такими параметрами не существует")
        return cleaned_data