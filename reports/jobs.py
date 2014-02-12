import sys
import docker
from django.utils.encoding import smart_str

def job(uuid, url, useragent, referer):
    c = docker.Client(base_url='unix://var/run/docker.sock', version="1.7")
    image = "espenfjo/fjospidie:latest"
    command = "bash -c \"cd /opt/fjospidie;pwd; xvfb-run -a python fjospidie.py --url '{}' --uuid '{}'\"".format(smart_str(url),uuid)
    if referer:
        command += " --referer '{}'".format(referer)
    if useragent:
        command += " --useragent '{}'".format(useragent)

    container = c.create_container(image, command=command, volumes={"/mnt/fjospidie":{}}, detach=True)
    c.start(container, binds={'/mnt/fjospidie':'/mnt/fjospidie'}, lxc_conf=None)
