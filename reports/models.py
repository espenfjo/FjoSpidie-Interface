# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Alert(models.Model):
    id = models.IntegerField(primary_key=True)
    report = models.ForeignKey('Report')
    alarm_text = models.TextField(blank=True)
    classification = models.TextField(blank=True)
    priority = models.IntegerField(blank=True, null=True)
    protocol = models.CharField(max_length=10, blank=True)
    from_ip = models.TextField(blank=True)
    to_ip = models.TextField(blank=True)
    time = models.TextField(blank=True)
    request = models.ForeignKey('Request', db_column='request', blank=True, null=True)
    http_method = models.TextField(blank=True)
    http_request = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'alert'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class Cookie(models.Model):
    id = models.IntegerField(primary_key=True)
    response = models.ForeignKey('Response', blank=True, null=True)
    name = models.TextField(blank=True)
    value = models.BinaryField(blank=True, null=True)
    path = models.TextField(blank=True)
    domain = models.TextField(blank=True)
    expires = models.TextField(blank=True)
    httponly = models.TextField(blank=True)
    secure = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'cookie'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

class Download(models.Model):
    id = models.IntegerField(primary_key=True)
    report = models.ForeignKey('Report')
    data = models.BinaryField(blank=True, null=True)
    md5 = models.TextField(blank=True)
    sha1 = models.TextField(blank=True)
    sha256 = models.TextField(blank=True)
    size = models.IntegerField(blank=True, null=True)
    uuid = models.TextField(blank=True) # This field type is a guess.
    filename = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'download'

class Entry(models.Model):
    id = models.IntegerField(primary_key=True)
    report = models.ForeignKey('Report')
    url = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'entry'

class Graph(models.Model):
    id = models.IntegerField(primary_key=True)
    report = models.ForeignKey('Report')
    graph = models.BinaryField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'graph'

class Header(models.Model):
    id = models.IntegerField(primary_key=True)
    entry = models.ForeignKey(Entry, blank=True, null=True)
    name = models.TextField(blank=True)
    value = models.TextField(blank=True)
    type = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'header'

class Pcap(models.Model):
    id = models.IntegerField(primary_key=True)
    report = models.ForeignKey('Report', blank=True, null=True)
    data = models.BinaryField(blank=True, null=True)
    uuid = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        managed = False
        db_table = 'pcap'

class Report(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.TextField(blank=True)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField(blank=True, null=True)
    uuid = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        managed = False
        db_table = 'report'

class Request(models.Model):
    id = models.IntegerField(primary_key=True)
    entry = models.ForeignKey(Entry, blank=True, null=True)
    bodysize = models.IntegerField(blank=True, null=True)
    headersize = models.IntegerField(blank=True, null=True)
    method = models.TextField(blank=True)
    uri = models.TextField(blank=True)
    httpversion = models.TextField(blank=True)
    host = models.TextField(blank=True)
    port = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'request'

class Response(models.Model):
    id = models.IntegerField(primary_key=True)
    entry = models.ForeignKey(Entry, blank=True, null=True)
    httpversion = models.TextField(blank=True)
    statustext = models.TextField(blank=True)
    status = models.IntegerField(blank=True, null=True)
    bodysize = models.IntegerField(blank=True, null=True)
    headersize = models.IntegerField(blank=True, null=True)
    content = models.BinaryField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'response'

class ResponseContent(models.Model):
    id = models.IntegerField(primary_key=True)
    response = models.ForeignKey(Response, blank=True, null=True)
    md5 = models.TextField(blank=True)
    data = models.TextField(blank=True)
    size = models.IntegerField(blank=True, null=True)
    path = models.TextField(blank=True)
    mimetype = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'response_content'

class Screenshot(models.Model):
    id = models.IntegerField(primary_key=True)
    report = models.ForeignKey(Report, blank=True, null=True)
    image = models.BinaryField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'screenshot'

class Yara(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.ForeignKey(ResponseContent, blank=True, null=True)
    rule = models.TextField(blank=True)
    description = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'yara'

class YaraString(models.Model):
    id = models.IntegerField(primary_key=True)
    yara = models.ForeignKey(Yara, blank=True, null=True)
    string = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'yara_string'

class YaraTag(models.Model):
    id = models.IntegerField(primary_key=True)
    yara = models.ForeignKey(Yara, blank=True, null=True)
    tag = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'yara_tag'

