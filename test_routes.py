def test_home(client):
    response=client.get("/")
    assert response.status_code==200 and "ComicCraft" in response.text

def test_health(client):
    response=client.get("/health")
    assert response.status_code==200 and response.json()["status"]=="ok"

def test_create_comic(client,valid_request):
    response=client.post("/api/comics",json=valid_request)
    assert response.status_code==201
    data=response.json()
    assert len(data["panels"])==5 and data["comic_id"]

def test_invalid_request(client,valid_request):
    valid_request["panel_count"]=20
    assert client.post("/api/comics",json=valid_request).status_code==422

def test_unknown_comic(client):
    assert client.get("/comic/not-found").status_code==404
