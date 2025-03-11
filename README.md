# AUSee - Anonymous Course Reviews for AUC


## About AUSee

AUSee is an anonymous course review platform designed for students of Amsterdam University College (AUC). It allows students to share their honest opinions about courses while maintaining anonymity. The platform was built by a group of students with the goal of helping others make informed decisions about their course selections.


## Our Mission

We believe that **shared knowledge and experiences** can help the student community. By maintaining anonymity, we encourage openness and honest feedback while fostering a respectful and constructive environment. AUSee is built on the principle of a **horizontal, decentralized structure** where all students can actively participate in adding and moderating courses and reviews. Our goal is to create an anarchic, self-governing space where students **collectively maintain the platform**, ensuring **transparency** and inclusivity in course evaluations. We discourage features that centralize the power to moderate content.&#x20;


## Review Guidelines

While we support free speech, we ask all users to follow these guidelines:

- No hateful or discriminatory comments.
- Be honest but constructive.
- Provide clear and factual reviews to help other students.
- Follow our [Terms of Use](#) for more details.



## Disclaimer

The opinions expressed in the reviews are those of individual users and do not reflect the official views of the developers or AUC.

---

# Getting Started with AUSee (for Contributors)

Did you just take Programming Your World and want some actual real world experience with Python? Dig in! AUSee is a **Django-based** web application. If you're new to Django and Python, we recommend going through the official [Django documentation](https://docs.djangoproject.com/en/stable/) to familiarize yourself with the framework.


## Prerequisites

Before setting up AUSee locally, ensure you have the following installed:

- Python (3.8 or later recommended)
- Git
- pip (Python package manager)
- Virtualenv (optional but recommended)


## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/ausee.git
   cd ausee
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv  # Create virtual environment
   source venv/bin/activate  # Activate (Linux/Mac)
   venv\Scripts\activate  # Activate (Windows)
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**

   ```bash
   python manage.py migrate
   ```

5. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000/` in your browser to see the site in action.


## Contributing

We encourage students to contribute to AUSee! Here’s how to start:

1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b your-feature-branch
   ```
3. **Make your changes and commit them**:
   ```bash
   git add .
   git commit -m "Describe your changes"
   ```
4. **Push your branch**:
   ```bash
   git push origin your-feature-branch
   ```
5. **Open a Pull Request** on GitHub.


## Learning Django

If you're new to Django, here are some resources to help you get started:

- [Official Django Documentation](https://docs.djangoproject.com/en/stable/)
- [Django Tutorial (Official)](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [MDN Django Guide](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)
- [Real Python Django Guide](https://realpython.com/tutorials/django/)

By contributing to AUSee, you're not only improving a helpful tool for AUC students but also gaining valuable experience in **Python and Django web development**.

---

## Supporting AUSee

Keeping AUSee running requires covering costs for the domain and hosting on our VPS. If you find this platform useful and want to support its continued existence, consider making a donation. Every contribution helps us keep AUSee free and accessible to all students.

**Buy us first floor coffee machine cappuccino:** [Support AUSee](https://donate.stripe.com/dR6g1o86T1UObXqcMM)


## License

© 2025 AUSee. All rights reserved.

We look forward to your contributions! 🚀

