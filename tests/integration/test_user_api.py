import pytest


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/api/v1/users/",
        json={"email": "new@example.com", "password": "secret123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert data["is_active"] is True
    assert "id" in data


@pytest.mark.asyncio
async def test_create_duplicate_user(client):
    payload = {"email": "dup@example.com", "password": "secret123"}
    await client.post("/api/v1/users/", json=payload)
    response = await client.post("/api/v1/users/", json=payload)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_user(client):
    create = await client.post(
        "/api/v1/users/",
        json={"email": "get@example.com", "password": "secret123"},
    )
    user_id = create.json()["id"]
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "get@example.com"


@pytest.mark.asyncio
async def test_get_nonexistent_user(client):
    response = await client.get("/api/v1/users/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_users(client):
    await client.post("/api/v1/users/", json={"email": "a@x.com", "password": "p"})
    await client.post("/api/v1/users/", json={"email": "b@x.com", "password": "p"})
    response = await client.get("/api/v1/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2
