from ninja_jwt.schema import TokenObtainPairSerializer
from ninja_jwt.controller import TokenObtainPairController
from ninja_jwt.controller import TokenVerificationController
from ninja_extra import api_controller, route
from ninja_schema import Schema
import ninja_jwt.schema as schema


class UserSchema(Schema):
    email: str

class MyTokenObtainPairOutSchema(Schema):
    access: str
    refresh: str
    user: UserSchema

class TokenObtainPairSchema(TokenObtainPairSerializer):
    def output_schema(self):
        out_dict = self.dict(exclude={"password"})
        out_dict.update(user=UserSchema.from_orm(self._user))
        return MyTokenObtainPairOutSchema(**out_dict)

@api_controller('/auth', tags=['Auth'])
class TokenObtainPairController(TokenObtainPairController):
    @route.post(
        "/login", response=MyTokenObtainPairOutSchema, url_name="token_obtain_pair"
    )
    def obtain_token(self, user_token: TokenObtainPairSchema):
        return user_token.output_schema()

@api_controller('/auth', tags=['Auth'])
class TokenVerificationController(TokenVerificationController):
    @route.post("/verify", response={200: Schema}, url_name="token_verify")
    def verify_token(self, token: schema.TokenVerifySerializer):
        return {}