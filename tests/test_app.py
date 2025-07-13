from datetime import date

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 404

def test_team_members_get(client):
    response = client.get("/team_members/")
    assert response.status_code == 200


def test_projects_get(client):
    response = client.get("/projects/")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_departments_get(client):
    response = client.get("/departments/")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_clients_get(client):
    response = client.get("/clients/")
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_performance_reviews_get(client):
    response = client.get("/performance_reviews/")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_team_member(client):
    response = client.post("/team_members/", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "msisdn": "0400000000",
        "start_date": date(2023, 1, 1).isoformat(),
        "tenure": 1,
        "salary": 50000
    })

    assert response.status_code == 201
