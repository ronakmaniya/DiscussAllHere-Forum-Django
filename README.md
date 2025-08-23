# DiscussAllHere-Forum-Django

A simple discussion forum built with **Django** 🐍✨

## Features

- User signup & login
- Create new discussions
- List all discussions
- View discussion details
- Separate templates for logged-in and non-logged-in users

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

```bash
# Clone the repo
git clone https://github.com/YourUsername/DiscussAllHere-Forum-Django.git
cd DiscussAllHere-Forum-Django

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# After clone and before Run server, run the given commands first
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver
```
