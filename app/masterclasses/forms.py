from datetime import date

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm
from masterclasses.models import (
    Masterclass,
    MasterclassDate,
    MasterclassType,
    PrivateStudent,
    Profi,
    Student,
)
from tempus_dominus.widgets import DatePicker, DateTimePicker, TimePicker


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
            Masterclass.cover.field.name,
            Masterclass.name.field.name,
            Masterclass.description.field.name,
            Masterclass.location.field.name,
            Masterclass.category.field.name,
            Masterclass.students_amount.field.name,
            Masterclass.student_age.field.name,
        )

    mc_type = forms.ModelChoiceField(
        queryset=MasterclassType.objects.all(),
        empty_label="Choose Masterclass Type",
        label="Masterclass Type",
    )
    date = forms.DateField(
        required=True,
        widget=DatePicker(
            options={
                "minDate": date.today().isoformat(),
                "multipleDates": True,
                "multipleDatesSeparator": "; ",
                "keepOpen": True,
            },
        ),
    )


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = (
            Student.name.field.name,
            Student.email.field.name,
        )


class StudentFormPrivate(StudentForm):
    class Meta:
        model = PrivateStudent
        fields = (
            PrivateStudent.name.field.name,
            PrivateStudent.email.field.name,
        )

    def __init__(self, *args, **kwargs):
        self.enabled_dates = kwargs.pop("enabled_dates")
        super().__init__(*args, **kwargs)
        self.fields["masterclass_date"].widget.js_options.update(
            enabledDates=[d.isoformat() for d in self.enabled_dates]
        )

    masterclass_date = forms.DateField(
        required=True,
        widget=DatePicker(
            options={
                "minDate": date.today().isoformat(),
            },
        ),
    )
