"""
Gunicorn Production Configuration
Run with: gunicorn -c gunicorn_config.py app:app
"""

# Server socket configuration
bind = "0.0.0.0:5000"
backlog = 2048
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "proconnect-backend"

# Server hooks
def post_fork(server, worker):
    """Called after a worker has been spawned"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_int(worker):
    """Called when a worker is interrupted"""
    worker.log.info("Worker interrupted (pid: %s)", worker.pid)

# Deployment settings
daemon = False
pidfile = "/tmp/gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# Development/Production mode
raw_env = ["FLASK_ENV=production"]
