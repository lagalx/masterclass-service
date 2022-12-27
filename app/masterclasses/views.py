from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from masterclasses.forms import MasterclassCreateForm, ProfiCreationForm, StudentForm
from masterclasses.models import Category, Masterclass, Profi, Student

SEARCH_KEY = "search"
CATEGORY_KEY = "category"


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

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            check_student = mc.students.filter(name=form.instance.name).first()
            if not check_student:
                student = form.save()
                mc.students.add(student)
        return redirect(
            "masterclass_view",
            masterclass_id=masterclass_id,
        )
    else:
        form = StudentForm()
    context.update(masterclass=mc, form=form)
    return render(request, "masterclass/view.html", context=context)


def masterclass_create(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        form = MasterclassCreateForm(request.POST)
        if form.is_valid():
            form.instance.profi = request.user
            masterclass = form.save()
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
