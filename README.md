# Fast API application

Application description

## Before develoopment

* create venv
```
python -m venv venv
```

* activate it
```
source .venv/bin/activate
```

* install dependencies
pip install -r requirements.txt

* in the root directory create file .env
```
touch .env
```

* set up .env file with your credentials 
```
DB_HOSTNAME=[localhost]
DB_PORT=[5432]
DB_NAME=[postgres]
DB_USERNAME=[username]
DB_PASSWORD=[password]
SECRET_KEY=[secret_key]
ALGORITHM=[HS256]
ACCESS_TOKEN_EXPIRE_MINUTES=[60]
```


### Start server
uvicorn app.main:app --reload --port 8000

