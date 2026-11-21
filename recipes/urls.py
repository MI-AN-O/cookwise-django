from django.urls import path

from . import views

app_name = "recipes"

# The fixed paths ("new/", "mine/", "<int:pk>/") come before "<slug:slug>/" so they
# are not mistaken for category names.
urlpatterns = [
    path("", views.home, name="home"),
    path("recipes/", views.recipe_list, name="recipe_list"),
    path("recipes/new/", views.recipe_create, name="recipe_create"),
    path("recipes/mine/", views.my_recipes, name="my_recipes"),
    path("recipes/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("recipes/<int:pk>/edit/", views.recipe_update, name="recipe_update"),
    path("recipes/<int:pk>/delete/", views.recipe_delete, name="recipe_delete"),
    path("recipes/<slug:slug>/", views.category_detail, name="category_detail"),
]
