# ASD Management

#### Responsive web app for managing a Sports Association.

![Python](https://badgen.net/badge/Built%20with/Python/blue)
![Django](https://img.shields.io/badge/Built%20with-Django-092E20)
![Django Rest Framework](https://img.shields.io/badge/Built%20with-DRF-red)
[![Tests](https://github.com/aleattene/asd-management-webapp-responsive-backend-django/actions/workflows/tests.yml/badge.svg)](https://github.com/aleattene/asd-management-webapp-responsive-backend-django/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/aleattene/asd-management-webapp-responsive-backend-django/graph/badge.svg?token=452QWRN2E6)](https://codecov.io/gh/aleattene/asd-management-webapp-responsive-backend-django)
[![GitHub commits](https://badgen.net/github/commits/aleattene/asd-management-webapp-responsive-backend-django)](https://github.com/aleattene/asd-management-webapp-responsive-backend-django/commits/)
[![GitHub last commit](https://img.shields.io/github/last-commit/aleattene/asd-management-webapp-responsive-backend-django)](https://github.com/aleattene/asd-management-webapp-responsive-backend-django/commits/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/aleattene/asd-management-webapp-responsive-backend-django/pulls)
[![License](https://img.shields.io/github/license/aleattene/asd-management-webapp-responsive-backend-django?color=blue)](https://github.com/aleattene/asd-management-webapp-responsive-backend-django/blob/main/LICENSE)


*Work in Progress....*

**Backend** deploy (**django**-vercel / **postgres**-supabase):

https://asd-management-django.vercel.app/

Frontend deploy (**react**-netlify):

https://asd-management.netlify.app/

![image](https://user-images.githubusercontent.com/74595044/153876039-85241269-cc8b-40ec-94db-9def28df9d5e.png)

## Installation
Follow these steps to set up and run the project locally.

### 1. Clone the Repository
Clone the repository to your local machine using Git:
```bash
git clone https://github.com/aleattene/asd-management-backend-django.git
```

### 2. Navigate to the Project Directory
```bash
cd asd-management-backend-django
```

### 3. Create a Virtual Environment
It's recommended to use a virtual environment to manage project dependencies.

**Using** `venv`:
```bash
python3.11 -m venv asd_venv
```

### 4. Activate the Virtual Environment
**On Unix or macOS**:
```bash
source asd_venv/bin/activate
```
**On Windows**:
```bash
asd_venv\Scripts\activate
```

### 5. Install Dependencies
Install the required Python packages using `pip`:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

<hr/>

## Configuration

The project uses environment variables to manage sensitive information and configuration settings. 
Follow these steps to set up your environment variables.

### 1 Create a `.env` File
In the root directory of the project, create a file named `.env`

### 2. Add Environment Variables
Open the .env`` file in your preferred text editor and add the following variables:
```bash
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
```

<hr/>

## Running the Server
Once the setup is complete, you can run the Django development server.

### 1. Apply Migrations
Ensure all database migrations are applied:
```bash
python manage.py migrate
```

### 2. Create a Superuser (Optional)
To access the Django admin interface, create a superuser:
```bash
python manage.py createsuperuser
```
Follow the prompts to set up your superuser account.

### 3. Run the Development Server
Start the Django development server:

```bash
python manage.py runserver
```
Access the application by navigating to `http://localhost:8000/` in your web browser.

<hr/>

## Running Tests
The project uses Django's built-in testing framework along with coverage.py to measure test coverage.

### 1. Run Tests with Coverage
Execute the tests and generate a coverage report:

```bash
coverage run manage.py test && coverage report --show-missing
```

<hr/>

## Contributing
Contributions are welcome! Please follow these steps:

### 1. Fork the Repository

Click the "Fork" button on the top-right corner of the repository page.

### 2. Clone Your Fork

```bash
git clone https://github.com/aleattene/asd-management-webapp-responsive-backend-django.git
```

### 3. Create a New Branch

```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes

### 5. Commit Your Changes

```bash
git commit -m "Add a meaningful commit message"
```

### 6. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 7. Create a Pull Request

Go to the original repository and create a pull request from your fork (from the `feature/your-feature-name` branch 
to the `main` branch).

<hr/>

## License
This project is licensed under the [MIT License](https://it.wikipedia.org/wiki/Licenza_MIT).

<hr/>
