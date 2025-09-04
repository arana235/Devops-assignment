# WSGI entrypoint for gunicorn
from aceest_fitness import create_app
app = create_app()
