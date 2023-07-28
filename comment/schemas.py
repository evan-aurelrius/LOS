from ninja import UploadedFile
from ninja.orm import create_schema
from .models import Comment

CommentSchema = create_schema(Comment, exclude=['author','id','created_at','updated_at','attachment'])

class CreateCommentSchema(CommentSchema):
    attachment: UploadedFile = None

class ResponseCommentSchema(CommentSchema):
    attachment: str = None
    name: str = None