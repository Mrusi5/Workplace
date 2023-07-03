from conftest import client

def test_add_workplace():
    response = client.post("/workplace/add", json={
        "name": "string",
        "key": "string"
    })
    
    assert response.status_code == 200