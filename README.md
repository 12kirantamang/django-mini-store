# 🛒 Django Mini Store

&gt; A simple yet functional eCommerce web application built with Django, designed for small-scale online retail operations.

![Django](https://img.shields.io/badge/Django-4.x-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

**Django Mini Store** is a lightweight eCommerce platform that enables users to browse products, manage shopping carts, and place orders. It includes a comprehensive admin panel for store management.

### Target Users
- Online shoppers looking for a simple buying experience
- Small business owners needing a basic store management system
- Developers learning Django eCommerce patterns

---

## 🌐 Demo

**Local Demo:** `http://localhost:8000/`



| Home Page | Product List | Cart Page | Admin Panel |
|-----------|-------------|-----------|-------------|
| ![Home](https://github.com/user-attachments/assets/bf90586c-2fee-4950-b06a-e22d31486b70) | ![Product List](https://github.com/user-attachments/assets/c25f8ec8-8904-49a3-bd56-5d32f96c6111) | ![Cart](https://github.com/user-attachments/assets/63826cae-0d9c-470d-90ba-d4e7ef63bc44) | <img width="1911" height="943" alt="Screenshot From 2026-04-28 15-48-53" src="https://github.com/user-attachments/assets/bca5a818-7384-4e63-a71b-9795fe1497bc" />


## 🚀 Features

### 👤 User Features
| Feature | Description |
|---------|-------------|
| **User Registration & Login** | Secure account creation and authentication |
| **Product Browsing** | View all products with details |
| **Add to Cart** | Select items and manage quantities |
| **Cart Management** | Update quantities or remove items |
| **Order Placement** | Complete checkout process |

### 🔧 Admin Features
| Feature | Description |
|---------|-------------|
| **Product Management** | Create, Read, Update, Delete (CRUD) products |
| **User Management** | View and manage registered users |
| **Order Management** | Track and process customer orders |

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Python 3.9+, Django 4.x |
| **Database** | SQLite (Development) / MySQL (Production) |
| **Frontend** | HTML, CSS, JavaScript |
| **Authentication** | Django Built-in Auth |


---

## 🗄️ Database Design (ER Diagram)

![ER Diagram]<img width="1387" height="987" alt="image" src="https://github.com/user-attachments/assets/fd4f25dc-e810-4d24-9229-cded9b396f13" />


### Entity Relationships
- **User** → **Cart** (One-to-Many)
- **User** → **Order** (One-to-Many)
- **Order** → **OrderItem** (One-to-Many)
- **Product** → **OrderItem** (One-to-Many)
- **Product** → **Cart** (One-to-Many)

## 🏗️ Infrastructure Diagram

![Infrastructure Diagram]<img width="1187" height="1387" alt="image (1)" src="https://github.com/user-attachments/assets/b12569d2-248d-460a-9270-5ad4aabf2bd6" />


### Architecture Overview
| Layer | Technology | Role |
|-------|-----------|------|
| Client | Web Browser | User interface |
| Web Server | Nginx + Gunicorn | Reverse proxy, SSL, static files |
| Application | Django | Business logic, templates, admin |
| Database | SQLite/MySQL/PostgreSQL | Data persistence |

### Request Flow
1. **Client** sends HTTPS request
2. **Nginx** handles SSL and routes to Gunicorn
3. **Gunicorn** passes WSGI request to Django
4. **Django** processes logic and queries database via ORM
5. **Database** returns data
6. Response flows back up to client

## 📦 Installation

### Prerequisites
- Python 3.9+
- pip
- Git

### Setup Steps

```bash
# 1. Clone repository
git clone https://github.com/12kirantamang/django-mini-store.git
cd django-mini-store

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Create superuser (admin)
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver

# 8. Access application
# User site: http://localhost:8000/
# Admin panel: http://localhost:8000/admin/


