🐾 Animal Shelter Adoption & Rescue System
📋 Project Overview

The Animal Shelter Adoption & Rescue System is a comprehensive web-based platform designed to manage an animal shelter's daily operations.

This system helps track:

🐶 Pets
👤 Adopters
🧑‍⚕️ Staff members
💉 Medical records
🏠 Foster assignments
📄 Adoption processes

It ensures that animals are properly cared for and placed in loving homes safely.

🚀 Quick Start Guide
🔹 Step 1: Activate Virtual Environment

Windows (PowerShell):

venv\Scripts\Activate.ps1

Windows (Command Prompt):

venv\Scripts\activate.bat
🔹 Step 2: Install Dependencies (First Time Only)

Using requirements file:

pip install -r requirements.txt

Or install manually:

pip install django
pip install Pillow
🔹 Step 3: Run Migrations
python manage.py migrate
🔹 Step 4: Create Superuser (Admin Account)
python manage.py createsuperuser

Follow the prompts:

Username: admin
Email: admin@example.com
Password: admin123
🔹 Step 5: Start the Server
python manage.py runserver 8080
🔹 Step 6: Open in Browser

Go to:

http://127.0.0.1:8080/
🔹 Step 7: Login Credentials

Admin / Staff:

Username: admin
Password: admin123

Adopter:

Use your registered email and password
🛠️ Technologies Used
Backend Framework: Django 6.0.4
Database: MySQL / SQLite3
Frontend: HTML5, CSS3, Bootstrap 5
Language: Python 3.14
Authentication: Django built-in authentication system with custom Staff model
