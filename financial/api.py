from typing import List
from ninja_extra import api_controller, route

from .models import Financial
from ninja_jwt.authentication import JWTAuth
from django.http import JsonResponse
from .schemas import FinancialSchema
from django.shortcuts import get_object_or_404
from applicant.models import Applicant

@api_controller('/financial', tags=['Financial'])
class FinancialController:
        
    @route.get('/list/{applicant_id}', auth=JWTAuth(), response=List[FinancialSchema])
    def list_financial(self, applicant_id:int):
        financials = Financial.objects.filter(applicant_id=applicant_id)
        financial_data = []
        for financial in financials:
            financial_data.append(
                FinancialSchema(
                    id=financial.id,
                    title=financial.title,
                    amount=financial.amount
                )
            )
        return financial_data
    
    @route.post('/create/{applicant_id}', auth=JWTAuth())
    def create(self, applicant_id:int, financial_data: FinancialSchema):
        try:
            appicant = get_object_or_404(Applicant, pk=applicant_id)
            Financial.objects.create(
                applicant=appicant,
                **financial_data.dict()
            )
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Cannot create this financial data'}, status=400)
        return JsonResponse({'message': 'Financial data created'}, status=201)
    
    @route.put('/{financial_id}', auth=JWTAuth())
    def update_financial(self, financial_id:int, financial_data: FinancialSchema):
        try:
            financial = get_object_or_404(Financial, pk=financial_id)
            financial.title = financial_data.title
            financial.amount = financial_data.amount
            financial.save()
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Cannot update this financial data'}, status=400)
        return JsonResponse({'message': 'Financial data updated'}, status=200)
    
    @route.delete('/{financial_id}', auth=JWTAuth())
    def delete_financial(self, financial_id:int):
        try:
            financial = get_object_or_404(Financial, pk=financial_id)
            financial.delete()
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Cannot delete this financial data'}, status=400)
        return JsonResponse({'message': 'Financial data deleted'}, status=200)