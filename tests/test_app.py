from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_root_redirects_to_static_index():
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_data():
    # Arrange
    expected_activity = "Chess Club"
    expected_description = "Learn strategies and compete in chess tournaments"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert expected_activity in activities
    assert activities[expected_activity]["description"] == expected_description
    assert isinstance(activities[expected_activity]["participants"], list)


def test_signup_and_remove_participant_flow():
    # Arrange
    activity_name = "Programming Class"
    email = "teststudent+1@mergington.edu"

    # Act: sign up participant
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert signup_response.status_code == 200
    assert f"Signed up {email} for {activity_name}" in signup_response.json()["message"]

    # Act: verify participant was added
    activities_response = client.get("/activities")

    # Assert
    assert activities_response.status_code == 200
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants

    # Act: remove the participant
    delete_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert delete_response.status_code == 200
    assert f"Unregistered {email} from {activity_name}" in delete_response.json()["message"]

    # Act: verify participant was removed
    cleanup_response = client.get("/activities")

    # Assert
    assert cleanup_response.status_code == 200
    assert email not in cleanup_response.json()[activity_name]["participants"]
