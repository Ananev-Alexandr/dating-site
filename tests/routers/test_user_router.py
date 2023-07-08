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
DATA_USER3 = {
        "username": "test_name2",
        "age": 22,
        "location": "TestCity2",
        "email": "test2@mail.ru"
    }


def test_create_user(test_db):
    response = client.post("/users", json=DATA_USER)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "test_name"
    assert data["age"] == 20
    assert data["location"] == "TestCity"
    assert data.get("password") is None


def test_get_user(test_db):
    client.post("/users", json=DATA_USER)
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "test_name"
    assert data["age"] == 20
    assert data["location"] == "TestCity"
    assert data.get("password") is None
    
def test_get_all_users(test_db):
    client.post("/users", json=DATA_USER)
    client.post("/users", json=DATA_USER2)
    response = client.get("/users/?sort_username=Сортировка по возрастанию&sort_email=Сортировка по возрастанию")
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) == 2
    response = client.get("/users/?sort_username=Сортировка по возрастанию&sort_email=Сортировка по возрастанию&age_filters=20")
    data = response.json()
    assert len(data["users"]) == 1
    response = client.get("/users/?sort_username=Сортировка по возрастанию&sort_email=Сортировка по возрастанию&age_filters=1")
    data = response.json()
    assert len(data["users"]) == 0

def test_delete_user(test_db):
    client.post("/users", json=DATA_USER)
    response = client.delete("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data == {'message': 'User successfully deleted'}
    response = client.get("/users/?sort_username=Сортировка по возрастанию&sort_email=Сортировка по возрастанию&")
    data = response.json()
    assert len(data["users"]) == 0
    response = client.delete("/users/11")
    assert response.status_code == 404
    
def test_update_user(test_db):
    client.post("/users", json=DATA_USER)
    response = client.put("/users/1", json=DATA_USER3)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test_name2"
    assert data["age"] == 22
    assert data["location"] == "TestCity2"
    assert data["email"] == "test2@mail.ru"
    assert data["id"] == 1
    assert len(data) == 5
