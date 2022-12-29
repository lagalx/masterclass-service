from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from masterclasses.forms import (
    MasterclassCreateForm,
    ProfiCreationForm,
    StudentForm,
    StudentFormPrivate,
)
from masterclasses.models import (
    Category,
    Masterclass,
    MasterclassDate,
    MasterclassType,
    Profi,
    Student,
)

SEARCH_KEY = "search"
CATEGORY_KEY = "category"
MC_PUBLIC = MasterclassType.objects.get(name="public")
MC_PRIVATE = MasterclassType.objects.get(name="private")

# Create your views here.
class SignupView(CreateView):
    form_class = ProfiCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def index(request: HttpRequest) -> HttpResponse:
    context = {}
    query = request.GET.get(SEARCH_KEY)
    category = request.GET.get(CATEGORY_KEY)

    if query:
        masterclasses = Masterclass.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
        )
    else:
        masterclasses = Masterclass.objects.all()

    if category:
        category = Category.objects.get(name=category)
        masterclasses = masterclasses.filter(category__in=[category]).all()
    context.update(masterclasses=masterclasses)
    return render(request, "index.html", context=context)


def profi(request: HttpRequest, profi_login: str) -> HttpResponse:
    context = {}
    user = Profi.objects.get(username=profi_login)
    context.update(profi=user)
    return render(request, "profi.html", context=context)


@login_required
def masterclass_view(request: HttpRequest, masterclass_id: int) -> HttpResponse:
    context = {}
    mc = Masterclass.objects.get(id=masterclass_id)
    date = None

    if mc.mc_type == MC_PUBLIC:
        date = MasterclassDate.objects.get(masterclass=mc).date
    else:
        date = [d.date for d in MasterclassDate.objects.filter(masterclass=mc).all()]
    if request.method == "POST":
        form = None
        if mc.mc_type == MC_PUBLIC:
            form = StudentForm(request.POST)
        else:
            form = StudentFormPrivate(request.POST, enabled_dates=date)

        if form.is_valid():
            if mc.mc_type == MC_PUBLIC:
                check_student = mc.students.filter(name=form.instance.name).first()
            else:
                form.instance.masterclass_date = form.cleaned_data["masterclass_date"]
                check_student = mc.private_students.filter(
                    name=form.instance.name,
                    masterclass_date=form.instance.masterclass_date,
                )
            if not check_student:
                student = form.save()
        return redirect(
            "masterclass_view",
            masterclass_id=masterclass_id,
        )
    else:

        if mc.mc_type == MC_PUBLIC:
            form = StudentForm()
        else:
            form = StudentFormPrivate(enabled_dates=date)

    context.update(masterclass=mc, form=form, date=date)
    return render(request, "masterclass/view.html", context=context)


def masterclass_create(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        form = MasterclassCreateForm(request.POST)
        if form.is_valid():
            form.instance.profi = request.user
            date = form.cleaned_data["date"]
            mc_type = form.cleaned_data["mc_type"]
            masterclass = form.save(commit=False)
            masterclass.mc_type = mc_type
            form.save()
            MasterclassDate.objects.create(masterclass=masterclass, date=date)
            return redirect("index")
    else:
        form = MasterclassCreateForm()
    context.update(form=form)
    return render(request, "masterclass/create.html", context=context)


def category_view(request: HttpRequest) -> HttpResponse:
    context = {}
    categories = Category.objects.all()
    context.update(categories=categories)
    return render(request, "category.html", context=context)
