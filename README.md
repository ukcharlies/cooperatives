# Cooperatives Backend

## Overview

The **Cooperatives Backend** is the core system designed to manage cooperative societies, providing robust functionalities for user management, cooperative operations, and financial tracking. It serves as the backend API for a cooperative management system, enabling seamless frontend integration.

## Features

### **User Management**

- User registration and authentication.
- Role-based access control (e.g., Admin, Member).

### **Cooperative Operations**

- Creation and management of cooperatives.
- Member enrollment and tracking.

### **Financial Management**

- Contribution tracking.
- Loan management and repayment schedules.
- Financial reporting and analytics.

### **Notifications**

- Email and SMS notifications for important updates.

## Tech Stack

- **Backend Framework**: Django (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Token)
- **Environment Variables**: dotenv for configuration management

## Installation

### Prerequisites

Ensure you have the following installed:

- **Python 3.9+**
- **PostgreSQL**
- **Django & Required Packages**
- **Git**

### Setup Instructions

#### 1. Clone the Repository

```sh
git clone https://github.com/your-username/cooperatives.git
cd cooperatives
```

#### 2. Create and Activate a Virtual Environment

```sh
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

#### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

Create a `.env` file in the root directory and add the following variables:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/cooperatives_db
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_password
```

#### 5. Run Database Migrations

```sh
python manage.py migrate
```

#### 6. Start the Server

```sh
python manage.py runserver
```

## Usage

- Access the API documentation at `/api-docs` (if Swagger or similar is configured).
- Use tools like Postman to test endpoints.

## API Endpoints

### **Authentication**

- `POST /auth/register` - Register a new user.
- `POST /auth/login` - Authenticate a user.

### **Cooperatives**

- `POST /cooperatives` - Create a new cooperative.
- `GET /cooperatives` - List all cooperatives.

### **Members**

- `POST /cooperatives/:id/members` - Add a member to a cooperative.
- `GET /cooperatives/:id/members` - List members of a cooperative.

### **Financials**

- `POST /cooperatives/:id/contributions` - Record a contribution.
- `POST /cooperatives/:id/loans` - Request a loan.

## Contributing

- Fork the repository.
- Create a new branch for your feature or bugfix.
- Submit a pull request.

## License

This project is licensed under the **MIT License**.

## Contact

For inquiries or support, reach out to **ukcharlies@gmail.com**.
