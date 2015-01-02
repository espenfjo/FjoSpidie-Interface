import gridfs
import uuid
import simplejson
import re

from bson.objectid import ObjectId
from django.db import connections
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext

from reports.forms import JobForm
from reports.jobs import job
from reports.models import Report, GeoIP


def dashboard(request):
    if request.POST:
        form = JobForm(request.POST)
        if form.is_valid():
            uid = uuid.uuid4()
            job(uid, form.cleaned_data['url'],
                form.cleaned_data['useragent'], form.cleaned_data['referer'])
            return HttpResponseRedirect(reverse('report', args=[uid]))

        else:
            print form
    else:
        reports = Report.objects.only('starttime', 'alerts', 'uuid', 'url').order_by("-starttime")
    return render_to_response("index.html",
                              {"reports": reports},
                              context_instance=RequestContext(request))


def pcap(request, uuid):
    pass
#    r = get_object_or_404(Report, uuid=uuid)
#    p = get_object_or_404(Pcap.objects.select_related(), report=r.id)
#    response = HttpResponse(p.data, content_type='application/octet-stream')
#    response['Content-Length'] = len(p.data)
#    return response


def pcap_size(rid):
    pass
# cursor = connection.cursor()
# statement = "SELECT LENGTH(data) from pcap where report_id = %s";

# cursor.execute(statement, [rid])
# records = cursor.fetchall()
# if records:
#     return records[0][0]
# else:
#     return None


def graph(request, uuid):
    r = get_object_or_404(Report, uuid=uuid)
    try:
        db = connections['default']
        fs = gridfs.GridFS(db.database)
        if fs.exists(ObjectId(r.graph_id)):
            gridfile = fs.get(ObjectId(r.graph_id))
    except Exception, e:
        raise Http404
    else:
        image = gridfile.read()
        response = HttpResponse(image, mimetype="image/png")
        response['Content-Length'] = len(image)
        return response


def screenshot(request, uuid):
    r = get_object_or_404(Report, uuid=uuid)
    try:
        db = connections['default']
        fs = gridfs.GridFS(db.database)
        if fs.exists(ObjectId(r.screenshot_id)):
            gridfile = fs.get(ObjectId(r.screenshot_id))
    except Exception, e:
        raise Http404
    else:
        image = gridfile.read()
        response = HttpResponse(image, mimetype="image/png")
        response['Content-Length'] = len(image)
        return response


def report(request, uuid):
    try:
        r = Report.objects.get(uuid=uuid)
    except Report.DoesNotExist:
        return render(request, 'report.html', {'done': False})
    if not r.endtime:
        raise Http404
    relationships = find_relations(r)
    data = {
        'report':    r,
        'rip': get_ip_html(r.ip, r.geoip),
        'relationships': relationships,
        'alerts':    r.alerts,
        'downloads': r.downloads,
        'headers':   headers_html(headers(r.entries)),
        'pcap':      pcap_size(r),
        'yaras':     yara_matches(r)
    }

    return render(request, 'report.html', data)

def find_relations(report):
    """
    Find relations to other reports/analysis
    """
    relations = {
        'connections': {},
        'urls': {}
    }
    db = connections['default']
    col = db.get_collection('analysis')
    urls = []
    import cProfile, pstats
    import StringIO
    pr = cProfile.Profile()
    pr.enable()
    print "Finding connections"
    for connection in report.connections:
        for c_report in col.find({"$and": [{"connections": connection}, {"_id": {"$ne": ObjectId(report._id)}}]}):
            if not connection in relations['connections']:
                relations['connections'][connection] = []
            relations['connections'][connection].append({"uuid":c_report['uuid'], "url":c_report['url']})
    pr.disable()
    s = StringIO.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats()
    print s.getvalue()

    print "found conns"
    print "Finding urls"
    pr.enable()
    for entry in report.entries:
        print "Finding for {}".format(entry.url)
        for m_report in col.find({"$and": [{"entries.url": entry.url}, {"_id": {"$ne": ObjectId(report._id)}}]}):
            if not entry.url in relations['urls']:
                relations['urls'][entry.url] = []
            relations['urls'][entry.url].append({"uuid":m_report['uuid'], "url":m_report['url']})
    pr.disable()
    s = StringIO.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats()
    print s.getvalue()

    return relations

def get_ip_html(ip, ipdata):
    if not ip:
        return ""
    if isinstance(ipdata, GeoIP):
        ipdata = ipdata.__dict__
        if '_state' in ipdata:
            ipdata.pop('_state')
            ipdata.pop('_original_pk')
    ipdata_formatted = simplejson.dumps(ipdata, sort_keys=True, indent=4)
    ipdata_formatted = ipdata_formatted.replace("\n", "<br>\n")

    html = """<div class="popoverip btn" data-content='<code class="prettify">{}</code>' """.format(ipdata_formatted)
    html += """rel="popover" data-placement="bottom" data-html="true" data-original-title="{}" """.format(ip)
    html += """data-trigger="hover"><b>"""
    if ipdata['country_code']:
        html += '<img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" class="flag flag-{}" alt="{}" /> '.format(ipdata['country_code'].lower(), ipdata['country_name'])
    html += ip
    html += """</b></div>"""

    return html

def headers_html(headers):
    """
    Since Django / Templates are slow, make our own html
    """
    html = ""
    for header in headers:
        html += """<tr id='""" + str(header['entry_num']) + """' class="connection">
<td class="headers">
  <b>"""
        html += header['method'] + " " + header['uri'] + \
            " " + header['request_http_version']
        html += """<br>
    <br>
  </b>
  <div class="headers">"""
        for request_headers in header['request_header']:
            ip_html = get_ip_html(header['ip'], header['ipdata'])
            html += u"<b> {}: </b>{} <br>".format(request_headers.name,
                                                  request_headers.value)
        html += """</div>
</td>
<td class="headers">
<b>"""
        html += ip_html
        html += "<br>"
        html += "{} {} {}".format(header['status'],
                                  header['status_text'], header['response_http_version'])
        html += """<br>
    <br>
  </b>
  <div class="headers">"""
        for response in header['response_header']:
            html += u"<b>{}: </b> {} <br>".format(response.name,
                                                  response.value)
        html += "</div>"

    return html


def yara_matches(report):
    data = []
    for entry in report.entries:
        matches = []
        for match in entry.parser_match:
            match.entry_num = entry.num
            matches.append(match)
        data.extend(matches)
    return data


def headers(entries):
    headers = []
    for entry in entries:
        response = entry.response
        request = entry.request
        headers.append({
            'status': response.status,
            'host': request.hostname,
            'method': request.method,
            'uri': request.url,
            'request_http_version': request.http_version,
            'status_text': response.status_text,
            'response_http_version': response.http_version,
            'request_header': request.headers,
            'response_header': response.headers,
            'entry_num': entry.num,
            'ip': entry.ip
        })

    return headers
