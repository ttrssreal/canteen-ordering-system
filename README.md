# Burnside High School - Canteen Ordering System

### This is a school project.

### Description
A web-app to manage student orders at the canteen. The backend is python3 with Flask, SQLAlchemy, SQLite etc.

### Dev environment

To run a dev environment:\
`git clone git@github.com:ttrssreal/canteen-ordering-system.git`\
`cd canteen-ordering-system`

Make and enter a new virtual environment:\
`python3 -m venv deploy/env`\
`source deploy/env/bin/activate`

Install required python packages:\
`pip3 install -r deploy/requirements.txt`

The following enviroment variables need to be set:
```
DATABASE_LOCATION=sqlite:///path_to_project_root/database/canteendb
FLASK_APP=src/app.py
SECRET=secret
```

To run database migrations:\
`flask db upgrade`

Then to start:\
`python3 src/app.py`

### Deploy

`git clone git@github.com:ttrssreal/canteen-ordering-system.git`\
`cd canteen-ordering-system`

A `.env` file is needed in the project root directory with the following contents:
```
DATABASE_LOCATION=sqlite:////app/database/canteendb
FLASK_APP=src/app.py
SECRET=secret
```

Then to launch the container:\
`docker-compose up`