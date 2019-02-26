from django.contrib import admin
from web import models
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','content']
class TaskLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'result']
# Register your models here.
admin.site.register(models.HostGroup)
admin.site.register(models.Host)
admin.site.register(models.HostToRemoteUser)
admin.site.register(models.IDC)
admin.site.register(models.RemoteUser)
admin.site.register(models.UserProfile)
admin.site.register(models.Task,TaskAdmin)
admin.site.register(models.TaskLogDetail,TaskLogAdmin)