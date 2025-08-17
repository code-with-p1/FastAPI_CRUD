# FastAPI CRUD Project with SQLite

This project demonstrates a **FastAPI** application implementing CRUD (Create, Read, Update, Delete) operations for managing users, using **SQLite** as the database. It includes both **async** and **sync** implementations for comparison, organized in a modular structure similar to Flask Blueprints, and comes with tests using `pytest` and `httpx`.

## Features
- **CRUD Operations**: Create, read, update, and delete users via RESTful API endpoints.
- **Async and Sync Support**: Implements both async (using `aiosqlite`) and sync (using SQLAlchemy) database operations.
- **Modular Structure**: Organized with separate modules for routes, models, and database logic.
- **SQLite Database**: Persistent storage using SQLite for user data.
- **Testing**: Includes tests for both async and sync endpoints using `pytest` and `httpx`.
- **Pydantic Validation**: Uses Pydantic models for request/response validation.

## Project Structure
```
fastapi_crud/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Main FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py            # Pydantic model for user
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── async_routes.py    # Async CRUD endpoints
│   │   └── sync_routes.py     # Sync CRUD endpoints
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py             # SQLite database setup
├── tests/
│   ├── __init__.py
│   └── test_user_crud.py     # Tests for async and sync endpoints
├── requirements.txt           # Project dependencies
├── README.md                 # Project documentation
```

## Prerequisites
- **Python**: 3.8 or higher
- **pip**: For installing dependencies

## Installation
1. **Clone the Repository** (or create the project structure manually):
   ```bash
   git clone <repository-url>
   cd fastapi_crud
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` includes:
   ```
   fastapi
   uvicorn
   pydantic
   sqlalchemy
   aiosqlite
   pytest
   pytest-asyncio
   httpx
   ```

## Running the Application
1. **Start the FastAPI Server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   - The server runs at `http://127.0.0.1:8000`.
   - The `--reload` flag enables auto-reload for development.

2. **Access the API**:
   - **Interactive Docs**: Open `http://127.0.0.1:8000/docs` in a browser to use the Swagger UI.
   - **Endpoints**:
     - **Async Routes**: `/async/users/` (e.g., `POST /async/users/`, `GET /async/users/{user_id}`)
     - **Sync Routes**: `/sync/users/` (e.g., `POST /sync/users/`, `GET /sync/users/{user_id}`)

## API Usage
The API supports CRUD operations for users with the following fields:
- `id`: UUID (auto-generated)
- `name`: String (required)
- `email`: String (required, unique)
- `age`: Integer (required)

### Example Requests
Use tools like `curl`, Postman, or the Swagger UI to interact with the API.

1. **Create a User**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/async/users/" -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com", "age": 30}'
   ```
   Response:
   ```json
   {"id": "123e4567-e89b-12d3-a456-426614174000", "name": "John Doe", "email": "john@example.com", "age": 30}
   ```

2. **Get All Users**:
   ```bash
   curl -X GET "http://127.0.0.1:8000/async/users/"
   ```

3. **Get a User**:
   ```bash
   curl -X GET "http://127.0.0.1:8000/async/users/123e4567-e89b-12d3-a456-426614174000"
   ```

4. **Update a User**:
   ```bash
   curl -X PUT "http://127.0.0.1:8000/async/users/123e4567-e89b-12d3-a456-426614174000" -H "Content-Type: application/json" -d '{"name": "Jane Doe", "email": "jane@example.com", "age": 31}'
   ```

5. **Delete a User**:
   ```bash
   curl -X DELETE "http://127.0.0.1:8000/async/users/123e4567-e89b-12d3-a456-426614174000"
   ```

Replace `/async/` with `/sync/` to test the sync endpoints.

## Running Tests
1. **Ensure the Server is Running**:
   ```bash
   uvicorn app.main:app
   ```

2. **Run Tests**:
   ```bash
   pytest tests/test_user_crud.py -v
   ```
   - Tests cover both async and sync CRUD operations.
   - The test file uses `httpx` for HTTP requests and `pytest-asyncio` for async tests.
   - Unique email addresses are generated to avoid conflicts.

## Database
- **SQLite**: The database is stored in `users.db` in the project root.
- **Initialization**: The database and `users` table are created automatically when the app starts.
- **Schema**:
  - Table: `users`
  - Columns: `id` (UUID, primary key), `name` (string), `email` (string, unique), `age` (integer)

## Async vs. Sync
- **Async Routes** (`/async/users/`): Use `aiosqlite` and SQLAlchemy's async support, suitable for I/O-bound tasks.
- **Sync Routes** (`/sync/users/`): Use standard SQLAlchemy, simpler for CPU-bound tasks or legacy code.
- **Performance**: Async is generally better for handling concurrent requests, especially with database operations. Sync may be easier to debug or integrate with non-async code.

## Notes
- **Error Handling**: The API includes error handling for duplicate emails, invalid data, and non-existent users.
- **Modularity**: The project uses FastAPI's `APIRouter` for modular routing, similar to Flask Blueprints.
- **Extensibility**: To add more features (e.g., authentication, pagination), modify the respective modules.

## Troubleshooting
- **Database Issues**: Ensure `users.db` is writable in the project directory.
- **Dependency Errors**: Verify all packages are installed (`pip install -r requirements.txt`).
- **Test Failures**: Ensure the server is running before running tests.

For further assistance, contact the project maintainer or open an issue.