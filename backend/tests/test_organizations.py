import pytest

def test_create_organizations(client):
    response = client.post("/api/v1/organizations",
        json={"name": "Acme"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Acme"
    assert isinstance(data["id"], int)
    assert data["created_at"] is not None

    saved = client.get(f"/api/v1/organizations/{data['id']}")

    assert saved.status_code == 200
    assert saved.json() == data

def test_create_organization_rejects_blank_name(client):
    response = client.post(
        "/api/v1/organizations",
        json={"name": "   "},
    )

    assert response.status_code == 422

def test_update_organization(client):
    created = client.post(
        "/api/v1/organizations",
        json={"name": "Acme"},
    )
    assert created.status_code == 200
    organization_id = created.json()["id"]

    updated = client.patch(
        f"/api/v1/organizations/{organization_id}",
        json={"name": "Acme Europe"},
    )

    assert updated.status_code == 200
    assert updated.json()["name"] == "Acme Europe"
    assert updated.json()["id"] == organization_id

    retrieved = client.get(
        f"/api/v1/organizations/{organization_id}"
    )

    assert retrieved.status_code == 200
    assert retrieved.json()["name"] == "Acme Europe"

def test_delete_organization(client):
    created = client.post(
        "/api/v1/organizations",
        json={"name": "Acme"},
    )
    assert created.status_code == 200
    organization_id = created.json()["id"]

    deleted = client.delete(
        f"/api/v1/organizations/{organization_id}"
    )

    assert deleted.status_code == 204
    assert deleted.content == b""

    retrieved = client.get(
        f"/api/v1/organizations/{organization_id}"
    )

    assert retrieved.status_code == 404

@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_nonexistent_organization_returns_404(client, method):
    created = client.post(
        "/api/v1/organizations",
        json={"name": "Temporary organization"},
    )
    assert created.status_code == 200

    organization_id = created.json()["id"]
    url = f"/api/v1/organizations/{organization_id}"

    deleted = client.delete(url)
    assert deleted.status_code == 204

    if method == "patch":
        response = client.patch(url, json={"name": "New name"})
    else:
        response = client.request(method, url)

    assert response.status_code == 404
    assert response.json()["detail"] == "Organization not found"