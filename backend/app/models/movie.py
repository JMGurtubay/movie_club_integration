from pydantic import BaseModel

class MovieDB(BaseModel):
    id: str = None
    title: str
    overview: str
    year: int
    rating: float
    category: str
    duration: int
