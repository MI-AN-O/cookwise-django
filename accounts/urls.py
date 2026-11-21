from django.urls import include, path

from . import views

# Django's built-in auth views provide login/ and logout/ (plus password views).
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("", include("django.contrib.auth.urls")),
]
