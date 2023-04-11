# splendia
Web interface to play Splendor, solo game against différent kind of AIs.


To create the correct python virtual environnement :
```
python -m venv env
```
To enter the virtual environnement :
```
source env/bin/activate
```
To install the necessary dependancies :
```
pip install -r requirements.txt
```
To quit the virtual environnement :
```
deactivate
```

To run the backend :
---
Place yourself in splendia_backend then run :
```
python manage.py runserver 8080
```
To create and update the database:
---

Place yourself in splendia_backend then run :
```
python manage.py migrate api
```


To run tests on the model :
```
python -m unittest -v
```
