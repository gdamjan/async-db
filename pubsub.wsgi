import gevent_psycopg2
gevent_psycopg2.monkey_patch()

import gevent.monkey
gevent.monkey.patch_thread()

DSN = "postgresql+psycopg2://postgres@/"

import itertools
import uwsgidecorators

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import gevent

engine = create_engine(DSN)
DBSession = sessionmaker(bind=engine)

def publisher(session):
    for i in itertools.count():
        data = 'message %d' % i
        session.execute('select pg_sleep(5)')
        session.execute("NOTIFY topic, :data", {'data': data})
        session.commit()

session = DBSession()
gevent.spawn(publisher, session)


def subscriber(session):
    sa_conn = session.bind.connect()
    sa_conn.detach()
    pg_conn = sa_conn.connection.connection
    pg_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    sa_conn.execute('LISTEN topic')
    while True:
        gevent.socket.wait_read(pg_conn.fileno())
        pg_conn.poll()
        while pg_conn.notifies:
            notify = pg_conn.notifies.pop()
            yield notify.payload
    sa_conn.execute('UNLISTEN topic')
    sa_conn.close()


def application(env, start_response):
    start_response('200 OK', [('content-type', 'text/plain')])

    session = DBSession()
    yield 'start\n'
    for msg in subscriber(session):
        yield "%s\n" % msg
    yield 'end\n'

