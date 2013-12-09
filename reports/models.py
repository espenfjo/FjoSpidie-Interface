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
    time  = models.TextField(blank=True)
    request = models.ForeignKey('Request', blank=True, null=True, db_column="request")
    http_method = models.TextField(blank=True)
    http_request = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'alert'
    def __unicode__(self):
        return "{} {} {} {} {}".format(self.alarm_text, self.from_ip,self.to_ip,self.protocol,self.classification)
        
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
    def __unicode__(self):
        return "{} {} {} {} {} {}".format(self.filename, self.size, self.md5, self.sha1, self.sha256, self.uuid)

class Entry(models.Model):
    id = models.IntegerField(primary_key=True)
    report = models.ForeignKey('Report')
    class Meta:
        managed = False
        db_table = 'entry'
    def __unicode__(self):
        return str(self.id)

class Graph(models.Model):
    id = models.IntegerField(primary_key=True)
    report = models.ForeignKey('Report')
    graph = models.BinaryField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'graph'
    def __unicode__(self):
        if graph:            
            return "We have a graph, wont print it here..."
        else:
            return "No graph.. :("

class Screenshot(models.Model):
    id = models.IntegerField(primary_key=True)
    report = models.ForeignKey('Report')
    image = models.BinaryField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'screenshot'
    def __unicode__(self):
        if graph:            
            return "We have a screenshot, wont print it here..."
        else:
            return "No screenshot.. :("


class Header(models.Model):
    id = models.IntegerField(primary_key=True)
    entry = models.ForeignKey(Entry, blank=True, null=True)
    name = models.TextField(blank=True)
    value = models.TextField(blank=True)
    type = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'header'
    def __unicode__(self):
        return "{} {}".format(self.name, self.value)

class Pcap(models.Model):
    id = models.IntegerField(primary_key=True)
    report = models.ForeignKey('Report', blank=True, null=True)
    data = models.BinaryField(blank=True, null=True)
    uuid = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        managed = False
        db_table = 'pcap'
    def __unicode__(self):
        return self.uuid

class Report(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.TextField(blank=True)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField(blank=True, null=True)
    uuid = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        managed = False
        db_table = 'report'
    def __unicode__(self):
        return "{} {} {} {}".format(self.url, self.starttime, self.endtime, self.uuid)

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
    def __unicode__(self):
        return "{} {} {} {} {} {} {}".format(self.method, self.uri, self.httpversion,self.host,self.port,self.headersize,self.bodysize)

class Response(models.Model):
    id = models.IntegerField(primary_key=True)
    entry = models.ForeignKey(Entry, blank=True, null=True)
    httpversion = models.TextField(blank=True)
    statustext = models.TextField(blank=True)
    status = models.IntegerField(blank=True, null=True)
    bodysize = models.IntegerField(blank=True, null=True)
    headersize = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'response'
    def __unicode__(self):
        return "{} {} {} {} {} ".format(self.status, self.statustext, self.httpversion, self.bodysize,self.headersize)

