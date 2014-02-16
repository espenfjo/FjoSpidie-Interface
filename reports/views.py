from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.db import connection
import sys
import collections
from reports.models import Report, Alert, Download, Entry, Graph, Pcap, Screenshot
from django.db.models import Count, Sum
from django.utils.encoding import smart_text
from reports.forms import JobForm
from reports.jobs import job
import uuid

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'reports'

    def get_queryset(self):
        cursor = connection.cursor()
        statement = "SELECT r.id, r.url, r.uuid, r.starttime, count(a.id)  as alerts FROM report r LEFT JOIN alert a ON a.report_id = r.id WHERE r.endtime IS NOT NULL GROUP BY r.id ORDER BY r.starttime DESC";

        cursor.execute(statement)
        records = cursor.fetchall()
        data = []
        for report in records:
            data.append({
                'id':report[0],
                'url':report[1],
                'uuid':report[2],
                'starttime':report[3],
                'alerts':report[4],
            })
        return data

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['uuid'] = uuid.uuid4

        return context

class DetailView(generic.DetailView):
    model = Report
    template_name = 'report.html'


def pcap(request, uuid):
    r = get_object_or_404(Report, uuid=uuid)
    p = get_object_or_404(Pcap.objects.select_related(), report=r.id)
    response = HttpResponse(p.data, content_type='application/octet-stream')
    response['Content-Length'] = len(p.data)
    return response

def pcap_size( rid ):
    cursor = connection.cursor()
    statement = "SELECT LENGTH(data) from pcap where report_id = %s";

    cursor.execute(statement, [rid])
    records = cursor.fetchall()
    if records:
        return records[0][0]
    else:
        return None

def graph(request, uuid):
    r = get_object_or_404(Report, uuid=uuid)
    g = get_object_or_404(Graph.objects.select_related(), report=r.id)
    response = HttpResponse(g.graph, content_type='image/png')
    response['Content-Length'] = len(g.graph)
    return response

def screenshot(request, uuid):
    r = get_object_or_404(Report, uuid=uuid)
    s = get_object_or_404(Screenshot.objects.select_related(), report=r.id)
    response = HttpResponse(s.image, content_type='image/png')
    response['Content-Length'] = len(s.image)
    return response

def report(request, uuid):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job(uuid, form.cleaned_data['url'], form.cleaned_data['useragent'], form.cleaned_data['referer'])
            return render(request, 'report.html', {})
        else:
            print form
    else:
        r = get_object_or_404(Report, uuid=uuid)

    if not r.endtime:
        raise Http404

    yara = yara_matches(r.uuid)
    data = {
        'report':    r,
        'alerts':    Alert.objects.filter(report=r.id),
        'downloads': Download.objects.filter(report=r.id),
        'headers':   headers_html(headers(r.uuid)),
        'pcap':      pcap_size(r.id),
        'yaras':     yara
    }

    return render(request, 'report.html', data )

def headers_html(headers):
    html = ""
    for key,header in headers.items():
        html+="""<tr id='""" + str(header['rid']) + """' class="connection">
        <td class="headers">
          <b>"""
        html += header['method'] + " " + header['uri'] + " " + header['rhttpversion']
        html +="""<br>
            <br>
          </b>
          <div class="headers">"""
        for request_headers in header['request_header']:
            html += u"<b> {}: </b>{} <br>".format(request_headers['name'],request_headers['value'])
        html += """</div>
        </td>
        <td class="headers">
          <b>"""
        html += "{} {} {}".format(header['status'], header['statustext'], header['httpversion'])
        html +="""<br>
            <br>
          </b>
          <div class="headers">"""
        for response in header['response_header']:
            html +=u"<b>{}: </b> {} <br>".format(response['name'], response['value'])
        html +="</div>"

    return html


def yara_matches(uuid):
    statement ="SELECT y.id, y.rule, y.description, r.id, request.id FROM yara y JOIN response_content rc on y.content_id = rc.id JOIN response r ON rc.response_id=r.id JOIN entry e ON r.entry_id = e.id JOIN report on e.report_id=report.id LEFT JOIN request ON request.entry_id = e.id WHERE ( report.uuid = %s )"
    cursor = connection.cursor()

    cursor.execute(statement, [uuid])
    records = cursor.fetchall()
    data = []
    for match in records:
        id          = match[0]
        rule        = match[1]
        description = match[2]
        response_id = match[3]
        request_id  = match[4]

        data.append({'id': id, 'rule': rule, 'description': description, 'response_id':response_id, 'request_id':request_id })
    return data


def headers(uuid):
    from time import time
    start = time()
    cursor = connection.cursor()
    statement = "SELECT me.id, me.entry_id, me.name, me.value, me.type, requests.host, requests.port, responses.httpversion, responses.statustext, responses.status, responses.bodysize, responses.headersize, requests.bodysize, requests.headersize, requests.method, requests.uri, requests.httpversion, requests.id FROM header me JOIN entry entry ON entry.id = me.entry_id JOIN report report ON report.id = entry.report_id LEFT JOIN response responses ON responses.entry_id = entry.id LEFT JOIN request requests ON requests.entry_id = entry.id WHERE ( report.uuid = %s ) ORDER BY requests.id ASC";

    cursor.execute(statement, [uuid])
    records = cursor.fetchall()
    data = collections.OrderedDict()

    for header in records:
        id           = header[0]
        entry_id     = header[1]
        name         = header[2]
        value        = header[3]
        type         = header[4]
        host         = header[5]
        port         = header[6]
        httpversion  = header[7]
        statustext   = header[8]
        status       = header[9]
        method       = header[14]
        uri          = header[15]
        rhttpversion = header[16]
        rid          = header[17]

        if not entry_id in data:
            data[entry_id] ={ 'entry_id':entry_id, 'status':status,  'host':host, 'port':port, 'method':method, 'uri':uri, 'rhttpversion':rhttpversion, 'statustext':statustext, 'httpversion':httpversion, 'request_header':[], 'response_header':[], 'rid': rid}

        for d in data:
            if data[d]['entry_id'] == entry_id:
                if type == 'request':
                    data[d]['request_header'].append({'name':name,'value':value})
                else:
                    data[d]['response_header'].append({'name':name,'value':value})
    return data
