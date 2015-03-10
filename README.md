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

Test requests:

    time curl localhost:8080 -i & \
    time curl localhost:8080 -i & \
    time curl localhost:8080 -i & \
    wait


Observations
============

The threading library must be patched when using gevent with SQLAlchemy, since the connection pool uses thread locks.
Those locks will deadlock (huh) the interpreter udner gevent if not patched with `gevent.monkey.patch_thread()`.
SQLAlchemy before 0.9.3 didn't have those locks, but it probably would fail strangely when used with normal threads.
