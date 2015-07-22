FjoSpidie-Interface
===================

This is a WEB interface for the FjoSpidie Honey Client.
It is written in Python and built on django

Usage
=====
The interface is best run in Docker `docker run --link some-mongo:mongo -p 80:8080 -d espenfjo/spidieface`

To run analysis jobs from the GUI Docker needs to listen to `172.17.42.1:2375`. This can be done by adding `-H tcp://172.17.42.1:2375` to the Docker Daemon options (/etc/default/docker). The WEB GUI will then be able to connect to the Docker daemon to launch `FjoSpidie` jobs.

See http://i.imgur.com/z9Hh0SQ.png for how it looks.
