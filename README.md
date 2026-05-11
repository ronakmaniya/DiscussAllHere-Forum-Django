# DiscussAllHere-Forum-Django

A discussion forum built with Django. Includes categories, threaded comments, search, and simple moderation tools.

## Live Website

- Production URL: https://discussallhere.onrender.com
- Hosting Platform: Render (https://render.com/)

## Features

- User signup, login, logout
- Category-based discussions and global discussion list
- Create discussions and add comments (with reply support)
- Delete own discussions and comments
- Search by discussion title
- About/Help page

## Project Structure

```bash

DiscussAllHere-Forum-Django/
│── DiscussAllHere/        # Main project settings
│   ├── settings.py
│   ├── urls.py
│
│── forum/                 # Forum app
│   ├── migrations/
│   ├── templates/forum/   # HTML templates
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
│── db.sqlite3             # Local development DB
│── manage.py              # Django management script
│── requirements.txt       # Dependencies

```

## Setup & Run

## Environment

Create a local .env file from the example and adjust values as needed:

```bash
copy .env.example .env         # Windows PowerShell
cp .env.example .env           # macOS/Linux
```

Required values for production:
- DJANGO_SECRET_KEY
- DJANGO_DEBUG=false
- DJANGO_ALLOWED_HOSTS
- DATABASE_URL (optional; SQLite works for small demos)

The app reads from system environment variables first and falls back to .env.

```bash
# Clone the repo
git clone https://github.com/ronakmaniya/DiscussAllHere-Forum-Django.git
cd DiscussAllHere-Forum-Django

# Create a virtual environment in the project root
python -m venv venv

# Install dependencies (Windows PowerShell)
venv\Scripts\python -m pip install -r requirements.txt

# Install dependencies (macOS/Linux)
venv/bin/python -m pip install -r requirements.txt

# Database setup (first run after clone)
venv\Scripts\python manage.py migrate      # Windows PowerShell
venv/bin/python manage.py migrate           # macOS/Linux

# Run server
venv\Scripts\python manage.py runserver     # Windows PowerShell
venv/bin/python manage.py runserver          # macOS/Linux
```

## Migrations

- Run `venv\Scripts\python manage.py makemigrations` (Windows) or `venv/bin/python manage.py makemigrations` (macOS/Linux) only when you change models.
- Run `venv\Scripts\python manage.py migrate` (Windows) or `venv/bin/python manage.py migrate` (macOS/Linux) after pulling new migrations or on a fresh clone.

## Admin Access

If you want to use the Django admin:

```bash
venv\Scripts\python manage.py createsuperuser     # Windows PowerShell
venv/bin/python manage.py createsuperuser          # macOS/Linux
```

Then start the server and open http://127.0.0.1:8000/admin/ to log in.

## Notes

- The development server runs at http://127.0.0.1:8000/
- Use `CTRL+BREAK` to stop the server on Windows

## Deployment (Render)

### Build and Start Commands

Use the included build script and gunicorn start command:

```bash
./build.sh
gunicorn DiscussAllHere.wsgi
```

### Render Setup

1. Push the project to GitHub.
2. Create a Render Web Service and connect your repo.
3. Set Build Command: `./build.sh`
4. Set Start Command: `gunicorn DiscussAllHere.wsgi`
5. Add environment variables:
	- DJANGO_SECRET_KEY
	- DJANGO_DEBUG=false
	- DJANGO_ALLOWED_HOSTS=yourapp.onrender.com
	- DATABASE_URL (optional)

If static files do not load, run:

```bash
venv\Scripts\python manage.py collectstatic --noinput
```
