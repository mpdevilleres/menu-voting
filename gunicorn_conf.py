import multiprocessing

from pprint import pprint

# Gunicorn config variables
loglevel = "info"
workers = multiprocessing.cpu_count()  # make sure to maximize the cores
bind = "0.0.0.0:8000"
errorlog = "-"
accesslog = "-"
graceful_timeout = 600
timeout = 600
keepalive = 5
worker_class = "uvicorn.workers.UvicornWorker"
forwarded_allow_ips = "*"

# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "graceful_timeout": graceful_timeout,
    "timeout": timeout,
    "keepalive": keepalive,
    "errorlog": errorlog,
    "accesslog": accesslog,
}

pprint(log_data)
