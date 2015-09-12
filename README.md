# RaspiDrink

Raspidrink is a Raspberry Pi project used to build a cocktail maker machine.
The whole project is made in two part:
* The web GUI
* The Raspberry API.

## Installation 
You can either install this part of the project on a Rpi or on another Linux server for more performence.

### Install necesary packages
```
sudo apt-get install python-dev python-pip
```
### Install Django framework and some libs
```
sudo pip install Django==1.7.10
sudo pip install django-dajaxice
sudo pip install django-dajax
sudo pip install requests
```

### Check the installation.
This command should show you your current Django version.
```
python -c "import django; print(django.get_version())"
```

### Clone the project
```

```

### Create the database
```
python manage.py makemigrations
python manage.py migrate
```

### Create admin user
This account will be allowed to access the admin section of RaspiDrink
```
python manage.py createsuperuser
```


Use Django's server to run Raspidrink
==========

It's not the best practice but it's easy and fast. Recommanded if you are running the code from a Rpi.

As pi user :

Copy the init script and add it to the startup
```
sudo cp RaspiDrink/run_raspidrink/init_script/raspidrink.sh /etc/init.d/raspidrink
sudo chmod +x /etc/init.d/raspidrink
sudo update-rc.d raspidrink defaults
```
You can edit it to customise settings.
Start Raspidrink :
```
sudo /etc/init.d/raspidrink start
```
That's it, you can now access your raspidrink at http://youip:8000