"""Load the categories and sample recipes that used to live as a Python list in views.py."""

from django.db import migrations

CATEGORIES = [
    ("sweets", "Sweets", "Bake it like you mean it.", "pexels-catscoming-3752075.jpg"),
    ("spicy", "Spicy", "A little goes a long way.", "pexels-pixabay-70842.jpg"),
    ("main-dishes", "Main dishes", "Find your next favourite dish.", "pexels-catscoming-1907244.jpg"),
    ("appetisers", "Appetisers", "Small bites to start the meal right.", "IMAGE7.jpeg"),
]

RECIPES = [
    {
        "title": "Spaghetti Carbonara",
        "category": "main-dishes",
        "prep_time": 25,
        "ingredients": ["200g spaghetti", "100g pancetta", "2 large eggs", "50g pecorino cheese", "Salt and pepper", "Fresh parsley"],
        "instructions": "Cook spaghetti. Fry pancetta. Beat eggs with cheese, add to pasta off heat. Mix in pancetta. Serve with parsley.",
    },
    {
        "title": "Vegetable Stir-Fry",
        "category": "main-dishes",
        "prep_time": 15,
        "ingredients": ["2 cups mixed vegetables (bell peppers, broccoli, carrots)", "2 tablespoons soy sauce", "1 tablespoon olive oil", "1 clove garlic, minced", "Salt and pepper"],
        "instructions": "Heat oil, add garlic, and stir-fry vegetables for 5-7 minutes. Add soy sauce and cook for another minute.",
    },
    {
        "title": "Garlic Bread",
        "category": "appetisers",
        "prep_time": 15,
        "ingredients": ["1 baguette", "3 tablespoons butter, softened", "2 cloves garlic, minced", "Fresh parsley"],
        "instructions": "Mix butter, garlic and parsley. Spread on sliced baguette and bake at 200°C for 8-10 minutes.",
    },
    {
        "title": "Pili Pili Chicken Wings",
        "category": "spicy",
        "prep_time": 45,
        "ingredients": ["500g chicken wings", "2 fresh bird's eye chillies", "1 tablespoon lemon juice", "2 cloves garlic", "Salt"],
        "instructions": "Blend chillies, garlic, lemon juice and salt. Coat the wings and roast at 200°C for 35 minutes, turning once.",
    },
    {
        "title": "Banana Bread",
        "category": "sweets",
        "prep_time": 75,
        "ingredients": ["3 ripe bananas", "250g flour", "100g sugar", "75g melted butter", "1 egg", "1 teaspoon baking soda"],
        "instructions": "Mash bananas, mix in butter, sugar and egg. Fold in flour and baking soda. Bake at 175°C for 60 minutes.",
    },
]


def seed(apps, schema_editor):
    Category = apps.get_model("recipes", "Category")
    Recipe = apps.get_model("recipes", "Recipe")
    categories = {}
    for slug, name, tagline, image in CATEGORIES:
        categories[slug] = Category.objects.create(slug=slug, name=name, tagline=tagline, image=image)
    for data in RECIPES:
        Recipe.objects.create(
            title=data["title"],
            category=categories[data["category"]],
            prep_time=data["prep_time"],
            ingredients="\n".join(data["ingredients"]),
            instructions=data["instructions"],
        )


def unseed(apps, schema_editor):
    Category = apps.get_model("recipes", "Category")
    Recipe = apps.get_model("recipes", "Recipe")
    Recipe.objects.filter(author__isnull=True, title__in=[r["title"] for r in RECIPES]).delete()
    Category.objects.filter(slug__in=[c[0] for c in CATEGORIES], recipes__isnull=True).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
