from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin

admin.site.register(models.Teacher)
admin.site.register(models.CourseCategory)
admin.site.register(models.Chapter)
admin.site.register(models.Student)
admin.site.register(models.Admin)
admin.site.register(models.Class)
admin.site.register(models.Schedule)
# Register your models here.
admin.site.site_header = "LeaderShip Sclass"