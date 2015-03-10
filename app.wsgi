import os

if os.environ.get('GEVENT'):
    if os.environ.get('DB') == 'MYSQL':
        import greenify
        greenify.greenify()
        assert greenify.patch_lib('/usr/lib/libmysqlclient.so')
    else:
        import gevent_psycopg2
        gevent_psycopg2.monkey_patch()
    import gevent.monkey
    gevent.monkey.patch_thread()

if os.environ.get('DB') == 'MYSQL':
    DSN = "mysql+oursql://root@/"
    QUERY = "SELECT sleep(5)"
else:
    DSN = "postgresql+psycopg2://localhost/"
    QUERY = "SELECT pg_sleep(5)"


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DSN)
DBSession = sessionmaker(bind=engine)


def application(env, start_response):
    start_response('200 OK', [('content-type', 'text/plain')])

    session = DBSession()
    session.execute(QUERY)

    return ['ok?\n']
