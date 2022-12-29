from django.contrib.auth.decorators import login_required
from django.urls import path
from masterclasses import views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "masterclasses/",
        views.index,
        name="index",
    ),
    path(
        "signup/",
        views.SignupView.as_view(),
        name="signup",
    ),
    path(
        "profi/<profi_login>",
        views.profi,
        name="profi",
    ),
    path(
        "masterclass/<int:masterclass_id>",
        views.masterclass_view,
        name="masterclass_view",
    ),
    path(
        "masterclass/create",
        views.masterclass_create,
        name="masterclass_create",
    ),
    path(
        "category",
        views.category_view,
        name="category_view",
    ),
]
