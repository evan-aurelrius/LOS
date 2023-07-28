from datetime import datetime
from typing import List

from django.db.models import Q
from django.forms import Form
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.datetime_safe import strftime
from ninja import UploadedFile, File
from ninja.errors import HttpError
from ninja.pagination import paginate
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

from applicant.models import Applicant, ApplicantFile
from applicant.schemas import ApplicantListSchema, FileSchema, UpdateLogSchema, Message


@api_controller('/applicant', tags=['Applicant'])
class ApplicantController:

    @route.get('/list', response=List[ApplicantListSchema], auth=JWTAuth())
    @paginate()
    def list_applicant(
            self,
            request,
            status: str = None,
            start_date: str = None,
            end_date: str = None,
            area: str = None
    ):
        query = Q()
        if status:
            query &= Q(application_status=status)
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%d-%m-%Y')
                query &= Q(create_date__gte=start_date)
            except ValueError:
                raise HttpError(400, "Invalid start date format. Use DD-MM-YYYY.")
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%d-%m-%Y')
                query &= Q(create_date__lte=end_date)
            except ValueError:
                raise HttpError(400, "Invalid end date format. Use DD-MM-YYYY.")
        if area:
            query &= Q(domicile_city__icontains=area)

        query &= Q(branch=request.user.branch)

        applicants = Applicant.objects.filter(query)
        return applicants

    @route.post('{applicant_id}/file', response={200: Message}, auth=JWTAuth())
    def upload_applicant_file(self, request, applicant_id: int, files: List[UploadedFile] = File(...)):
        detail = request.POST.get('detail')
        applicant = get_object_or_404(Applicant, id=applicant_id)
        for file in files:
            ApplicantFile.objects.create(applicant=applicant, file=file, detail=detail)
        applicant.update_date = timezone.now()
        applicant.update_by = request.user
        applicant.save()
        return {"message": "Files successfully uploaded"}

    @route.get('{applicant_id}/file/list', response={200: List[FileSchema]}, auth=JWTAuth())
    def get_applicant_file_list(self, applicant_id: int):
        applicant = get_object_or_404(Applicant, id=applicant_id)
        file_ids = list(applicant.applicantfile_set.values_list('id', flat=True))
        files = []
        for file_id in file_ids:
            _file = get_object_or_404(ApplicantFile, id=file_id)
            files.append({"id": _file.id, "name": _file.filename, "extension": _file.extension, "url": _file.file.url, "detail":_file.detail})
        return files

    @route.delete('file/{file_id}', response={200: Message}, auth=JWTAuth())
    def delete_applicant_file(self, request, file_id: int):
        _file = get_object_or_404(ApplicantFile, id=file_id)
        applicant = _file.applicant
        file_name = _file.filename
        _file.delete()
        applicant.update_date = timezone.now()
        applicant.update_by = request.user
        applicant.save()
        return 200, {"message": f"{file_name} successfully deleted"}

    @route.get('log/{applicant_id}', response={200: UpdateLogSchema}, auth=JWTAuth())
    def get_applicant_update_log(self, applicant_id: int):
        applicant = get_object_or_404(Applicant, id=applicant_id)
        first_name = applicant.update_by.first_name
        last_name = applicant.update_by.last_name
        update_date = strftime(timezone.localtime(applicant.update_date), "%Y-%m-%d %H:%M:%S")
        update_by = ' '.join(filter(None, (first_name, last_name)))
        return 200, {"update_date": update_date, "update_by": update_by}
