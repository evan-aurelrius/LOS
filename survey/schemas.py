from typing import List
from ninja import Schema
from ninja.orm import create_schema

from answer.schemas import CreateAnswerSchema
from .models import Survey

BaseSurveySchema = create_schema(Survey, exclude=['filler','final_score','id'])

class SurveySchema(BaseSurveySchema):
    answers: List[CreateAnswerSchema]

class SurveyScoreSchema(Schema):
    id: int
    section_id: int
    section_name: str
    final_score: int

class RemarkSchema(Schema):
    remark: str