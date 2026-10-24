# CookWise

A recipe-sharing web application built with Django for the Application Programming for the Internet semester project.

## The idea

1. **What problem does it solve?** Home cooks have recipes scattered across notebooks, WhatsApp chats and videos, and struggle to decide what to cook with what they already have.
2. **Who will use it?** Home cooks and students who want to save, share and discover recipes.
3. **What can users do?** Browse recipes by category (sweets, spicy, main dishes, appetisers). Later in the semester: register and log in, add/edit/delete their own recipes, search by ingredient, and save favourites.

## Project structure

```
cookwise-django/
├── config/                 # Project configuration (settings, urls, wsgi, asgi)
├── recipes/                # Django app
│   ├── templates/recipes/  # App-level templates
│   ├── urls.py
│   └── views.py
├── templates/              # Project-level templates (base.html, home.html)
├── static/                 # CSS and images
└── manage.py
```

## Running locally

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/.

| URL | Page | Template location |
| --- | --- | --- |
| `/` | Home - recipe categories | Project level: `templates/home.html` |
| `/recipes/` | All recipes | App level: `recipes/templates/recipes/recipe_list.html` |
| `/recipes/<category>/` | Recipes in one category | App level |

Run the tests with `python manage.py test`.
