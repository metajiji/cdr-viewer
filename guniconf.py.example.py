from multiprocessing import cpu_count

# Server sockets
bind = '127.0.0.1:5000'  # See nginx vhost config.
backlog = 1024

workers = cpu_count() * 2 + 1
worker_class = 'gevent'  # pip install gevent
worker_connections = 1024
timeout = 30
keepalive = 2

# Debugging
debug = False
spew = False

# Server mechanics
daemon = False
pidfile = 'gunicorn.pid'
errorlog = '-'
access_log_format = '%(X-Forwarded-For)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
