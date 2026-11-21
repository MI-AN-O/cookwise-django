from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    tagline = models.CharField(max_length=150, blank=True)
    # Name of a file inside static/images/ used as the category banner
    image = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recipes:category_detail", args=[self.slug])


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="recipes")
    # Null only for the sample recipes that ship with the site
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes",
        null=True,
        blank=True,
    )
    prep_time = models.PositiveIntegerField("preparation time (minutes)", null=True, blank=True)
    ingredients = models.TextField(help_text="One ingredient per line.")
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:recipe_detail", args=[self.pk])

    def ingredient_list(self):
        return [line.strip() for line in self.ingredients.splitlines() if line.strip()]
