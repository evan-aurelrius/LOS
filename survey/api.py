from typing import List
from django.http import JsonResponse
from ninja_extra import api_controller, route
from answer.models import Answer
from answer.schemas import AnswerSchema
from application.models import Application
from question.models import Question
from question.schemas import QuestionAnswerSchema, QuestionSchema
from .models import Survey
from section.models import Section
from ninja_jwt.authentication import JWTAuth
from .schemas import SurveySchema, SurveyScoreSchema, RemarkSchema
from django.shortcuts import get_object_or_404
from loanproduct.models import LoanProductSection
from django.db import transaction

def create_survey(filler,application,section,survey_data):
    survey = Survey.objects.create(
        filler=filler,
        application=application,
        section=section)
    final_score = 0
    for answer in survey_data.answers:
        question = get_object_or_404(Question, id=answer.question)
        score = 0

        for i in range(len(question.choices)):
            if answer.chosen == question.choices[i]:
                score = question.scores[i]
                break
        
        question = question.question
        answer = Answer.objects.create(
            survey=survey,
            question=question,
            chosen=answer.chosen,
            score=score)
        final_score += score
    survey.final_score = final_score
    survey.save()
    return survey

@api_controller('/survey', tags=['survey'])
class SurveyController:

    @route.post('', auth=JWTAuth())
    def create(self, survey_data: SurveySchema, request):
        filler = request.auth
        application = get_object_or_404(
            Application, id=survey_data.application)
        section = get_object_or_404(Section, id=survey_data.section)

        try:
            with transaction.atomic():
                survey = create_survey(filler,application,section,survey_data)
            return JsonResponse({'message': 'Survey created successfully'})

        except Exception:
            with transaction.atomic():
                survey = get_object_or_404(Survey, application=application, section=section)
                survey.delete()
                survey = create_survey(filler,application,section,survey_data)
            return JsonResponse({'message': 'Survey updated successfully'})

    @route.get('/details/{survey_id}', auth=JWTAuth(), response=List[AnswerSchema])
    def get_survey_details(self, survey_id: int):
        survey = get_object_or_404(Survey, id=survey_id)
        answers = Answer.objects.filter(survey=survey)
        result = []
        for answer in answers:
            answerSchema = AnswerSchema(
                id=answer.id,
                question=answer.question,
                chosen=answer.chosen,
                score=answer.score
            )
            result.append(answerSchema)
        return result
    
    @route.get('/remark/{application_id}', auth=JWTAuth(), response=RemarkSchema)
    def get_remark(self, application_id: int):
        application = get_object_or_404(Application, id=application_id)
        loan_product = application.loan_product
        loan_product_sections = LoanProductSection.objects.filter(loan_product=loan_product)
        sections = Section.objects.filter(loanproductsection__in=loan_product_sections)
        
        survey_results = Survey.objects.filter(
            application=application,
            section__in=sections
        )
        
        for survey_result in survey_results:
            if survey_result.final_score < survey_result.section.minimum_score:
                return RemarkSchema(remark="Tidak Layak Diberikan")
        
        return RemarkSchema(remark="Layak Diberikan")

    @route.get('/{application_id}/{section_id}', auth=JWTAuth(), response=SurveyScoreSchema)
    def get_survey(self, application_id: int, section_id: int):
        application = get_object_or_404(Application, id=application_id)
        section = get_object_or_404(Section, id=section_id)
        survey = get_object_or_404(
            Survey, application=application, section=section)
        surveyScoreSchema = SurveyScoreSchema(
            id=survey.id,
            section_id=survey.section.id,
            section_name=survey.section.name,
            final_score=survey.final_score
        )
        return surveyScoreSchema

    @route.get('/{application_id}', auth=JWTAuth(), response=List[SurveyScoreSchema])
    def get_surveys(self, application_id: int):
        application = get_object_or_404(Application, id=application_id)
        loan_product = application.loan_product
        loan_product_section = LoanProductSection.objects.filter(
            loan_product=loan_product)
        sections = Section.objects.filter(
            loanproductsection__in=loan_product_section)
        surveys = []
        for section in sections:
            survey = Survey.objects.filter(
                application=application, section=section).first()
            if (survey is not None):
                surveyScoreSchema = SurveyScoreSchema(
                    id=survey.id,
                    section_id=survey.section.id,
                    section_name=survey.section.name,
                    final_score=survey.final_score
                )
                surveys.append(surveyScoreSchema)
        return surveys