from ninja_extra import api_controller, route

from section.models import Section
from .models import Question
from ninja_jwt.authentication import JWTAuth
from django.http import JsonResponse
from .schemas import QuestionSchema
from django.shortcuts import get_object_or_404

@api_controller('/question', tags=['Question'])
class QuestionController:
        
    @route.post('section/{section_id}', auth=JWTAuth())
    def create(self, section_id: int, question_data: QuestionSchema):
        try:
            section = get_object_or_404(Section, id=section_id)
            question = section.question_set.get(question=question_data.question)
        except Question.DoesNotExist:
            question = None
        if question != None:
            return JsonResponse({'message': 'Question already exists'}, status=409)
        question = Question.objects.create(section=section, **question_data.dict())
        return JsonResponse({'question_id': question.id}, status=201)
        
    @route.get('/{question_id}', response=QuestionSchema, auth=JWTAuth())
    def get_question_detail(self, question_id:int):
        question = get_object_or_404(Question, id=question_id)
        return question
        
    @route.put('/{question_id}', auth=JWTAuth())
    def edit_question(self, question_id:int, question_data: QuestionSchema):
        question = get_object_or_404(Question, id=question_id)
        question.question = question_data.question
        question.choices = question_data.choices
        question.scores = question_data.scores
        question.save()
        return JsonResponse({'message': 'Question updated'}, status=200)
    
    @route.delete('/{question_id}', auth=JWTAuth())
    def delete_question(self, question_id:int):
        question = get_object_or_404(Question, id=question_id)
        question.delete()
        return JsonResponse({'message': 'Question deleted'}, status=204)