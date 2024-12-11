from pymongo import MongoClient
from app.shared.config import settings

# Crear una conexión global a MongoDB
client = MongoClient(settings.MONGO_URI)
db = client["movie_club"]  # Nombre de la base de datos
