from django.contrib import admin
from masterclasses.models import (
    Category,
    Masterclass,
    MasterclassDate,
    MasterclassType,
    PrivateStudent,
    Profi,
    Student,
)

# Register your models here.
admin.site.register(Profi)
admin.site.register(Student)
admin.site.register(PrivateStudent)
admin.site.register(Masterclass)
admin.site.register(Category)
admin.site.register(MasterclassDate)
admin.site.register(MasterclassType)
