# Personal Workout Log API

This is a simple but powerful REST API for logging personal workouts, built with Python, FastAPI, and SQLModel. It provides a complete set of CRUD (Create, Read, Update, Delete) operations for managing workout entries and saves all data to a persistent SQLite database.

## Features

* **Full CRUD Functionality:** Create, Read, Update, and Delete workout entries.
* **Data Validation:** Uses Pydantic and SQLModel to ensure data integrity.
* **Persistent Storage:** All data is saved to a local SQLite database file.
* **Automatic API Documentation:** Interactive documentation is automatically generated and available at the `/docs` endpoint.
* **Professional Structure:** The code is modularized, with a clean separation of concerns.

## Technologies Used

* **Python 3**
* **FastAPI:** For the web framework.
* **SQLModel:** For data validation (Pydantic) and database interaction (ORM).
* **SQLite:** For the file-based database.
* **Uvicorn:** As the ASGI server to run the application.

## Setup and Usage

To run this project locally, follow these steps:

### 1. Prerequisites

* Python 3.11+
* Git

### 2. Clone the Repository

```bash
git clone [https://github.com/YourUsername/fastapi-workout-api.git](https://github.com/0xDubos/fastapi-workout-api.git)
cd fastapi-workout-api 
```
### 3. Create and Activate Virtual Environment
On Windows:

``` Bash

python -m venv venv
.\venv\Scripts\activate
```
On macOS / Linux:

``` Bash
python3 -m venv venv
source venv/bin/activate
```
### 4. Install Dependencies
``` Bash

pip install -r requirements.txt
```
### 5. Run the Application
``` Bash

uvicorn main:app --reload
```
The API will now be running on your local machine.

### 6. Access the API
```
 Live API: http://127.0.0.1:8000
```
Interactive Docs (Swagger UI): http://127.0.0.1:8000/docs

You can use the interactive docs page to test all the API endpoints directly from your browser.
