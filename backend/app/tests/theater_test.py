def test_create_theater(client):
    response = client.post("/theater", json={
        "name": "Anfiteatro Griego",
        "max_capacity": 35,
        "projection": "4K",
        "screen_size": '120"',
        "description": "Sala ambientada en un anfiteatro griego con sonido envolvente",
    })
    assert response.status_code == 200  # Actualizar código esperado si el endpoint devuelve 200
    json_response = response.json()
    assert json_response["code"] == 200  # Ajustar a 200 si es el código esperado
    assert json_response["message"] == "La sala de proyección ha sido creada exitosamente."
    assert json_response["description"] == "La sala de proyección ha sido añadida correctamente a la base de datos."
    assert json_response["data"]["name"] == "Anfiteatro Griego"


def test_get_theaters(client):
    response = client.get("/theater")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "Salas de proyección obtenidas con éxito."
    assert json_response["description"] == "Se obtuvo correctamente la lista de salas de proyección."
    assert isinstance(json_response["data"], list)


def test_get_theater_by_id(client):
    # Crear un teatro para probar el GET por ID
    theater_response = client.post("/theater", json={
        "name": "Sala Vintage",
        "max_capacity": 25,
        "projection": "1080p",
        "screen_size": '100"',
        "description": "Sala con decoración retro.",
    })
    theater_id = theater_response.json()["data"]["id"]

    response = client.get(f"/theater/{theater_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "Sala de proyección obtenida con éxito."
    assert json_response["description"] == "Se obtuvo correctamente la sala de proyección solicitada."
    assert json_response["data"]["id"] == theater_id
    assert json_response["data"]["name"] == "Sala Vintage"



def test_update_theater(client):
    # Crear un teatro para probar el UPDATE
    theater_response = client.post("/theater", json={
        "name": "Sala Clásica",
        "max_capacity": 40,
        "projection": "1080p",
        "screen_size": '120"',
        "description": "Sala con un diseño clásico.",
    })
    theater_id = theater_response.json()["data"]["id"]

    # Actualizar el teatro
    update_response = client.put(f"/theater/{theater_id}", json={
        "name": "Sala Moderna",
        "max_capacity": 50,
        "projection": "4K",
        "screen_size": '150"',
        "description": "Sala con diseño moderno y tecnología avanzada.",
    })
    assert update_response.status_code == 200
    json_response = update_response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "La sala de proyección ha sido actualizada exitosamente."
    assert json_response["description"] == "Los datos de la sala de proyección se han modificado correctamente."
    assert json_response["data"]["name"] == "Sala Moderna"


def test_delete_theater(client):
    # Crear un teatro para probar el DELETE
    theater_response = client.post("/theater", json={
        "name": "Sala Vintage",
        "max_capacity": 30,
        "projection": "4K",
        "screen_size": '140"',
        "description": "Sala vintage con decoración temática.",
    })
    theater_id = theater_response.json()["data"]["id"]

    # Eliminar el teatro
    delete_response = client.delete(f"/theater/{theater_id}")
    assert delete_response.status_code == 200
    json_response = delete_response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "La sala de proyección ha sido eliminada exitosamente."
    assert json_response["description"] == "Se eliminó correctamente la sala de proyección de la base de datos."
    assert json_response["data"] is None

