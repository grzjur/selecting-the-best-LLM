from pydantic import BaseModel

class Answer(BaseModel):
    model: str
    question: str
    answer: str
    speed: float
    rating: int = 0

class ModelRating(BaseModel):
    model: str
    rating: int
    total_speed: float
    average_speed: float
    answer_count: int
