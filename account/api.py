from ninja_extra import api_controller, route
from account.models import User
from django.contrib.auth import authenticate
from ninja_jwt.authentication import JWTAuth
from .permission import OnlySuperUser
from django.http import JsonResponse

from .schemas import RegisterData


@api_controller('/auth', tags=['Account'])
class AccountController():
        
    @route.post('/create-account', auth=OnlySuperUser())
    def create_account(self, register_data: RegisterData):
        user = authenticate(email=register_data.email, password=register_data.password)
        if user is not None:
            #  return error message with status code 400
            return JsonResponse({'error': 'User already exists'}, status=400)
        User.objects.create_user(**register_data.dict())
        return JsonResponse({'message': 'Successfully created account'})
        
    @route.get('/test', auth=JWTAuth())
    def test(self):
        return JsonResponse({'message': 'Hello, World!'})