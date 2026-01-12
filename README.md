# SmartCalc-Backend
ssh valifea1@50.6.18.74
 
password: 6elxJ6nyNrzAerPy

cd SmartCalc

pip freeze > requirements.txt

pip install -r requirements.txt

Create a Python virtual environment:

python -m venv venv

venv\Scripts\activate

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver


python manage.py startapp adminpanel

hosting link = https://smartcalc-pv5v.onrender.com/

change password api POST /api/users/change-password/
