from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_greet_default():
    response = client.get("/greet")
    assert response.status_code == 200
    assert response.json() == {"greeting": "Hello, Shan!"}

def test_greet_zh():
    response = client.get("/greet?name=小山&language=zh")
    assert response.status_code == 200
    assert response.json() == {"greeting": "你好, 小山!"}

def test_greet_french():
    response = client.get("/greet?name=Jean&language=fr")
    assert response.status_code == 200
    assert response.json() == {"greeting": "Bonjour, Jean!"}

def test_greet_unknown_language():
    response = client.get("/greet?name=Test&language=es")
    assert response.status_code == 200
    assert response.json() == {"greeting": "not match language, Test!"}


# ✅ 測試成功建立 instance
def test_create_instance_success():
    payload = {
        "name": "my-server",
        "region": "us-west-1",
        "cpu": 4
    }
    response = client.post("/instances", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Instance created successfully!"
    assert data["data"]["name"] == "my-server"
    assert data["data"]["region"] == "us-west-1"
    assert data["data"]["cpu"] == 4

# ❌ 測試 region 錯誤（不在 Enum 中）
def test_create_instance_invalid_region():
    payload = {
        "name": "my-server",
        "region": "invalid-region",
        "cpu": 2
    }
    response = client.post("/instances", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
    assert "Input should be" in response.text

# ❌ 測試缺欄位（少傳 cpu）
def test_create_instance_missing_field():
    payload = {
        "name": "my-server",
        "region": "us-west-1"
    }
    response = client.post("/instances", json=payload)
    assert response.status_code == 422
    assert "cpu" in response.text

def test_stop_instance():
    payload = {
        "name": "my-server",
        "region": "invalid-region",
        "cpu": 2
    }
    response = client.post("/instances_async", json=payload)
    instance_id = response.json()["data"]["id"]

    stop_response = client.patch(f"/instances_async/{instance_id}/stop")
    assert stop_response.status_code == 200
    assert stop_response.json()["status"] == "stopped"

    get_instance = client.get(f"/instances_async/{instance_id}")
    assert get_instance.json()["status"] == "stopped"