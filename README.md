### Install

```
pip install -r requirements.txt
```

### Config

setup FLASK_CONFIG，or default is 'default'
```
export FLASK_CONFIG="production"
```

setup db
```
python manage.py db init
python manage.py db setup_db
```
### Run

```
python manage.py runserver
```

### Test

run test
```
python manage.py test
```
