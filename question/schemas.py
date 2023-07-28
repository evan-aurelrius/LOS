from ninja.orm import create_schema
from .models import Question

QuestionSchema = create_schema(Question, exclude=['section', 'is_deleted', 'deleted_at', 'deleted_by'])
QuestionWithoutScoreSchema = create_schema(Question, exclude=['section', 'scores', 'is_deleted', 'deleted_at', 'deleted_by'])

class QuestionAnswerSchema(QuestionWithoutScoreSchema):
    chosen: str