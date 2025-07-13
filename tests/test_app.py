def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 404

def test_team_members_get(client):
    response = client.get("/team_members/")
    assert response.status_code == 200
