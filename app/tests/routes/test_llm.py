def test_get_llm_options_200(client, get_llm_list):
    response = client.get("/llm-options")
    llms = response.json()
    assert response.status_code == 200
    assert len(llms) == len(get_llm_list)


def test_get_llm_options_404(client):
    response = client.get("/llm-option")
    assert response.status_code == 404


def test_get_vector_db_list_200(client, get_vector_db_list):
    response = client.get("/vector-db-list")
    db_list = response.json()
    assert response.status_code == 200
    assert len(db_list) == len(get_vector_db_list)


def test_get_vector_db_list_404(client):
    response = client.get("/vector-db-lists")
    assert response.status_code == 404


def test_check_collection_field_required_422(client):
    response = client.get("/check-collection")
    data = response.json()
    assert response.status_code == 422
    assert len(data["detail"]) == 2


def test_check_collection_collection_name_required_422(client):
    response = client.get("/check-collection?vector_db_name=faiss")
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"][1] == "collection_name"


def test_check_collection_vector_db_required_422(client):
    response = client.get("/check-collection?collection_name=djckdnlcj4r384389")
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"][1] == "vector_db_name"


def test_check_collection_correct_vector_db_required_422(client):
    response = client.get(
        "/check-collection?collection_name=djckdnlcj4r384389&vector_db_name=test"
    )
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"][1] == "vector_db_name"


def test_check_collection_200(client):
    response = client.get(
        "/check-collection?collection_name=djckdnlcj4r384389&vector_db_name=chromadb"
    )
    assert response.status_code == 200
