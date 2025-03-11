
---

# AUSee - Anonymous Course Reviews for AUC

AUSee is an anonymous course review platform designed for Amsterdam University College (AUC) students. It empowers you to share honest opinions about courses while maintaining anonymity, helping others make informed decisions about their course selections.

---

## Table of Contents
- [Overview](#overview)
- [Our Mission](#our-mission)
- [Review Guidelines & Disclaimer](#review-guidelines--disclaimer)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Local Setup](#local-setup)
  - [Testing the Setup](#testing-the-setup)
- [Contributing](#contributing)
- [Learning Django](#learning-django)
- [Supporting AUSee](#supporting-ausee)
- [License](#license)

---

## Overview

AUSee is built on Django and follows a decentralized, community-driven approach. It’s developed by students for students, ensuring that every voice is heard without centralizing the power to moderate content.

---

## Our Mission

We believe that **shared knowledge and experiences** can help the student community. By maintaining anonymity, we encourage openness and honest feedback while fostering a respectful and constructive environment. AUSee is built on the principle of a **horizontal, decentralized structure** where all students can actively participate in adding and moderating courses and reviews. Our goal is to create an anarchic, self-governing space where students **collectively maintain the platform**, ensuring **transparency** and inclusivity in course evaluations. We discourage features that centralize the power to moderate content.&#x20;

---

## Review Guidelines & Disclaimer

**Review Guidelines:**
- **No hateful or discriminatory comments.**
- **Be honest but constructive.**
- **Provide clear and factual reviews.**
- **Follow our [Terms of Use](#) for more details.**

**Disclaimer:**  
The opinions expressed in reviews are solely those of the users and do not represent the official views of the developers or AUC.

---

## Getting Started

### Prerequisites
Before setting up AUSee locally, ensure you have the following:
- **Python 3.8 or later**
- **Git**
- **pip (Python package manager)**
- **Virtualenv** (optional but recommended)
- **PostgreSQL**

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/ausee.git
   cd ausee
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv  # Create the virtual environment
   source venv/bin/activate  # Activate on Linux/Mac
   # For Windows:
   # venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database:**
   Run migrations:
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to see the site.

### Local Setup

Follow these steps to configure and run the project locally with your custom environment settings:

1. **Create a Local `.env` File in the Project Root:**
   ```bash
   touch .env
   nano .env
   ```
   Add the following environment variables:
   ```plaintext
   DEBUG=True
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=postgres://username:password@localhost:5432/ausee_db
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

2. **Create a Local PostgreSQL Database:**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE ausee_db;
   CREATE USER your_username WITH PASSWORD 'your_password';
   ALTER ROLE your_username SET client_encoding TO 'utf8';
   ALTER ROLE your_username SET default_transaction_isolation TO 'read committed';
   ALTER ROLE your_username SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE ausee_db TO your_username;
   \q
   ```

3. **(Re)Create and Activate the Virtual Environment (if not already done):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect Static Files:**
   ```bash
   python manage.py collectstatic
   ```

8. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Your site should now be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Testing the Setup

1. **Admin Interface:**  
   Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in with your superuser credentials.

2. **Create a Course:**  
   Use the admin interface to create a course.

3. **View Courses:**  
   Check that the course appears at [http://127.0.0.1:8000/courses/](http://127.0.0.1:8000/courses/).

**Common Issues to Watch Out For:**
- Ensure PostgreSQL is installed and running.
- Verify that your database credentials in `.env` match those created in your PostgreSQL setup.
- For static file errors, confirm that `DEBUG=True` in your local environment.

---

## Contributing

We welcome contributions! To get started:

1. **Fork the Repository on GitHub.**
2. **Create a New Branch for Your Feature or Bug Fix:**
   ```bash
   git checkout -b your-feature-branch
   ```
3. **Make Your Changes and Commit Them:**
   ```bash
   git add .
   git commit -m "Describe your changes"
   ```
4. **Push Your Branch:**
   ```bash
   git push origin your-feature-branch
   ```
5. **Open a Pull Request on GitHub.**

---

## Learning Django

If you're new to Django, check out these resources:
- [Official Django Documentation](https://docs.djangoproject.com/)
- [Django Tutorial (Official)](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [MDN Django Guide](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)
- [Real Python Django Guide](https://realpython.com/tutorials/django/)

---

## Supporting AUSee

Running AUSee requires covering costs for the domain and hosting on our VPS. If you find this platform useful, consider making a donation. Every contribution helps us keep AUSee free and accessible to all students.

[Buy us a first floor coffee machine cappuccino: Support AUSee](#)

---

## License

© 2025 AUSee. All rights reserved.

---

We look forward to your contributions and hope you enjoy working with AUSee! 🚀

---
