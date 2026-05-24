import pytest
from httpx import AsyncClient


async def test_create_department(client: AsyncClient):
    response = await client.post("/api/v1/departments/", json={"name": "Test Dept"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Dept"
    assert data["parent_id"] is None


async def test_create_child_department(client: AsyncClient):
    create_parent = await client.post(
        "/api/v1/departments/", json={"name": "Parent Department"}
    )
    parent_id = create_parent.json()["id"]
    response = await client.post(
        "/api/v1/departments/",
        json={"name": "Child Department", "parent_id": parent_id},
    )
    assert response.status_code == 200
    assert response.json()["parent_id"] == parent_id


async def test_get_department(client: AsyncClient):
    create = await client.post("/api/v1/departments/", json={"name": "Get Test Dept"})
    dept_id = create.json()["id"]
    response = await client.get(f"/api/v1/departments/{dept_id}")
    assert response.status_code == 200
    assert response.json()["id"] == dept_id
    assert response.json()["name"] == "Get Test Dept"


async def test_get_department_not_found(client: AsyncClient):
    response = await client.get("/api/v1/departments/99999")
    assert response.status_code == 404


async def test_create_employee(client: AsyncClient):
    dept = await client.post("/api/v1/departments/", json={"name": "HR"})
    dept_id = dept.json()["id"]
    response = await client.post(
        f"/api/v1/departments/{dept_id}/employees/",
        json={"full_name": "John Doe", "position": "Manager"},
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "John Doe"
    assert response.json()["department_id"] == dept_id


async def test_department_name_conflict(client: AsyncClient):
    parent = await client.post("/api/v1/departments/", json={"name": "Parent"})
    parent_id = parent.json()["id"]
    await client.post(
        "/api/v1/departments/", json={"name": "Backend", "parent_id": parent_id}
    )
    response = await client.post(
        "/api/v1/departments/", json={"name": "Backend", "parent_id": parent_id}
    )
    assert response.status_code == 409


async def test_delete_department_cascade(client: AsyncClient):
    dept = await client.post("/api/v1/departments/", json={"name": "To Delete"})
    dept_id = dept.json()["id"]
    response = await client.delete(f"/api/v1/departments/{dept_id}?mode=cascade")
    assert response.status_code == 204
    get_response = await client.get(f"/api/v1/departments/{dept_id}")
    assert get_response.status_code == 404


async def test_update_department(client: AsyncClient):
    dept = await client.post("/api/v1/departments/", json={"name": "Old Name"})
    dept_id = dept.json()["id"]
    response = await client.patch(
        f"/api/v1/departments/{dept_id}", json={"name": "New Name"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


async def test_cycle_detection(client: AsyncClient):
    parent = await client.post("/api/v1/departments/", json={"name": "Cycle Parent"})
    parent_id = parent.json()["id"]
    child = await client.post(
        "/api/v1/departments/", json={"name": "Cycle Child", "parent_id": parent_id}
    )
    child_id = child.json()["id"]
    response = await client.patch(
        f"/api/v1/departments/{parent_id}", json={"parent_id": child_id}
    )
    assert response.status_code == 409
