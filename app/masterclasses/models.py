from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models

MASTERCLASS_DATE = models.DateField()
# Create your models here.
class Profi(AbstractUser):
    tel = models.CharField(max_length=12, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)


class Student(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=12)

    def __str__(self) -> str:
        return self.name


class MasterclassType(models.Model):
    name = models.CharField(max_length=24)
    description = models.CharField(max_length=24)

    def __str__(self) -> str:
        return self.description


class PrivateStudent(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    masterclass_date = MASTERCLASS_DATE


class Masterclass(models.Model):
    MIN_STUDENT_AMOUNT = 1
    MAX_STUDENT_AMOUNT = 100
    MIN_DESCRIPTION_LENGTH = 12

    name = models.CharField(max_length=32)
    cover = models.ImageField(null=True, blank=True, upload_to="covers")
    description = models.TextField(
        max_length=120,
        validators=[MinLengthValidator(MIN_DESCRIPTION_LENGTH)],
    )
    student_age = models.IntegerField()
    students_amount = models.IntegerField(
        validators=[
            MinValueValidator(MIN_STUDENT_AMOUNT),
            MaxValueValidator(MAX_STUDENT_AMOUNT),
        ],
    )
    location = models.TextField(max_length=64)
    profi = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    students = models.ManyToManyField(Student, blank=True)
    private_students = models.ManyToManyField(PrivateStudent, blank=True)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    category = models.ManyToManyField(Category)
    mc_type = models.ForeignKey(MasterclassType, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class MasterclassDate(models.Model):
    masterclass = models.ForeignKey(Masterclass, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.masterclass.name} | {self.date}"
