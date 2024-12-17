from typing import List

def test_create_comment(client):
    # Crear un comentario relacionado con una película
    response = client.post("/comments", json={
        "user_id": "123",
        "movie_id": "64f1a4b2e3c9a5508d1e82e4",  # Suponiendo un ID válido de película
        "parent_comment_id": None,
        "comment_content": "Este es un comentario de prueba.",
    })
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["code"] == 201
    assert json_response["message"] == "El comentario ha sido creado exitosamente."
    assert json_response["description"] == "El comentario ha sido añadido correctamente a la base de datos."
    assert json_response["data"]["comment_content"] == "Este es un comentario de prueba."


def test_get_all_comments(client):
    # Obtener todos los comentarios
    response = client.get("/comments")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "Comentarios obtenidos con éxito."
    assert json_response["description"] == "Se obtuvo correctamente la lista de comentarios."
    assert isinstance(json_response["data"], list)


def test_get_comment_by_id(client):
    # Crear un comentario para probar el GET por ID
    comment_response = client.post("/comments", json={
        "user_id": "456",
        "movie_id": "64f1a4b2e3c9a5508d1e82e5",  # Suponiendo otro ID válido de película
        "parent_comment_id": None,
        "comment_content": "Comentario para obtener por ID.",
    })
    comment_id = comment_response.json()["data"]["id"]

    # Obtener el comentario por ID
    response = client.get(f"/comments/{comment_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "Comentario obtenido con éxito."
    assert json_response["description"] == "Se obtuvo correctamente el comentario solicitado."
    assert json_response["data"]["id"] == comment_id
    assert json_response["data"]["comment_content"] == "Comentario para obtener por ID."


def test_update_comment(client):
    # Crear un comentario para probar el UPDATE
    comment_response = client.post("/comments", json={
        "user_id": "789",
        "movie_id": "64f1a4b2e3c9a5508d1e82e6",  # Otro ID válido de película
        "parent_comment_id": None,
        "comment_content": "Comentario inicial.",
    })
    comment_id = comment_response.json()["data"]["id"]

    # Actualizar el comentario
    update_response = client.put(f"/comments/{comment_id}", json={
        "comment_content": "Comentario actualizado.",
    })
    assert update_response.status_code == 200
    json_response = update_response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "El comentario ha sido actualizado exitosamente."
    assert json_response["description"] == "Los datos del comentario se han modificado correctamente."
    assert json_response["data"]["comment_content"] == "Comentario actualizado."


def test_delete_comment(client):
    # Crear un comentario para probar el DELETE
    comment_response = client.post("/comments", json={
        "user_id": "101",
        "movie_id": "64f1a4b2e3c9a5508d1e82e7",  # Otro ID válido de película
        "parent_comment_id": None,
        "comment_content": "Comentario para eliminar.",
    })
    comment_id = comment_response.json()["data"]["id"]

    # Eliminar el comentario
    delete_response = client.delete(f"/comments/{comment_id}")
    assert delete_response.status_code == 200
    json_response = delete_response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "El comentario ha sido eliminado exitosamente."
    assert json_response["description"] == "Se eliminó correctamente el comentario de la base de datos."
    assert json_response["data"] is None
