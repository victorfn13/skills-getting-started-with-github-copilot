import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def restore_activity_state():
    original_participants = {
        name: details["participants"][:]
        for name, details in activities.items()
    }
    yield
    for name, details in activities.items():
        details["participants"] = original_participants[name][:]


client = TestClient(app)


def test_unregister_participant():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
