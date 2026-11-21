from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "category", "prep_time", "ingredients", "instructions"]
        widgets = {
            "ingredients": forms.Textarea(attrs={"rows": 6, "placeholder": "200g spaghetti\n2 large eggs"}),
            "instructions": forms.Textarea(attrs={"rows": 6}),
        }

    def clean_ingredients(self):
        # Drop blank lines and stray spaces so each line is one clean ingredient
        lines = [line.strip() for line in self.cleaned_data["ingredients"].splitlines() if line.strip()]
        if len(lines) < 2:
            raise forms.ValidationError("Please list at least two ingredients, one per line.")
        return "\n".join(lines)

    def clean_prep_time(self):
        prep_time = self.cleaned_data["prep_time"]
        if prep_time is not None and prep_time == 0:
            raise forms.ValidationError("Preparation time must be at least 1 minute.")
        return prep_time
