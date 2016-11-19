# This file starts the WSGI web application.
# - Heroku starts gunicorn, which loads Procfile, which starts runserver.py
# - Developers can run it from the command line: python runserver.py

from app.app_and_db import app, db
from app.startup.init_app import init_app
import os

application = app
init_app(application, db)

# Start a development web server if executed from the command line
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=True)
