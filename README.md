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

=======
FjoSpidie Interface
===================
This is a WEB interface for the FjoSpidie Honey Client.
It is based on Perl and Catalyst MVC.

Building
========
* `perl Makefile.PL`
* `make`

Usage
=====
Run script/fjospidie_server.pl to start the application.

See https://www.dropbox.com/s/eiwul3ipmqto57s/Screenshot%202013-10-26%2021.35.40.png for how it looks.
