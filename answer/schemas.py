from ninja.orm import create_schema
from pydantic import BaseModel
from .models import Answer
from typing import List

AnswerSchema = create_schema(Answer, exclude=['survey','score'])

class CreateAnswerSchema(BaseModel):
    question: int
    chosen: str