from django.contrib import admin
from django.db import models
from django.utils import timezone

from account.models import User


class SoftDeleteModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_deleted',)
    list_filter = ('is_deleted',)
    actions = ['soft_delete_selected', 'restore_selected']

    def soft_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.soft_delete(user=request.user)

    soft_delete_selected.short_description = "Soft delete selected objects"

    def restore_selected(self, request, queryset):
        for obj in queryset:
            obj.restore()

    restore_selected.short_description = "Restore selected objects"

    def get_queryset(self, request):
        qs = self.model.all_objects.get_queryset()
        return qs


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
    deleted_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def soft_delete(self, user=None):
        for field in self._meta.get_fields():
            if (field.one_to_many or field.one_to_one) and field.auto_created:
                related_objects = getattr(self, field.get_accessor_name()).all()
                for obj in related_objects:
                    obj.delete()
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save()

    def delete(self, using=None, keep_parents=False, user=None):
        self.soft_delete(user=user)

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save()

    class Meta:
        abstract = True
