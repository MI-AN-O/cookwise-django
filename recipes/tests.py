from django.test import TestCase
from django.urls import reverse


class PageTests(TestCase):
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
