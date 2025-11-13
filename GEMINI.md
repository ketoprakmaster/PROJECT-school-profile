# Gemini Project Context: School Profile Website

## Project Overview

This is a school profile website built using the Django web framework and the Wagtail Headless CMS. The primary purpose is to provide a comprehensive school profile that is manageable through a user-friendly admin interface.

- **Backend:** Python, Django, Wagtail CMS
- **Frontend:** TailwindCSS, DaisyUI, htmx
- **Database:** SQLite (for development), PostgreSQL (configured for production)
- **Python Environment:** Managed via `uv` and `pyproject.toml`.

### Architecture

- The project follows a standard Django structure with a `src` directory.
- **`core` app:** Contains project-wide settings, URL configurations, and base templates.
- **`home` app:** Manages the main landing page (`HomePage` model).
- **`themes` app:** Manages frontend assets. CSS source files are located in `src/themes/source/css` and are compiled into `src/themes/static/css` using TailwindCSS.
- Content is made editable through Wagtail's `StreamField` and other field types in the `home/models.py` file.

## Building and Running

### 1. Setup

**Backend:**
Install Python dependencies using `uv`.
```bash
uv pip install -r requirements.txt
```

**Frontend:**
Install Node.js dependencies.
```bash
npm install
```

### 2. Running the Development Server

You need to run two processes in separate terminals.

**Terminal 1: Watch for CSS changes**
This command compiles your TailwindCSS files automatically as you make changes.
```bash
npm run watch:css
```

**Terminal 2: Run the Django server**
```bash
python src/manage.py runserver
```

The website will be available at `http://127.0.0.1:8000`.
The Wagtail admin panel is at `http://127.0.0.1:8000/django-cms/`.

### 3. Building for Production

**Frontend:**
Build and minify the CSS files.
```bash
npm run build:css
```

**Backend:**
Collect all static files into a single directory.
```bash
python src/manage.py collectstatic
```

## Development Conventions

- **Settings:** Django settings are split into `base.py`, `dev.py`, and `production.py` inside `src/core/settings/`.
- **Wagtail Models:** New editable pages or content types should be defined as models in their respective app's `models.py` file (e.g., `src/home/models.py`).
- **Migrations:** After changing a model, run `python src/manage.py makemigrations <app_name>` and `python src/manage.py migrate`.
- **Superuser:** To access the admin panel, a superuser is required. If one doesn't exist, create one:
  ```bash
  python src/manage.py createsuperuser
  ```
- **Templates:** HTML templates are located in `src/templates/`. The base template is `src/templates/common/base.html`.
