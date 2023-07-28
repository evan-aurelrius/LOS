from typing import List
from django.http import Http404, JsonResponse
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth
from .schemas import CommentSchema, CreateCommentSchema, ResponseCommentSchema
from .models import Comment


@api_controller('/comment', tags=['Comment'])
class CommentController:

    @route.get('/{application_id}', response=List[ResponseCommentSchema], auth=JWTAuth())
    def get_comments(self, application_id: int):
        comments = Comment.objects.filter(application=application_id)
        if comments.count() == 0:
            return []
        commentSchemas = []
        for comment in comments:
            print(comment.attachment.name if comment.attachment else None)
            commentSchemas.append(
                ResponseCommentSchema(
                    application_id=application_id,
                    title=comment.title,
                    message=comment.message,
                    attachment=comment.attachment.url if comment.attachment else None,
                    name=comment.filename if comment.attachment else None,
                )
            )
        return commentSchemas

    @route.post('/', auth=JWTAuth())
    def create_comment(self, request):
        author = request.auth
        application_id = request.POST.get('application_id')
        title = request.POST.get('title')
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')
        Comment.objects.create(
            application_id=application_id,
            author=author,
            title=title,
            message=message,
            attachment=attachment
        )
        return JsonResponse({'message': 'Comment successfully created'})