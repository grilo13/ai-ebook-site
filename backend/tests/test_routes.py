def test_health_endpoint(client):
    response = client.get("/health")
    assert response.json == {"message": "I am healthy!"}
    assert response.status_code == 200
