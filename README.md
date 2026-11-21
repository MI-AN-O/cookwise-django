# CookWise

A recipe-sharing web application built with Django for the Application Programming for the Internet semester project.

## The idea

1. **What problem does it solve?** Home cooks have recipes scattered across notebooks, WhatsApp chats and videos, and struggle to decide what to cook with what they already have.
2. **Who will use it?** Home cooks and students who want to save, share and discover recipes.
3. **What can users do?** Browse recipes by category (sweets, spicy, main dishes, appetisers), sign up and log in, and add, edit and delete their own recipes. Later in the semester: search by ingredient and save favourites.

## Models, forms and authentication

| Part | Where | What it does |
| --- | --- | --- |
| `Category` model | `recipes/models.py` | Sweets, Spicy, Main dishes, Appetisers (seeded by migration `0002`) |
| `Recipe` model | `recipes/models.py` | Title, category, author (a `User`), prep time, ingredients, instructions, timestamps |
| `RecipeForm` | `recipes/forms.py` | `ModelForm` for adding/editing recipes; needs at least two ingredients, one per line |
| `SignUpForm` | `accounts/forms.py` | Extends Django's `UserCreationForm` with a required, unique email |
| Sign up | `accounts/views.py` | Creates the account and logs the user straight in |
| Log in / log out | `django.contrib.auth.urls` | Django's built-in views, using `templates/registration/` |

Rules: anyone can browse recipes; only logged-in users can add one; only a recipe's author can edit or delete it (other users get a 404). Both models are registered in the Django admin.

## Project structure

```
cookwise-django/
├── config/                 # Project configuration (settings, urls, wsgi, asgi)
├── accounts/               # Sign-up form and view (login/logout use Django's built-in views)
├── recipes/                # Recipes app
│   ├── migrations/         # 0001 creates the tables, 0002 loads the sample data
│   ├── templates/recipes/  # App-level templates
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/              # Project-level templates (base, home, registration/ for auth pages)
├── static/                 # CSS and images
└── manage.py
```

## Running locally

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Then open http://127.0.0.1:8000/.

| URL | Page | Template location |
| --- | --- | --- |
| `/` | Home - recipe categories | Project level: `templates/home.html` |
| `/recipes/` | All recipes | App level: `recipes/templates/recipes/recipe_list.html` |
| `/recipes/<category>/` | Recipes in one category | App level |
| `/recipes/<id>/` | One recipe | App level |
| `/recipes/new/`, `/recipes/<id>/edit/`, `/recipes/<id>/delete/` | Add, edit, delete (login required) | App level |
| `/recipes/mine/` | The logged-in user's recipes | App level |
| `/accounts/signup/`, `/accounts/login/` | Sign up, log in (log out is a button in the menu) | Project level: `templates/registration/` |
| `/admin/` | Django admin | Built in |

Run the tests with `python manage.py test`.
