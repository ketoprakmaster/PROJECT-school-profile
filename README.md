# School Profile Website

This is a school profile website built with Django and Wagtail, designed to be managed through a headless admin interface. The frontend is built with TailwindCSS and DaisyUI, with htmx for dynamic interactions.

## Features

-   **CMS-driven Content:** Easily editable pages and content blocks via Wagtail admin.
-   **Modern Frontend:** A clean and responsive UI built with TailwindCSS and DaisyUI.
-   **Dynamic Components:** Interactive elements powered by htmx.
-   **Containerized:** Docker support for easy setup and deployment.

## Getting Started

You can run this project in two ways: using Docker or setting it up manually.

### Prerequisites

-   [uv](https://github.com/astral-sh/uv) (for manual setup)
-   [Python 3.11+](https://www.python.org/)
-   [Node.js](https://nodejs.org/en/) (with npm)
-   [Docker](https://www.docker.com/products/docker-desktop/) (for Docker-based setup)

---

### 1. Running with Docker (Recommended)

This is the easiest way to get the project up and running.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

1.  **Build and run the containers:**
    ```bash
    docker-compose up --build -d
    ```

1.  **Access the application:**
    -   **Website:** [http://127.0.0.1:80](http://127.0.0.1:80)
    -   **Wagtail Admin:** [http://127.0.0.1:80/django-cms/](http://127.0.0.1:80/django-cms/)

    A default superuser is created with the following credentials (unless changed in the `.env` file):
    -   **Username:** `admin`
    -   **Password:** `yourpassword`

---

### 2. Manual Installation

Follow these steps to run the project on your local machine without Docker.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install Python dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    # Using uv
    uv sync

    # Or using pip
    pip install -r requirements.txt
    ```

3.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

4.  **Run database migrations:**
    ```bash
    # pip
    python src/manage.py migrate
    
    # uv
    uv src/manage.py migrate
    ```

5.  **Run the development servers:**
    You need to run two processes in separate terminals.

    **Terminal 1: Watch for CSS changes**
    ```bash
    npm run watch:css
    ```

    **Terminal 2: Run the Django server**
    ```bash
    # using uv
    uv src/manage.py runserver

    # or using pip
    python src/manage.py runserver
    ```

6.  **Access the application:**
    -   **Website:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
    -   **Wagtail CMS:** [http://127.0.0.1:8000/django-cms/](http://127.0.0.1:8000/django-cms/)
    -   **Wagtail Admin:** [http://127.0.0.1:8000/django-admin/](http://127.0.0.1:8000/django-admin/)


## Creating a Superuser

If you are running the project manually, you'll need a superuser account to access the admin panel.
```bash
# pip
python src/manage.py createsuperuser

# uv
uv src/manage.py createsuperuser
```
Follow the prompts to create your username, email, and password.

## Building for Production

If you are deploying the application manually, you need to build the frontend assets and collect static files.

1.  **Build Frontend Assets:**
    This command will build and minify the CSS files.
    ```bash
    npm run build:css
    ```

2.  **Collect Static Files:**
    This command collects all static files into a single directory.
    ```bash
    # pip
    python src/manage.py collectstatic

    # uv
    uv src/manage.py collectstatic
    ```
