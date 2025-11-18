from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Feature Votes API" in response.json()["message"]


def test_health_endpoint():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_features_empty():
    """Test getting features from empty database"""
    response = client.get("/api/v1/features")
    assert response.status_code == 200
    assert response.json() == []


def test_create_feature():
    """Test creating a new feature"""
    feature_data = {"title": "Test Feature", "description": "Test Description"}
    response = client.post("/api/v1/features", json=feature_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Feature"
    assert data["description"] == "Test Description"
    assert data["votes_count"] == 0
    assert "id" in data


def test_get_features_with_data():
    """Test getting features after creating one"""
    response = client.get("/api/v1/features")
    assert response.status_code == 200
    features = response.json()
    assert len(features) >= 1


def test_get_feature_detail():
    """Test getting specific feature details"""
    feature_data = {"title": "Detail Feature", "description": "For detail test"}
    create_response = client.post("/api/v1/features", json=feature_data)
    feature_id = create_response.json()["id"]

    response = client.get(f"/api/v1/features/{feature_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Detail Feature"
    assert data["id"] == feature_id


def test_get_feature_not_found():
    """Test getting non-existent feature"""
    response = client.get("/api/v1/features/99999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_vote_for_feature():
    """Test voting for a feature"""
    feature_data = {"title": "Voting Feature", "description": "For voting test"}
    create_response = client.post("/api/v1/features", json=feature_data)
    feature_id = create_response.json()["id"]

    vote_data = {"user_id": 1, "value": 1}
    response = client.post(f"/api/v1/features/{feature_id}/vote", json=vote_data)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["feature_id"] == feature_id
    assert data["value"] == 1


def test_duplicate_vote():
    """Test duplicate vote prevention"""
    feature_data = {
        "title": "Duplicate Vote Feature",
        "description": "For duplicate test",
    }
    create_response = client.post("/api/v1/features", json=feature_data)
    feature_id = create_response.json()["id"]

    vote_data = {"user_id": 2, "value": 1}
    first_vote = client.post(f"/api/v1/features/{feature_id}/vote", json=vote_data)
    assert first_vote.status_code == 200

    second_vote = client.post(f"/api/v1/features/{feature_id}/vote", json=vote_data)
    assert second_vote.status_code == 400
    data = second_vote.json()
    assert "detail" in data
    assert "already voted" in data["detail"]


def test_invalid_vote_value():
    """Test invalid vote value"""
    feature_data = {
        "title": "Invalid Vote Test",
        "description": "For invalid vote test",
    }
    create_response = client.post("/api/v1/features", json=feature_data)
    feature_id = create_response.json()["id"]

    vote_data = {"user_id": 3, "value": 5}
    response = client.post(f"/api/v1/features/{feature_id}/vote", json=vote_data)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "must be 1 or -1" in data["detail"]


def test_get_top_features():
    """Test getting top features"""
    response = client.get("/api/v1/features/top")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
