"""Integration style tests covering core workflows."""
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend import models
from backend.api.deps import get_db
from backend.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

models.Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def create_land_owner(client: TestClient) -> int:
    response = client.post(
        "/land-owners/",
        json={"name": "Owner One", "contact_info": "owner@example.com"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_project(client: TestClient, land_owner_id: int) -> int:
    response = client.post(
        "/projects/",
        json={
            "name": "Skyline Residences",
            "location": "Istanbul",
            "land_owner_id": land_owner_id,
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_unit(client: TestClient, project_id: int) -> int:
    response = client.post(
        "/units/",
        json={
            "project_id": project_id,
            "unit_number": "A1",
            "floor": 3,
            "area_sqm": 123.5,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "design"
    return data["id"]


def test_unit_full_lifecycle():
    client = TestClient(app)

    owner_id = create_land_owner(client)
    project_id = create_project(client, owner_id)

    # transition project to approved and sales to unlock unit transitions
    response = client.patch(f"/projects/{project_id}", json={"status": "approved"})
    assert response.status_code == 200
    response = client.patch(f"/projects/{project_id}", json={"status": "construction"})
    assert response.status_code == 200
    response = client.patch(f"/projects/{project_id}", json={"status": "sales"})
    assert response.status_code == 200

    unit_id = create_unit(client, project_id)

    response = client.post(f"/units/{unit_id}/transition", json={"next_status": "available"})
    assert response.status_code == 200
    assert response.json()["status"] == "available"

    response = client.post(f"/units/{unit_id}/transition", json={"next_status": "reserved"})
    assert response.status_code == 200
    assert response.json()["status"] == "reserved"

    # create shareholders and allocate shares
    shareholder_resp = client.post(
        "/shareholders/",
        json={"name": "Investor One", "email": "investor@example.com"},
    )
    assert shareholder_resp.status_code == 201
    shareholder_id = shareholder_resp.json()["id"]

    payload = [
        {
            "unit_id": unit_id,
            "shareholder_id": shareholder_id,
            "share_percentage": 60.0,
        }
    ]
    response = client.put(f"/units/{unit_id}/shares", json=payload)
    assert response.status_code == 200
    assert response.json()[0]["share_percentage"] == 60.0

    # register sales representative and assign
    rep_resp = client.post(
        "/sales/representatives",
        json={"name": "Selim Kaya", "email": "selim@example.com"},
    )
    assert rep_resp.status_code == 201
    rep_id = rep_resp.json()["id"]

    assignment_resp = client.post(
        "/sales/assignments",
        json={"unit_id": unit_id, "sales_representative_id": rep_id},
    )
    assert assignment_resp.status_code == 201
    assignment_id = assignment_resp.json()["id"]

    # finalize sale
    response = client.post(f"/units/{unit_id}/transition", json={"next_status": "sold"})
    assert response.status_code == 200
    assert response.json()["status"] == "sold"

    response = client.patch(
        f"/sales/assignments/{assignment_id}", json={"status": "completed"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

    # bulk transition to transferred
    response = client.post(
        "/units/bulk-transition",
        json={"unit_ids": [unit_id], "next_status": "transferred"},
    )
    assert response.status_code == 200
    assert response.json()[0]["status"] == "transferred"
