from typing import List


def test_create_movie(client):
    response = client.post("/movie", json={
        "title": "Inception",
        "overview": "Es momento de entrar a los sueños para implentar una idea, este es el caso de ...",
        "year": 2010,
        "rating": 8.8,
        "category": "Sci-Fi",
        "duration": 148,
    })
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "La película ha sido creada exitosamente."
    assert json_response["description"] == "La película ha sido añadida correctamente a la base de datos."
    assert json_response["data"]["title"] == "Inception"



def test_get_movies(client):
    response = client.get("/movie")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "Películas obtenidas con éxito."
    assert json_response["description"] == "Se obtuvo correctamente la lista de películas."
    assert isinstance(json_response["data"], list)



def test_get_movie_by_id(client):
    # Crear película para probar el GET por ID
    movie_response = client.post("/movie", json={
        "title": "Interstellar",
        "overview": "Naves espaciales",
        "year": 2005,
        "rating": 8.8,
        "category": "Sci-Fi",
        "duration": 120,
    })
    movie_id = movie_response.json()["data"]["id"]

    response = client.get(f"/movie/{movie_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "Película obtenida con éxito."
    assert json_response["description"] == "Se obtuvo correctamente la película solicitada."
    assert json_response["data"]["id"] == movie_id
    assert json_response["data"]["title"] == "Interstellar"



def test_update_movie(client):
    # Crear película para probar el UPDATE
    movie_response = client.post("/movie", json={
        "title": "Interstellar",
        "overview": "Naves espaciales",
        "year": 2005,
        "rating": 8.8,
        "category": "Sci-Fi",
        "duration": 120,
    })
    movie_id = movie_response.json()["data"]["id"]

    # Actualizar la película
    update_response = client.put(f"/movie/{movie_id}", json={
        "title": "Matrix",
        "overview": "La conquista de las máquinas",
        "year": 2007,
        "rating": 8.0,
        "category": "Sci-Fi",
        "duration": 130,
    })
    assert update_response.status_code == 200
    json_response = update_response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "La película ha sido actualizada exitosamente."
    assert json_response["description"] == "Los datos de la película se han modificado correctamente."
    assert json_response["data"]["title"] == "Matrix"


def test_delete_movie(client):
    # Crear película para probar el DELETE
    movie_response = client.post("/movie", json={
        "title": "Avatar",
        "overview": "Alienígenas azules",
        "year": 2002,
        "rating": 8.0,
        "category": "Sci-Fi",
        "duration": 162,
    })
    movie_id = movie_response.json()["data"]["id"]

    # Eliminar la película
    delete_response = client.delete(f"/movie/{movie_id}")
    assert delete_response.status_code == 200
    json_response = delete_response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "La película ha sido eliminada exitosamente."
    assert json_response["description"] == "Se eliminó correctamente la película de la base de datos."
    assert json_response["data"] is None


