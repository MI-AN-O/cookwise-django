from django.http import Http404
from django.shortcuts import render

# Temporary in-memory data. This moves into models.py once we reach the database topic.
CATEGORIES = {
    "sweets": {"name": "Sweets", "tagline": "Bake it like you mean it.", "image": "pexels-catscoming-3752075.jpg"},
    "spicy": {"name": "Spicy", "tagline": "A little goes a long way.", "image": "pexels-pixabay-70842.jpg"},
    "main-dishes": {"name": "Main dishes", "tagline": "Find your next favourite dish.", "image": "pexels-catscoming-1907244.jpg"},
    "appetisers": {"name": "Appetisers", "tagline": "Small bites to start the meal right.", "image": "IMAGE7.jpeg"},
}

RECIPES = [
    {
        "name": "Spaghetti Carbonara",
        "category": "main-dishes",
        "ingredients": ["200g spaghetti", "100g pancetta", "2 large eggs", "50g pecorino cheese", "Salt and pepper", "Fresh parsley"],
        "instructions": "Cook spaghetti. Fry pancetta. Beat eggs with cheese, add to pasta off heat. Mix in pancetta. Serve with parsley.",
    },
    {
        "name": "Vegetable Stir-Fry",
        "category": "main-dishes",
        "ingredients": ["2 cups mixed vegetables (bell peppers, broccoli, carrots)", "2 tablespoons soy sauce", "1 tablespoon olive oil", "1 clove garlic, minced", "Salt and pepper"],
        "instructions": "Heat oil, add garlic, and stir-fry vegetables for 5-7 minutes. Add soy sauce and cook for another minute.",
    },
    {
        "name": "Garlic Bread",
        "category": "appetisers",
        "ingredients": ["1 baguette", "3 tablespoons butter, softened", "2 cloves garlic, minced", "Fresh parsley"],
        "instructions": "Mix butter, garlic and parsley. Spread on sliced baguette and bake at 200°C for 8-10 minutes.",
    },
    {
        "name": "Pili Pili Chicken Wings",
        "category": "spicy",
        "ingredients": ["500g chicken wings", "2 fresh bird's eye chillies", "1 tablespoon lemon juice", "2 cloves garlic", "Salt"],
        "instructions": "Blend chillies, garlic, lemon juice and salt. Coat the wings and roast at 200°C for 35 minutes, turning once.",
    },
    {
        "name": "Banana Bread",
        "category": "sweets",
        "ingredients": ["3 ripe bananas", "250g flour", "100g sugar", "75g melted butter", "1 egg", "1 teaspoon baking soda"],
        "instructions": "Mash bananas, mix in butter, sugar and egg. Fold in flour and baking soda. Bake at 175°C for 60 minutes.",
    },
]


def home(request):
    # Rendered from the project-level templates folder (templates/home.html)
    return render(request, "home.html", {"categories": CATEGORIES})


def recipe_list(request):
    # Rendered from the app-level templates folder (recipes/templates/recipes/)
    return render(request, "recipes/recipe_list.html", {"title": "All recipes", "recipes": RECIPES})


def category_detail(request, slug):
    category = CATEGORIES.get(slug)
    if category is None:
        raise Http404("Category not found")
    recipes = [recipe for recipe in RECIPES if recipe["category"] == slug]
    return render(request, "recipes/recipe_list.html", {
        "title": category["name"],
        "tagline": category["tagline"],
        "recipes": recipes,
    })
