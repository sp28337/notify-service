from app.core.settings import settings as s

bind = s.gunicorn.bind
workers = s.gunicorn.workers
worker_class = s.gunicorn.worker_class
timeout = s.gunicorn.timeout
keepalive = s.gunicorn.keepalive

access_log_format = s.gunicorn.access_log_format
error_logfile = s.gunicorn.error_logfile
access_logfile = s.gunicorn.access_logfile

graceful_timeout = s.gunicorn.graceful_timeout
loglevel = s.gunicorn.loglevel
