from django.contrib import admin
from .models import Admin, User

admin.site.site_header = "PPL LOS Admin"
admin.site.index_title = "Welcome to PPL LOS Admin Portal"
admin.site.register(Admin)
admin.site.register(User)