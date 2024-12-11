def test_create_reservation(client):
    # Crear un usuario
    user_response = client.post("/user", json={
        "username": "user123",
        "password": "Password@123",
        "email": "user123@example.com"
    })
    assert user_response.status_code == 200

    # Iniciar sesión para obtener el token
    login_response = client.post("/auth", data={
        "username": "user123",
        "password": "Password@123"
    })
    assert login_response.status_code == 200
    token_data = login_response.json()
    access_token = token_data["access_token"]

    # Crear una película
    movie_response = client.post("/movie", json={
        "title": "Inception",
        "overview": "Es momento de entrar a los sueños para implentar una idea, este es el caso de ...",
        "year": 2010,
        "rating": 8.8,
        "category": "Sci-Fi",
        "duration": 60,
    })
    assert movie_response.status_code == 200
    movie_data = movie_response.json()["data"]

    # Crear un teatro
    theater_response = client.post("/theater", json={
        "name": "Anfiteatro Griego",
        "max_capacity": 35,
        "projection": "4K",
        "screen_size": '120"',
        "description": "Sala ambientada en un anfiteatro griego con sonido envolvente",
    })
    assert theater_response.status_code == 200
    theater_data = theater_response.json()["data"]

    # Crear una reservación
    reservation_response = client.post("/reservation", json={
        "theater_id": theater_data["id"],  # Usar el ID generado del teatro
        "movie_id": movie_data["id"],  # Usar el ID generado de la película
        "is_private": True,
        "start_time": "14:00",
        "end_time": "16:00",
        "reservation_date": "2024-11-25",
        "status": "active"
    }, headers={"Authorization": f"Bearer {access_token}"})
    assert reservation_response.status_code == 200
    json_response = reservation_response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "La reservación ha sido creada exitosamente."
    assert json_response["description"] == "La reservación se añadió correctamente a la base de datos."


def test_get_reservations(client):
    # Obtener todas las reservaciones
    response = client.get("/reservation")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "Reservaciones obtenidas con éxito."
    assert json_response["description"] == "Se obtuvo correctamente la lista de reservaciones."
    assert isinstance(json_response["data"], list)  # Asegurar que es una lista

def test_get_reservation_by_id(client):
    # Crear un usuario
    user_response = client.post("/user", json={
        "username": "usuario123",
        "password": "Password@123",
        "email": "usuario123@example.com",
    })
    assert user_response.status_code == 200

    # Iniciar sesión para obtener el token
    login_response = client.post("/auth", data={
        "username": "usuario123",
        "password": "Password@123"
    })
    assert login_response.status_code == 200
    token_data = login_response.json()
    access_token = token_data["access_token"]

    # Crear una película
    movie_response = client.post("/movie", json={
        "title": "Inception",
        "overview": "Es momento de entrar a los sueños para implentar una idea, este es el caso de ...",
        "year": 2010,
        "rating": 8.8,
        "category": "Sci-Fi",
        "duration": 60,
    })
    assert movie_response.status_code == 200
    movie_data = movie_response.json()["data"]

    # Crear un teatro
    theater_response = client.post("/theater", json={
        "name": "Anfiteatro Griego",
        "max_capacity": 35,
        "projection": "4K",
        "screen_size": '120"',
        "description": "Sala ambientada en un anfiteatro griego con sonido envolvente",
    })
    assert theater_response.status_code == 200
    theater_data = theater_response.json()["data"]

    # Crear una reservación
    reservation_response = client.post("/reservation", json={
        "theater_id": theater_data["id"],  # Usar el ID generado del teatro
        "movie_id": movie_data["id"],  # Usar el ID generado de la película
        "is_private": True,
        "start_time": "14:00",
        "end_time": "16:00",
        "reservation_date": "2024-11-25",
        "status": "active"
    }, headers={"Authorization": f"Bearer {access_token}"})
    reservation_id = reservation_response.json()["data"]["id"]

    # Obtener la reservación por ID
    response = client.get(f"/reservation/{reservation_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "Reservación obtenida con éxito."
    assert json_response["description"] == "Se obtuvo correctamente la reservación solicitada."

def test_update_reservation(client):
    # Crear un usuario
    user_response = client.post("/user", json={
        "username": "Juan",
        "password": "Password@123",
        "email": "Juan@example.com",
    })
    assert user_response.status_code == 200

    # Iniciar sesión para obtener el token
    login_response = client.post("/auth", data={
        "username": "Juan",
        "password": "Password@123"
    })
    assert login_response.status_code == 200
    token_data = login_response.json()
    access_token = token_data["access_token"]

    # Crear una película
    movie_response = client.post("/movie", json={
        "title": "Inception",
        "overview": "Es momento de entrar a los sueños para implentar una idea, este es el caso de ...",
        "year": 2010,
        "rating": 8.8,
        "category": "Sci-Fi",
        "duration": 60,
    })
    assert movie_response.status_code == 200
    movie_data = movie_response.json()["data"]

    # Crear un teatro
    theater_response = client.post("/theater", json={
        "name": "Anfiteatro Griego",
        "max_capacity": 35,
        "projection": "4K",
        "screen_size": '120"',
        "description": "Sala ambientada en un anfiteatro griego con sonido envolvente",
    })
    assert theater_response.status_code == 200
    theater_data = theater_response.json()["data"]

    # Crear una reservación
    reservation_response = client.post("/reservation", json={
        "theater_id": theater_data["id"],  # Usar el ID generado del teatro
        "movie_id": movie_data["id"],  # Usar el ID generado de la película
        "is_private": True,
        "start_time": "14:00",
        "end_time": "16:00",
        "reservation_date": "2024-11-25",
        "status": "active"
    }, headers={"Authorization": f"Bearer {access_token}"})
    reservation_id = reservation_response.json()["data"]["id"]

    # Actualizar la reservación
    response = client.put(f"/reservation/{reservation_id}", json={
        "theater_id": theater_data["id"],
        "movie_id": movie_data["id"],
        "is_private": True,
        "start_time": "09:00",
        "end_time": "12:00",
        "reservation_date": "2024-11-26",
        "status": "active"
    })
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "La reservación ha sido actualizada exitosamente."
    assert json_response["description"] == "Los datos de la reservación se han modificado correctamente."

def test_delete_reservation(client):
    # Crear un usuario
    user_response = client.post("/user", json={
        "username": "Lili",
        "password": "Password@123",
        "email": "lili@example.com",
    })
    assert user_response.status_code == 200

    # Iniciar sesión para obtener el token
    login_response = client.post("/auth", data={
        "username": "Lili",
        "password": "Password@123"
    })
    assert login_response.status_code == 200
    token_data = login_response.json()
    access_token = token_data["access_token"]

    # Crear una película
    movie_response = client.post("/movie", json={
        "title": "Inception",
        "overview": "Es momento de entrar a los sueños para implentar una idea, este es el caso de ...",
        "year": 2010,
        "rating": 8.8,
        "category": "Sci-Fi",
        "duration": 60,
    })
    assert movie_response.status_code == 200
    movie_data = movie_response.json()["data"]

    # Crear un teatro
    theater_response = client.post("/theater", json={
        "name": "Anfiteatro Griego",
        "max_capacity": 35,
        "projection": "4K",
        "screen_size": '120"',
        "description": "Sala ambientada en un anfiteatro griego con sonido envolvente",
    })
    assert theater_response.status_code == 200
    theater_data = theater_response.json()["data"]

    # Crear una reservación
    reservation_response = client.post("/reservation", json={
        "theater_id": theater_data["id"],  # Usar el ID generado del teatro
        "movie_id": movie_data["id"],  # Usar el ID generado de la película
        "is_private": True,
        "start_time": "14:00",
        "end_time": "16:00",
        "reservation_date": "2024-11-25",
        "status": "active"
    }, headers={"Authorization": f"Bearer {access_token}"})
    reservation_id = reservation_response.json()["data"]["id"]

    # Eliminar la reservación
    response = client.delete(f"/reservation/{reservation_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 200
    assert json_response["message"] == "La reservación ha sido eliminada exitosamente."
    assert json_response["description"] == "Se eliminó correctamente la reservación de la base de datos."
    assert json_response["data"] is None