from ninja import Schema, ModelSchema

from question.models import Question


class SectionSchema(Schema):
    id: str
    name: str
    question_count: int
    minimum_score: int
    created_date: str
    updated_date: str


class SectionPayloadSchema(Schema):
    name: str
    minimum_score: int


class SectionResponseSchema(Schema):
    message: str
    section_id: str


class QuestionSchema(ModelSchema):
    class Config:
        model = Question
        model_fields = ['id', 'question', 'choices', 'scores']


class QuestionPayloadSchema(ModelSchema):
    class Config:
        model = Question
        model_fields = ['question', 'choices', 'scores']


class QuestionResponseSchema(Schema):
    message: str
    question_id: str


class ErrorMessage(Schema):
    message: str
