from ninja import ModelSchema, Schema

from applicant.models import Applicant


class ApplicantListSchema(ModelSchema):
    class Config:
        model = Applicant
        model_fields = ['id', 'fullname', 'application_status', 'create_date']


class FileSchema(Schema):
    id: str
    name: str
    extension: str
    url: str
    detail: str

class UpdateLogSchema(Schema):
    update_date: str
    update_by: str


class Message(Schema):
    message: str