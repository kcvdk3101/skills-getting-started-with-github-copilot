from src.app import activities as app_activities


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)
    assert data["Chess Club"]["max_participants"] == 12
    assert data["Gym Class"]["description"] == "Physical education and sports activities"


def test_signup_for_activity_success(client):
    response = client.post("/activities/Chess Club/signup?email=teststudent@mergington.edu")
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up teststudent@mergington.edu for Chess Club"

    after = client.get("/activities").json()
    assert "teststudent@mergington.edu" in after["Chess Club"]["participants"]


def test_signup_for_nonexistent_activity(client):
    response = client.post("/activities/Nonexistent/signup?email=teststudent@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant(client):
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_missing_email(client):
    response = client.post("/activities/Chess Club/signup")
    assert response.status_code == 422
    body = response.json()
    assert body["detail"][0]["loc"][-1] == "email"


def test_signup_activity_full(client):
    app_activities["Chess Club"]["participants"] = [f"student{i}@mergington.edu" for i in range(12)]
    response = client.post("/activities/Chess Club/signup?email=extra@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_delete_participant_success(client):
    response = client.delete("/activities/Chess Club/participant?email=michael@mergington.edu")
    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    after = client.get("/activities").json()
    assert "michael@mergington.edu" not in after["Chess Club"]["participants"]


def test_delete_participant_not_found(client):
    response = client.delete("/activities/Chess Club/participant?email=missing@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in activity"


def test_delete_activity_not_found(client):
    response = client.delete("/activities/NotAnActivity/participant?email=teststudent@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
