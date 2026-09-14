import pytest
from app import app, jobs


@pytest.fixture(autouse=True)
def reset_jobs():
    jobs.clear()
    yield
    jobs.clear()


def test_add_job_success():
    client = app.test_client()

    response = client.post(
        "/jobs",
        json={
            "company": "Amazon",
            "role": "DevOps Engineer"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["company"] == "Amazon"
    assert data["role"] == "DevOps Engineer"
    assert data["status"] == "Applied"
    assert data["id"] == 1  # safe to assert now that state resets each test


def test_add_job_missing_fields():
    client = app.test_client()

    response = client.post(
        "/jobs",
        json={
            "company": "Amazon"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data


def test_add_job_invalid_json():
    client = app.test_client()

    response = client.post(
        "/jobs",
        data="this is not json",
        content_type="text/plain"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data