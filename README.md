Setup
=====

    export PYTHONUSERBASE=$PWD/py-env
    pip2 install --user -r requirements.txt

Prepare database
================

If you never had postgres setup:

    sudo -u postgres initdb --locale en_US.UTF-8 -D /var/lib/postgres/data
    sudo systemctl start postgresql
    sudo -u postgres createuser $USER
    sudo -u postgres createdb -O $USER $USER

Test
====

Run the app:

    uwsgi --ini uwsgi.ini --thr # to work with 1000 thread workers
    uwsgi --ini uwsgi.ini --gev # to work with 1000 async gevent cores
    uwsgi --ini uwsgi.ini --gev_patch # same as --gev but also patch the threading library

Test requests:

    time curl localhost:8080 -i & \
    time curl localhost:8080 -i & \
    time curl localhost:8080 -i

