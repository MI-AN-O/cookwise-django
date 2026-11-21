from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Category, Recipe


def home(request):
    # Rendered from the project-level templates folder (templates/home.html)
    return render(request, "home.html", {"categories": Category.objects.all()})


def recipe_list(request):
    # Rendered from the app-level templates folder (recipes/templates/recipes/)
    recipes = Recipe.objects.select_related("category", "author")
    return render(request, "recipes/recipe_list.html", {"title": "All recipes", "recipes": recipes})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    recipes = category.recipes.select_related("author")
    return render(request, "recipes/recipe_list.html", {
        "title": category.name,
        "tagline": category.tagline,
        "recipes": recipes,
    })


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.select_related("category", "author"), pk=pk)
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe})


@login_required
def my_recipes(request):
    recipes = request.user.recipes.select_related("category")
    return render(request, "recipes/recipe_list.html", {"title": "My recipes", "recipes": recipes})


@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, f"“{recipe.title}” was added.")
            return redirect(recipe)
    else:
        form = RecipeForm()
    return render(request, "recipes/recipe_form.html", {"form": form, "heading": "Add a recipe"})


@login_required
def recipe_update(request, pk):
    # Filtering by author means other users get a 404 instead of someone else's recipe
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, f"“{recipe.title}” was updated.")
            return redirect(recipe)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, "recipes/recipe_form.html", {"form": form, "heading": f"Edit {recipe.title}"})


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == "POST":
        recipe.delete()
        messages.success(request, f"“{recipe.title}” was deleted.")
        return redirect("recipes:my_recipes")
    return render(request, "recipes/recipe_confirm_delete.html", {"recipe": recipe})
