# Cloud-Based Data Deduplication API

> A cloud-native data deduplication service built with Python, Flask, and PostgreSQL on AWS RDS. This project, created as part of the CodeAlpha internship, ensures data integrity by preventing redundant entries.

---

## 📋 Table of Contents
- [About The Project](#about-the-project)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Getting Started](#-getting-started)
- [API Usage](#-api-usage)

---

## ℹ️ About The Project

This project is a backend service designed to solve the common problem of data redundancy in databases. It exposes a simple RESTful API endpoint that receives new data payloads. Before saving any new information, the system generates a unique hash of the incoming data and queries a cloud-hosted PostgreSQL database to check for its existence. Only unique, non-redundant data is appended, ensuring the database remains efficient and accurate.

This was developed as a core project for the Cloud Computing internship at **CodeAlpha**.

---

## ✨ Key Features

- **Redundancy Check**: Utilizes SHA-256 hashing to create a unique fingerprint for each data entry and prevent duplicates.
- **RESTful API Endpoint**: A simple and clean API built with Flask to accept and process new data.
- **Cloud Integration**: Connects securely to a managed PostgreSQL database hosted on AWS RDS.
- **Data Validation**: Includes basic checks to ensure incoming data payloads are well-formed.
- **Scalable Foundation**: Built with standard tools and practices that allow for future expansion.

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Flask
- **Database**: PostgreSQL
- **Cloud Provider**: Amazon Web Services (AWS RDS)
- **Database Driver**: Psycopg2
- **Environment Management**: python-dotenv

---

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites
- Python 3.8+
- An AWS Account with a running RDS PostgreSQL instance.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your_username/CodeAlpha_Data-Deduplication-API.git](https://github.com/your_username/CodeAlpha_Data-Deduplication-API.git)
    cd CodeAlpha_Data-Deduplication-API
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    - Create a file named `.env` and add your database credentials.
        ```
        DB_HOST=your-rds-endpoint.rds.amazonaws.com
        DB_NAME=your_database_name
        DB_USER=your_master_username
        DB_PASS=your_master_password
        DB_PORT=5432
        ```

5.  **Run the Flask application:**
    ```bash
    python main.py
    ```

---

## 📡 API Usage

### Add New Data

Send a `POST` request to the `/add-data` endpoint with your JSON payload.

- **Endpoint**: `/add-data`
- **Method**: `POST`
- **Body**:
    ```json
    {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }
    ```

#### Example `curl` Request:

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"Jane Doe\", \"email\": \"jane.doe@example.com\"}" [http://127.0.0.1:5000/add-data](http://127.0.0.1:5000/add-data)
```

#### Success Response (Status `201 Created`):
```json
{
  "hash": "generated_hash_value",
  "message": "Unique data has been successfully added.",
  "status": "success"
}
```

#### Redundant Data Response (Status `200 OK`):
```json
{
  "message": "This exact data already exists in the database.",
  "status": "redundant"
}
```