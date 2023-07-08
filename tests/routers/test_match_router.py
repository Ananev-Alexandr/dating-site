from datetime import date

from tests.conftest import client, test_db

DATA_USER = {
        "username": "test_name",
        "age": 20,
        "location": "TestCity",
        "password": "test_pass",
        "email": "test@mail.ru"
    }
DATA_USER2 = {
        "username": "test_name2",
        "age": 22,
        "location": "TestCity2",
        "password": "test_pass2",
        "email": "test2@mail.ru"
    }
MATCH_DATA = {
    "user1_id": 1,
    "user2_id": 2
}

def test_create_match(test_db):
    response = client.post("/users", json=DATA_USER)
    assert response.status_code == 200
    response = client.post("/users", json=DATA_USER2)
    assert response.status_code == 200
    response = client.post("/matches", json=MATCH_DATA)
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["user1_id"] == 1
    assert data["user2_id"] == 2
    assert data["match_date"] == str(date.today())
    assert len(data) == 4

def test_get_all_matches(test_db):
    response = client.post("/users", json=DATA_USER)
    assert response.status_code == 200
    response = client.post("/users", json=DATA_USER2)
    assert response.status_code == 200
    response = client.post("/matches", json=MATCH_DATA)
    assert response.status_code == 200
    response = client.get("/matches?sort=Сортировка по возрастанию")
    data = response.json()
    assert response.status_code == 200
    assert len(data["matches"]) == 1
    assert data["matches"][0]["id"] == 1
    assert data["matches"][0]["user1_id"] == 1
    assert data["matches"][0]["user2_id"] == 2
    assert data["matches"][0]["match_date"] == str(date.today())
    assert len(data["matches"][0]) == 4
    
def test_delete_matches(test_db):
    response = client.post("/users", json=DATA_USER)
    assert response.status_code == 200
    response = client.post("/users", json=DATA_USER2)
    assert response.status_code == 200
    response = client.post("/matches", json=MATCH_DATA)
    assert response.status_code == 200
    response = client.delete("/matches/1")
    data = response.json()
    assert response.status_code == 200
    assert data == {'message': 'Match successfully deleted'}
    response = client.get("/matches?sort=Сортировка по возрастанию")
    data = response.json()
    assert response.status_code == 200
    assert len(data["matches"]) == 0