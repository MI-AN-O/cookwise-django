from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import SignUpForm


def signup(request):
    if request.user.is_authenticated:
        return redirect("recipes:home")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the new user straight in
            messages.success(request, f"Welcome to CookWise, {user.username}!")
            return redirect("recipes:home")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})
