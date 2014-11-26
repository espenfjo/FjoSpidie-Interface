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
from django_mongodb_engine.contrib import MongoDBManager
from django_mongodb_engine.storage import GridFSStorage
from djangotoolbox.fields import EmbeddedModelField, ListField, DictField


from django.db import models

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

class Report(models.Model):
    _id = models.TextField(primary_key=True)
    url = models.TextField(blank=True)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField(blank=True, null=True)
    uuid = models.TextField(blank=True)
    screenshot_id = models.TextField(blank=True)
    graph_id = models.TextField(blank=True)
    entries = ListField(EmbeddedModelField('Entry'))
    alerts = ListField(EmbeddedModelField('Alerts'))
    downloads = ListField(EmbeddedModelField('Downloads'))
    
    objects = MongoDBManager()
    class MongoMeta:
        db_table="analysis"

class Entry(models.Model):
    url = models.TextField()
    num = models.TextField()
    content = EmbeddedModelField('Content')
    request = EmbeddedModelField('Request')
    response = EmbeddedModelField('Response')
    parser_match = ListField(EmbeddedModelField('YaraMatch'))


class Alerts(models.Model):
    src = models.TextField()
    dst = models.TextField()
    alarm_text = models.TextField()
    classification = models.TextField()
    priority = models.IntegerField()
    http_method = models.TextField()
    time = models.TextField()
    http_request = models.TextField()
    request_id = models.IntegerField()


class Downloads(models.Model):
    pass

class Headers(models.Model):
    header_type = models.TextField()
    name = models.TextField()
    value = models.TextField()

class Request(models.Model):
    _id = models.TextField()
    hostname = models.TextField()
    method = models.TextField()
    url = models.TextField()
    http_version = models.TextField()
    headers = ListField(EmbeddedModelField('Headers'))

class Response(models.Model):
    id = models.TextField(primary_key=True)
    status = models.TextField()
    status_text = models.TextField()
    http_version = models.TextField()
    headers = ListField(EmbeddedModelField('Headers'))
    
class Content(models.Model):
    content_id = models.TextField()
    md5 = models.TextField()
    mime_type = models.TextField()
    size = models.IntegerField()

class YaraMatch(models.Model):
    description = models.TextField()
    rule = models.TextField()
    tags = models.TextField()
