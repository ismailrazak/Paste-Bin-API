# Paste-Bin-API

Paste-Bin-API is a Pastebin-like API built with Django Rest Framework, providing features for creating snippets ,sharing snippets securely with view once option,date-expiration and more similar to Pastebin.

## Features

- **Create Paste**: Submit new text snippets with various categories and languages to choose from.
- **Syntax Highlighting**: Supports syntax highlighting for various languages.
- **Password Protection**: Secure Passoword protection of snippets if needed.
- **Time Expiration**: Allows setting pre-defined dates to expire at, also supports view once feature.
- **Secure Authentication**:Uses JWT for secure authentication of users.


## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ismailrazak/Paste-Bin-API.git
   cd Paste-Bin-API
# Project Setup and Usage Guide

## Setting Up a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

## Installing Dependencies

```bash
pip install -r requirements.txt
```

## Applying Migrations

```bash
python manage.py migrate
```

## Running the Development Server

```bash
python manage.py runserver
```

## API Endpoints

### Application Endpoints

- **Entry view:**
  ```
  /
  ```
- **List all snippets:**
  ```
   /snippets/
  ```
- **Snippet detail:**
  ```
   /snippets/<str:pk>
  ```
- **Highlighted snippet:**
  ```
   /snippets/<str:pk>/highlighted
  ```
- **List all users:**
  ```
   /users
  ```
- **User detail:**
  ```
   /users/<str:pk>
  ```
- **Password-protected view:**
  ```
   /password-required/<str:pk>
  ```

### Project Endpoints

- **Admin panel:**
  ```
  /admin/
  ```
- **Authentication:**
  ```
  /auth/
  ```
- **Registration:**
  ```
  /auth/registration/
  ```
- **Token obtain:**
  ```
  POST /token/
  ```
- **Token refresh:**
  ```
  POST /token/refresh/
  ```


## Configuration with Docker

The project includes a `docker-compose.yml` file for setting up the development environment using Docker.

### Build and Start Services

```bash
docker-compose up --build
```

### Apply Migrations Inside the Web Container

```bash
docker-compose exec web python manage.py migrate
```

### Create a Superuser (Optional)

```bash
docker-compose exec web python manage.py createsuperuser
```

