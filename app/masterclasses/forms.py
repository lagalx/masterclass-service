from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm
from masterclasses.models import (
    Masterclass,
    MasterclassDate,
    MasterclassType,
    Profi,
    Student,
)


class ProfiCreationForm(UserCreationForm):
    class Meta:
        model = Profi
        fields = (
            Profi.username.field.name,
            Profi.email.field.name,
            Profi.first_name.field.name,
            Profi.last_name.field.name,
            Profi.birth_date.field.name,
            Profi.tel.field.name,
        )


class ProfiChangeForm(UserChangeForm):
    class Meta:
        model = Profi
        fields = ProfiCreationForm.Meta.fields


class MasterclassCreateForm(ModelForm):
    class Meta:
        model = Masterclass
        fields = (
            Masterclass.name.field.name,
            Masterclass.description.field.name,
            Masterclass.location.field.name,
            Masterclass.category.field.name,
            Masterclass.students_amount.field.name,
            Masterclass.student_age.field.name,
        )


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = (
            Student.name.field.name,
            Student.email.field.name,
        )
