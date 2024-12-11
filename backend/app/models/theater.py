from pydantic import BaseModel

class TheaterDB(BaseModel):
    id: str = None
    name: str
    max_capacity: int
    projection: str
    screen_size:str
    description: str
