import pytest
import httpx
from uuid import uuid4
from app.models.user import User

@pytest.mark.asyncio
async def test_async_crud():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000/async") as client:
        # Create
        user_data = {"name": "John Doe", "email": f"john{uuid4()}@example.com", "age": 30}
        response = await client.post("/users/", json=user_data)
        assert response.status_code == 200
        user = response.json()
        user_id = user["id"]

        # Read all
        response = await client.get("/users/")
        assert response.status_code == 200
        assert any(u["id"] == user_id for u in response.json())

        # Read one
        response = await client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "John Doe"

        # Update
        update_data = {"name": "Jane Doe", "email": f"jane{uuid4()}@example.com", "age": 31}
        response = await client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["name"] == "Jane Doe"

        # Delete
        response = await client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted"

def test_sync_crud():
    with httpx.Client(base_url="http://127.0.0.1:8000/sync") as client:
        # Create
        user_data = {"name": "John Doe", "email": f"john{uuid4()}@example.com", "age": 30}
        response = client.post("/users/", json=user_data)
        assert response.status_code == 200
        user = response.json()
        user_id = user["id"]

        # Read all
        response = client.get("/users/")
        assert response.status_code == 200
        assert any(u["id"] == user_id for u in response.json())

        # Read one
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "John Doe"

        # Update
        update_data = {"name": "Jane Doe", "email": f"jane{uuid4()}@example.com", "age": 31}
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["name"] == "Jane Doe"

        # Delete
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted"