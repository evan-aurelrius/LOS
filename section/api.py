from datetime import datetime, timedelta
from typing import List

from django.db.models import Q, CharField, Count
from django.db.models.functions import Cast, TruncMinute
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja.errors import HttpError
from ninja.pagination import paginate
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

from loanproduct.service import get_filtered_objects
from question.models import Question
from section.models import Section
from section.schemas import SectionResponseSchema, SectionPayloadSchema, SectionSchema, QuestionResponseSchema, \
    QuestionPayloadSchema, QuestionSchema, ErrorMessage


@api_controller('/section', tags=['Section'])
class SectionController:

    @route.post('', response={200: SectionResponseSchema}, auth=JWTAuth())
    def create_section(self, payload: SectionPayloadSchema):
        section = Section.objects.create(**payload.dict())
        return 200, {"message": f"{section.name} successfully created", "section_id": section.id}

    @route.get('/list', response=List[SectionSchema], auth=JWTAuth())
    @paginate()
    def get_section_list(
            self,
            section_id: str = None,
            section_name: str = None,
            section_minimum_score: int = None,
            create_date_start: str = None,
            create_date_end: str = None,
            update_date_start: str = None,
            update_date_end: str = None
    ):
        query = Q()
        dateformat = '%Y-%m-%d'

        sections = get_filtered_objects(Section, query, dateformat, id=section_id, name=section_name,
                                        minimum_score=section_minimum_score, create_date_start=create_date_start,
                                        create_date_end=create_date_end, update_date_start=update_date_start,
                                        update_date_end=update_date_end)

        sections = sections.annotate(
            question_count=Count('question')
        )

        return list(sections)

    @route.get('/{section_id}', response={200: SectionSchema}, auth=JWTAuth())
    def get_section_detail(self, section_id: int):
        try:
            section = Section.objects.annotate(
                created_date=Cast(TruncMinute("create_date"), CharField()),
                updated_date=Cast(TruncMinute("update_date"), CharField()),
                question_count=Count('question')
            ).get(id=section_id)
            return 200, section
        except Section.DoesNotExist:
            raise HttpError(404, "Section does not exist")

    @route.put('/{section_id}', response={200: SectionResponseSchema}, auth=JWTAuth())
    def update_section(self, section_id: int, payload: SectionPayloadSchema):
        section = get_object_or_404(Section, id=section_id)
        for attr, value in payload.dict().items():
            setattr(section, attr, value)
        section.update_date = timezone.localtime(timezone.now())
        section.save()
        return 200, {"message": f"{section.name} successfully updated", "section_id": section.id}

    @route.delete('/{section_id}', response={200: SectionResponseSchema}, auth=JWTAuth())
    def delete_section(self, section_id: int):
        section = get_object_or_404(Section, id=section_id)
        section_name = section.name
        section_id = section.id
        section.delete()
        return 200, {"message": f"{section_name} successfully deleted", "section_id": section_id}

    @route.post('questions/{section_id}', response={200: QuestionResponseSchema}, auth=JWTAuth())
    def create_section_question(self, section_id: int, payload: QuestionPayloadSchema):
        section = get_object_or_404(Section, id=section_id)
        question = Question.objects.create(section=section, **payload.dict())
        return 200, {"message": "Question successfully created", "question_id": question.id}

    @route.get('questions/{section_id}/list', response={200: List[QuestionSchema]}, auth=JWTAuth())
    def get_section_question_list(self, section_id: int):
        section = get_object_or_404(Section, id=section_id)
        questions = section.question_set.all()
        return 200, questions

    @route.put('questions/{section_id}/order', response={200: SectionResponseSchema, 400: ErrorMessage}, auth=JWTAuth())
    def update_section_question_order(self, section_id: int, questions_id: List[int]):
        section = get_object_or_404(Section, id=section_id)
        question_count = section.question_set.count()
        matching_question_count = section.question_set.filter(id__in=questions_id).count()
        if question_count != matching_question_count:
            return 400, {"message": "Question doesnt match"}
        section.set_question_order(questions_id)
        return 200, {"message": f"{section.name} question order successfully updated", "section_id": section.id}
