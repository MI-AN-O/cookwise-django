from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import RecipeForm
from .models import Category, Recipe

User = get_user_model()


class PageTests(TestCase):
    """Public pages, using the sample data loaded by the 0002 migration."""

    def test_home_uses_project_level_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Sweets")

    def test_recipe_list_uses_app_level_template(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_list.html")
        self.assertContains(response, "Spaghetti Carbonara")

    def test_category_shows_only_its_recipes(self):
        response = self.client.get(reverse("recipes:category_detail", args=["sweets"]))
        self.assertContains(response, "Banana Bread")
        self.assertNotContains(response, "Garlic Bread")

    def test_unknown_category_returns_404(self):
        response = self.client.get(reverse("recipes:category_detail", args=["soups"]))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_lists_ingredients(self):
        recipe = Recipe.objects.get(title="Banana Bread")
        response = self.client.get(recipe.get_absolute_url())
        self.assertContains(response, "3 ripe bananas")
        self.assertContains(response, "CookWise team")


class ModelTests(TestCase):
    def test_ingredient_list_skips_blank_lines(self):
        recipe = Recipe(ingredients="1 egg\n\n  2 cups flour  \n")
        self.assertEqual(recipe.ingredient_list(), ["1 egg", "2 cups flour"])

    def test_str(self):
        self.assertEqual(str(Category.objects.get(slug="spicy")), "Spicy")


class RecipeFormTests(TestCase):
    def data(self, **overrides):
        data = {
            "title": "Chapati",
            "category": Category.objects.get(slug="main-dishes").pk,
            "prep_time": 40,
            "ingredients": "2 cups flour\n\n1 cup warm water\n",
            "instructions": "Knead, rest, roll and fry.",
        }
        data.update(overrides)
        return data

    def test_valid_form_cleans_ingredients(self):
        form = RecipeForm(self.data())
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["ingredients"], "2 cups flour\n1 cup warm water")

    def test_needs_two_ingredients(self):
        form = RecipeForm(self.data(ingredients="2 cups flour"))
        self.assertIn("ingredients", form.errors)

    def test_prep_time_cannot_be_zero(self):
        form = RecipeForm(self.data(prep_time=0))
        self.assertIn("prep_time", form.errors)

    def test_title_required(self):
        form = RecipeForm(self.data(title=""))
        self.assertIn("title", form.errors)


class RecipeCrudTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user("wanjiru", password="pass12345!")
        self.other = User.objects.create_user("otieno", password="pass12345!")
        self.category = Category.objects.get(slug="main-dishes")
        self.recipe = Recipe.objects.create(
            title="Githeri",
            category=self.category,
            author=self.author,
            ingredients="2 cups maize\n1 cup beans",
            instructions="Boil together until soft.",
        )

    def test_create_requires_login(self):
        url = reverse("recipes:recipe_create")
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_logged_in_user_can_create_recipe(self):
        self.client.login(username="otieno", password="pass12345!")
        response = self.client.post(reverse("recipes:recipe_create"), {
            "title": "Ugali",
            "category": self.category.pk,
            "ingredients": "2 cups maize flour\n3 cups water",
            "instructions": "Boil water, add flour, stir until firm.",
        })
        recipe = Recipe.objects.get(title="Ugali")
        self.assertEqual(recipe.author, self.other)
        self.assertRedirects(response, recipe.get_absolute_url())

    def test_author_can_edit(self):
        self.client.login(username="wanjiru", password="pass12345!")
        response = self.client.post(reverse("recipes:recipe_update", args=[self.recipe.pk]), {
            "title": "Githeri Special",
            "category": self.category.pk,
            "ingredients": "2 cups maize\n1 cup beans\n1 onion",
            "instructions": "Boil, then fry with onion.",
        })
        self.assertRedirects(response, self.recipe.get_absolute_url())
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, "Githeri Special")

    def test_other_user_cannot_edit_or_delete(self):
        self.client.login(username="otieno", password="pass12345!")
        edit = self.client.get(reverse("recipes:recipe_update", args=[self.recipe.pk]))
        delete = self.client.post(reverse("recipes:recipe_delete", args=[self.recipe.pk]))
        self.assertEqual(edit.status_code, 404)
        self.assertEqual(delete.status_code, 404)
        self.assertTrue(Recipe.objects.filter(pk=self.recipe.pk).exists())

    def test_edit_buttons_only_shown_to_author(self):
        self.client.login(username="otieno", password="pass12345!")
        response = self.client.get(self.recipe.get_absolute_url())
        self.assertNotContains(response, "Edit</a>")

    def test_author_can_delete(self):
        self.client.login(username="wanjiru", password="pass12345!")
        response = self.client.post(reverse("recipes:recipe_delete", args=[self.recipe.pk]))
        self.assertRedirects(response, reverse("recipes:my_recipes"))
        self.assertFalse(Recipe.objects.filter(pk=self.recipe.pk).exists())

    def test_my_recipes_only_shows_own(self):
        self.client.login(username="otieno", password="pass12345!")
        response = self.client.get(reverse("recipes:my_recipes"))
        self.assertNotContains(response, "Githeri")
