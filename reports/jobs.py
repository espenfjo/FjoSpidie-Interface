import sys
import docker
from django.utils.encoding import smart_str

def job(uuid, url, useragent, referer):
    c = docker.Client(base_url='unix://var/run/docker.sock', version="1.7")
    image = "espenfjo/fjospidie:latest"

    fjospidie_cmd = "cd /opt/fjospidie;pwd; xvfb-run -a python fjospidie.py --debug --url '{}' --uuid '{}'".format(smart_str(url),uuid)
    if referer:
        fjospidie_cmd += " --referer '{}'".format(referer)
    if useragent:
        fjospidie_cmd += " --useragent '{}'".format(useragent)

    command = "bash -c \"{}\"".format(fjospidie_cmd)

    container = c.create_container(image, command=command, volumes={"/mnt/fjospidie":{}}, detach=True)
    c.start(container, binds={'/mnt/fjospidie':'/mnt/fjospidie'}, lxc_conf=None)
