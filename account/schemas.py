from ninja import Schema


class LoginData(Schema):
    email: str
    password: str


class RegisterData(Schema):
    email: str
    password: str
    first_name: str
    last_name: str
    branch: str='Pusat'