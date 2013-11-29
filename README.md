FjoSpidie-Interface
===================

FjoSpidie Honey Client web interface

`python manage.py runserver`

Or, uwsgi: 

    [uwsgi]
    chdir=/home/espen/SpidieFace
    module=SpidieFace.wsgi:application
    master=True
    pidfile=/tmp/project-master.pid
    vacuum=True
    env DJANGO_SETTINGS_MODULE=SpidieFace.settings
    home=/home/espen/Sources/fjospidie_virtual
    max-requests=5000
    daemonize=/var/log/spidieface.log
    socket=/tmp/spidie.sock
    master
    processes=5
    plugins=python

