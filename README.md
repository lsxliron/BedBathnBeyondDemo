# Bed Bath & Beyond Demo

### Get Started
- Clone the repository
- To install the JavaScript dependencies, run ```bower install```. If you don't have ```bower``` installed, 
you can install it using npm: 
```
   npm install bower -g
```
- Create a virtual environment ```virtual env .env --no-site-packages````
- Activate the new environment ```source .env/bin/activate```
- Navigate to the clone repository and install dependecies ```pip install -r requirements.txt```
- Initialize the database: 
```
   python manage.py makemigrations demo
   python manage.py migrate
```
- Now we need to create some fake data. For that, we have to access the models from django shell: 

```
   python manage.py shell
```
- From django shell, we run ```execfile('createData.py')```
- Now, after we setup everything, we can quit the Django shell and run ```python manage runserver```
- Open your browser and navigate to ```localhost:8000```

####Note:
The docs are hosted separately from the Django app. To serve them, I use the python built in server.
Navigate to ```BedBathnBeyondDemo/docs/build/html``` and run
```
   python -m SimpleHTTPServer 3000
```
