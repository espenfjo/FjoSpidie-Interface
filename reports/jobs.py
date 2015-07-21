import sys
import docker
from django.conf import settings
from django.utils.encoding import smart_str

def job(uuid, url, useragent, referer):
    c = docker.Client(base_url='tcp://172.17.42.1:2375', version="1.7")
    image = "espenfjo/fjospidie:latest"

    fjospidie_cmd = "--debug --url '{}' --uuid '{}'".format(smart_str(url),uuid)
    if referer:
        fjospidie_cmd += " --referer '{}'".format(referer)
    if useragent:
        fjospidie_cmd += " --useragent '{}'".format(useragent)

    environment = {
        "MONGO_HOST": settings.DATABASES['default']['HOST']
        }
    if settings.DATABASES['default']['PORT']:
        environment['MONGO_PORT'] = settings.DATABASES['default']['PORT']
    container = c.create_container(image, command=fjospidie_cmd, volumes={"/mnt/fjospidie":{}}, detach=True, environment=environment)
    c.start(container, binds={'/mnt/fjospidie':'/mnt/fjospidie', '/var/run/suricata/':'/var/run/suricata/'}, lxc_conf=None)
