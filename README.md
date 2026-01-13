
# School Profile Website

A modern school profile website built with **Django** and **Wagtail CMS**. It features a headless-ready admin interface, a responsive frontend using **TailwindCSS** and **DaisyUI**, and dynamic interactions powered by **htmx**.

## Features

-   **Wagtail CMS:** Fully editable pages and flexible content blocks.
-   **Modern UI:** Responsive design using TailwindCSS + DaisyUI.
-   **Dynamic UX:** Seamless page updates without full reloads via htmx.
-   **Zero-Config Docker:** Run the entire app with a single command using SQLite.
    
----------

## 🚀 Quick Start (Docker)

This is the easiest way to run the project. It uses a single container with a local SQLite database, meaning you don't need to set up PostgreSQL or Nginx to get started.

### **1. Create a docker-compose.yaml**
Save the following content into a file named `docker-compose.yml`:
``` yaml
services:
  web:
    image: ghcr.io/ketoprakmaster/project-school-profile:main
    ports:
      - "8000:8000"
    volumes:
      - data_volume:/app/src/data
    environment:
      - DJANGO_SETTINGS_MODULE=core.settings.dev
      - DJANGO_SUPERUSER_USERNAME=admin
      - DJANGO_SUPERUSER_PASSWORD=12345
      - DJANGO_SUPERUSER_EMAIL=admin@example.com
      - SECRET_KEY=changeme

volumes:
  data_volume:
```

### **2.  Launch the Application:**
  run this command in your terminal
  ``` bash
  docker compose up
  ```
    
### **3.  Access the Site:**
  - Website: http://localhost:8000
  - Admin Panel: http://localhost:8000/django-cms/
    - Username: admin
    - Password: 12345
        

----------

## 🛠️ **Local Development**

Follow these steps to set up the project locally for development.

### **Prerequisites**

-   **Python 3.11+** (Managed via [uv](https://docs.astral.sh/uv/) recommended)
    
-   **Node.js & npm** (For TailwindCSS compilation)
    

### **1. Clone the repository**

``` bash
# Clone the repository
git clone https://github.com/ketoprakmaster/project-school-profile
cd project-school-profile
```

### **2. install required dependencies**
``` bash
# Install python dependencies with uv
uv sync 

# or install with pip 
pip install -r requirements.txt

# Install Node dependencies
npm install
```

### **3. Initialize Database**

```bash
# Run migrations
uv run src/manage.py migrate

# Create your admin account
uv run src/manage.py createsuperuser
```

### **4. Run Development Servers**

You need to run the Django server and the Tailwind compiler simultaneously:

**Django Server**
```bash
uv run src/manage.py runserver
```
**Tailwind Watch**
```bash
npm run watch:css
```
    
----------

## UI UX Design
The UI/UX design for this project was created to ensure a modern, clean, and user-friendly school profile website, with a strong focus on readability, responsiveness, and content hierarchy.

UI/UX Design Link : https://drive.google.com/drive/folders/1s2Eo6RJ3zaoq6Tew2cQ8yO7rgw0mGx4k?usp=sharing
