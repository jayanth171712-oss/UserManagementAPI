
# User Management REST API

## Project Description
This project is a User Management REST API developed using Python, FastAPI, Pydantic, SQLAlchemy, and SQLite.

It allows users to be created, viewed, updated, and deleted through REST API endpoints.

## Technologies Used
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Uvicorn
- Swagger UI

## Features
- Create a new user
- Retrieve all users
- Retrieve a user by ID
- Update user details
- Delete a user
- Validate email addresses
- Prevent duplicate email addresses
- Validate age between 18 and 60
- Require name and city
- Handle user-not-found errors
- Filter users by city
- Filter users by active status

## User Fields
- ID
- Name
- Email
- Age
- City
- Is Active

## Project Structure
```text
UserManagementAPI/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── README.md
├── users.db
└── screenshots/
```

## Installation

1. Create a virtual environment:

   `python -m venv venv`

2. Activate the virtual environment in PowerShell:

   `.\venv\Scripts\Activate.ps1`

3. Install the dependencies:

   `python -m pip install -r requirements.txt`

## Run the Application

Run the following command:

`python -m uvicorn main:app --reload`

## API Documentation

Open Swagger UI in your browser:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Create a user |
| GET | `/users` | Retrieve all users |
| GET | `/users/{user_id}` | Retrieve a user by ID |
| PUT | `/users/{user_id}` | Update a user |
| DELETE | `/users/{user_id}` | Delete a user |

## Filtering Examples

- `/users?city=Coimbatore`
- `/users?is_active=true`

## Validation and Error Handling
- Invalid email or age outside 18–60: HTTP 422
- Duplicate email: HTTP 409
- User not found: HTTP 404
- Successful user creation: HTTP 201
- Successful retrieval or update: HTTP 200
- Successful deletion: HTTP 204

## Database
The application uses SQLite. The `users.db` database and its table are created automatically when the application starts.

## Testing
The endpoints and validation rules were tested using Swagger UI.
