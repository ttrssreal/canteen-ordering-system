# Burnside High School - Canteen Ordering System


## Execution enviroment
requirements - python3, git

git clone https://github.com/ttrssreal/canteen-ordering-system.git
cd canteen-ordering-system/deploy
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

A `src/.env` file is needed with the following:
```
DATABASE_LOCATION=sqlite://the_database_location
SECRET=secret
FLASK_APP=src/app.py
```
## Execution
python3 ../src/app.py
