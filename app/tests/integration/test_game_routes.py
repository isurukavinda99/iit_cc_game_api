import os

import requests
import uuid

BASE_URL = "http://localhost:8000/game/"
HEADERS = {
    "x-amzn-oidc-data": os.environ["OIDC_TOKEN"]
}

def test_game_crud_flow():
    unique_name = f"Test Game {uuid.uuid4().hex[:6]}"
    payload = {
        "name": unique_name,
        "category_id": 1,
        "active": True
    }

    # 1. Create game
    create_res = requests.post(BASE_URL, json=payload, headers=HEADERS)
    assert create_res.status_code == 200, create_res.text
    game = create_res.json()
    game_id = game["id"]
    assert game["name"] == unique_name

    # 2. Get all games
    list_res = requests.get(BASE_URL, headers=HEADERS)
    assert list_res.status_code == 200
    all_games = list_res.json()
    assert any(g["id"] == game_id for g in all_games)

    # 3. Get by ID
    get_res = requests.get(f"{BASE_URL}{game_id}", headers=HEADERS)
    assert get_res.status_code == 200
    game_data = get_res.json()
    assert game_data["id"] == game_id
    assert game_data["name"] == unique_name

    # 4. Update game
    update_payload = {
        "name": f"{unique_name} Updated",
        "category_id": 2,
        "active": False,
        "updated_by": "test-integration"
    }
    update_res = requests.put(f"{BASE_URL}{game_id}", json=update_payload, headers=HEADERS)
    assert update_res.status_code == 200
