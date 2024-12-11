from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routers import movie, reservation, theater
from app.shared.exceptions import BusinessLogicError

app = FastAPI(
    title="Movie Club API",
    description="API para gestionar películas y reservas de salas en el Movie Club.",
    version="1.0.0",
)

# Registrar los routers
app.include_router(reservation.router, prefix="/reservation", tags=["Reservation"])
app.include_router(movie.router, prefix="/movie", tags=["Movie"])
app.include_router(theater.router, prefix="/theater", tags=["Theater"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API del Movie Club Fully Integrated"}
