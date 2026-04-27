🐾 Animal Shelter Adoption & Rescue System
A collaborative Django web application built as a group project, where each team member is responsible for a specific app module to manage an animal shelter's daily operations. The system helps track pets, adopters, staff members, medical records, foster assignments, and adoption processes.

👥 Group Members & Responsibilities
Member	App Module	Models
Lofranco	animals	Pet, MedicalRecord, Vaccination, Veterinary
Alvarado	accounts	Staff (custom user model)
Escuzar	shelter	ShelterBranch, KennelCage, IntakeRecord
Linaban	fostering	FosterAssignment
Nadal	adoptions	Adopter, AdoptionApplication, Interview, HomeVisit, Adoption, Payment
🛠️ Tech Stack
Technology	Version
Backend	Django 6.0.4
Language	Python 3.14
Database	MySQL / SQLite3
Frontend	HTML5, CSS3, Bootstrap 5
Icons	Font Awesome 6
📁 Project Structure
text
shelter_management/
├── shelter_management/          # Project settings, root URLs, WSGI
├── apps/
│   ├── accounts/                # Staff identity and authentication system
│   ├── animals/                 # Pet, medical records, vaccinations
│   ├── shelter/                 # Shelter branches, kennels, intake records
│   ├── fostering/               # Foster assignments and tracking
│   └── adoptions/               # Adopters, applications, adoptions, payments
├── templates/                   # HTML templates for all apps
├── static/                      # CSS, JS, and images
└── manage.py                    # Django management script
📱 App Modules
accounts (Alvarado)
Staff — Custom user model with role-based access (Admin, Manager, Vet, Staff, Volunteer)

Includes login/logout views and profile management

Only Admin can create, edit, or delete staff accounts

animals (Lofranco)
Pet — name, species, breed, age, sex, size, color, status

MedicalRecord — visit date, diagnosis, treatment, weight, FK → Pet, FK → Veterinary

Vaccination — vaccine name, dose number, vaccination date, next due date, FK → Pet, FK → Veterinary

Veterinary — veterinarian directory with license numbers

Validation: Visit date cannot be future, next due date must be after vaccination date

shelter (Escuzar)
ShelterBranch — name, address, city, contact number, email

KennelCage — kennel code, type, capacity, current occupancy, status, FK → ShelterBranch

IntakeRecord — intake type (Stray, Surrender, Rescue), condition notes, FK → Pet, FK → ShelterBranch, FK → Staff

Validation: Occupancy cannot exceed capacity, one intake record per pet

fostering (Linaban)
FosterAssignment — foster name, phone, address, start date, end date, status, FK → Pet

Validation: No multiple active fosters for same pet, end date must be after start date

adoptions (Nadal)
Adopter — first name, last name, email, phone, address, date of birth, has other pets, has children

AdoptionApplication — status (Pending, Approved, Rejected), interview schedule, notes, FK → Adopter, FK → Pet, FK → Staff

Interview — interview date/time, result (Pass/Fail), remarks, FK → Application

HomeVisit — visit date, result (Pass/Fail), remarks, FK → Application

Adoption — adoption date, fee, status (Completed/Cancelled), FK → Application, FK → Pet, FK → Adopter, FK → Staff

Payment — amount, method (Cash, GCash, Card), reference number, status, FK → Adoption

Validation: Adopter must be 18+ years old, max 3 pending applications, amount must match adoption fee

🚀 Setup & Installation
1. Clone the repository
bash
git clone https://github.com/carlos09123123/CSIT327.git
cd CSIT327
2. Create and activate virtual environment
Windows (PowerShell):

powershell
python -m venv venv
venv\Scripts\Activate.ps1
Mac / Linux:

bash
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
bash
pip install django
pip install Pillow
pip install mysqlclient  # If using MySQL
4. Configure database
Option A: SQLite (Default - No configuration needed)

Option B: MySQL

sql
CREATE DATABASE shelter_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
Update settings.py:

python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shelter_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
5. Apply migrations
bash
python manage.py makemigrations accounts
python manage.py makemigrations animals
python manage.py makemigrations shelter
python manage.py makemigrations fostering
python manage.py makemigrations adoptions
python manage.py migrate
6. Create a superuser
bash
python manage.py createsuperuser
Follow the prompts:

text
Username: admin
Email: admin@example.com
Password: admin123
7. Run the development server
bash
python manage.py runserver 8080
Then open http://127.0.0.1:8080/ in your browser.

🔗 URL Routes
URL	View	Access
/	Home / Dashboard	Staff, Admin, Vet
/login/	Login page	Public
/logout/	Logout	Authenticated users
/register/	Adopter registration	Public
/adopter-dashboard/	Adopter dashboard	Adopter only
/animals/	Pet list	Staff, Admin, Vet
/animals/add-pet/	Add new pet	Staff, Admin
/animals/<int:pk>/	Pet details	Staff, Admin, Vet
/animals/medical-records/	Medical records list	Staff, Admin, Vet
/animals/medical-stats/	Medical statistics	Vet, Staff, Admin
/animals/vets/	Veterinarian directory	Staff, Admin, Vet
/shelter/	Shelter branches	Staff, Admin
/shelter/kennels/	Kennel management	Staff, Admin
/shelter/intakes/	Intake records	Staff, Admin
/fostering/	Foster assignments	Staff, Admin
/adoptions/	Adoption records	Staff, Admin
/adoptions/applications/	Adoption applications	Staff, Admin
/adoptions/interviews/	Interview management	Staff, Admin
/adoptions/homevisits/	Home visit management	Staff, Admin
/adoptions/payments/	Payment records	Staff, Admin
/adoptions/terms-waiver/	Adoption waiver	Public
/accounts/	Staff management	Admin only
/accounts/profile/	User profile	Authenticated users
/admin/	Django admin panel	Admin only
👑 Admin Panel
All models are registered in the Django admin with appropriate list displays, filters, search fields, and inline views.

Default superuser (development only):

Username: admin

Password: admin123

Admin panel URL: http://127.0.0.1:8080/admin/

🔐 Role-Based Access Control
Role	Access Level
Admin	Full system access (all apps, staff management)
Manager	Full access except staff management
Staff	Access to animals, shelter, fostering, adoptions
Veterinarian	View pets, manage medical records, view statistics
Adopter	Dashboard, available pets, applications only
Volunteer	Read-only access (future implementation)
📊 Business Rules Implemented
Rule	Entity	Status
Auto-generated IDs	All entities	✅
Email must be unique	Adopter, Veterinary, Shelter, Staff	✅
Username must be unique	Staff	✅
Adopter must be ≥ 18 years old	Adopter	✅
Max 3 pending applications	Adopter	✅
No multiple active fosters	FosterAssignment	✅
Occupancy cannot exceed capacity	KennelCage	✅
One intake record per pet	IntakeRecord	✅
Visit date cannot be future	MedicalRecord	✅
Next due date after vaccination date	Vaccination	✅
Amount must match adoption fee	Payment	✅
Application must be approved before adoption	Adoption	✅
🌿 Git Branches
Branch	Member	Status
main	Lofranco	Active — all apps integrated
alvarado-branch	Alvarado	Integrated
escuzar-branch	Escuzar	Integrated
linaban-branch	Linaban	Integrated
nadal-branch	Nadal	Integrated
