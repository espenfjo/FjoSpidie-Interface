from django.contrib import admin
from reports.models import Report, Entry, Alert, Request, Response, Header, Download, Pcap, Graph

admin.site.register(Report)
admin.site.register(Entry)
admin.site.register(Alert)
admin.site.register(Request)
admin.site.register(Response)
admin.site.register(Header)
admin.site.register(Download)
admin.site.register(Pcap)
admin.site.register(Graph)


# Register your models here.
