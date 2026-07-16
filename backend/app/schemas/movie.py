from pydantic import BaseModel, ConfigDict


class MovieOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    genres: list[str]
    duration: str
    rating: float
    year: int
    image: str
    platform: str
    featured: bool


class CategoryOut(BaseModel):
    key: str
    title: str
    movies: list[MovieOut]
