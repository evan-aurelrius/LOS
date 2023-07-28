from typing import Any
from django.http import HttpRequest
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.authentication import JWTBaseAuthentication, HttpBearer
from ninja_jwt.exceptions import AuthenticationFailed

class OnlySuperUser(JWTAuth, JWTBaseAuthentication, HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Any:
        super().authenticate(request, token)
        if not request.user.is_superuser:
            raise AuthenticationFailed("Unauthorized")
        return request.user