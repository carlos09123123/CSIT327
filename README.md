🐾 Animal Shelter Adoption & Rescue System

📋 Project Overview

The Animal Shelter Adoption & Rescue System is a comprehensive web-based platform designed to manage an animal shelter's daily operations. The system helps track pets, adopters, staff members, medical records, foster assignments, and adoption processes, ensuring that animals are properly cared for and placed in loving homes safely.


Quick Start Commands

**Step 1: Activate Virtual Environment**
Windows (PowerShell):**

powershell
venv\Scripts\Activate.ps1
Windows (Command Prompt):

cmd
venv\Scripts\activate.bat

**Step 2: Install Dependencies (First Time Only)**
bash
pip install -r requirements.txt
Or install manually:

bash
pip install django
pip install Pillow

**Step 3: Run Migrations**
bash
python manage.py migrate

**Step 4: Create Superuser (Admin Account)**
bash
python manage.py createsuperuser
Follow the prompts:

text
Username: admin
Email: admin@example.com
Password: admin123

**Step 5: Start the Server**
bash
python manage.py runserver 8080

**Step 6: Open Browser**
Go to: http://127.0.0.1:8080/

**Step 8: Login**
Staff/Admin: Username admin, Password admin123

Adopter: Use your registered email and password

🛠️ Technologies Used
Backend Framework: Django 6.0.4

Database: MySQL / SQLite3

Frontend: HTML5, CSS3, Bootstrap 5

Languages: Python 3.14

Authentication: Django's built-in authentication system with custom Staff model

