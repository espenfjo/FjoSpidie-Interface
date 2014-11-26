from django.contrib import admin
from reports.models import Report, Entry, Request, Response

admin.site.register(Report)
admin.site.register(Entry)
admin.site.register(Request)
admin.site.register(Response)


# Register your models here.
