import multiply.double, multiply.triple

print(multiply.double.double(3))
print(multiply.triple.triple(3))

from multiply.double import double
from multiply.triple import triple

print(double(3))
print(triple(3))

from multiply.double import double as d
from multiply.triple import triple as t

print(d(3))
print(t(3))

#import multiply

#print(multiply.double.double(3))
#print(multiply.triple.triple(3))

# __init__.py
print('The multiply package is now initialized!')
import multiply.double, multiply.triple

# initializing.py
import multiply
print(multiply.double.double(3))
print(multiply.triple.triple(3))

# __init__.py
#print('The multiply package is now initialized!')
#import multiply.double, multiply.triple
__all__ = [
  'double',
  'triple'
]

# initializing.py
from multiply import *

print(dir())


# __init__.py
from example_package import mod1, mod2

# test_package.py

import example_package

example_package.mod1.test_mod1()
example_package.mod2.test_mod2()

# assignment 

python3 -m venv ex1
source ex1/bin/activate
python3 -m pip install colorama
# ls ex1/lib/python3.6/site-packages

source ex2/bin/activate
python3 -m pip uninstall scipy numpy -y
#ls ex2/lib/python3.6/site-packages

source ex3/bin/activate
pip freeze > requirements.txt
cat requirements.txt

source ex4/bin/activate
pip freeze > requirements.txt
pip uninstall -r requirements.txt 
# ls ex4/lib/python3.6/site-packages


## setup.py

from setuptools import setup
setup(
name='my_package',
version='1.0',
author='Calvin & Hobbes',
packages=['my_package'],
)

## terminal build wheel
source ex5/bin/activate
python3 setup.py sdist bdist_wheel

## poetry toml
[tool.poetry]
name = "learning-poetry"
version = "0.1.0"
description = ""
authors = ["Sandipan Dey <sandipan.dey@gmail.com>"]

[tool.poetry.dependencies]
python = "^3.6"

[tool.poetry.dev-dependencies]
pytest = "^5.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"


### github add ssh key
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJvHs/rOm9d40yKcXst5IKcNs9bETa8J4cco4pltuGWO sandipan.dey@gmail.com
git clone git@github.com:codio-content/sw_characters.git
git clone https://github.com/codio-content/sw_characters.git


import requests

def search(search_term='luke'):
  base_url = 'https://swapi.dev/api/people/?search='
  search_url = f'{base_url}{search_term}'
  resp = requests.get(search_url)
  resp_json = resp.json()
  if resp_json.get('results'):
    return resp.json()['results'][0]
  else:
    return None

if __name__ == '__main__':
  import pprint

  character = search()
  pprint.pprint(character)
  
# parse film titles
from sw_characters.search_api import search
import requests

def search(search_term='luke'):
  base_url = 'https://swapi.dev/api/people/?search='
  search_url = f'{base_url}{search_term}'
  resp = requests.get(search_url)
  resp_json = resp.json()
  if resp_json.get('results'):
    return resp.json()['results'][0]
  else:
    return None

def parse_name(person):
  name = person.get('name')
  return name

def parse_planet(person):
  planet_url = person.get('homeworld')
  resp = requests.get(planet_url)
  planet = resp.json().get('name')
  return planet

def parse_films(person):
  film_urls = person.get('films')
  films =[fetch_title(film_url) for film_url in film_urls]
  return films

def fetch_title(url):
  film_json = requests.get(url).json()
  film_title = film_json.get('title')
  return film_title

def format_titles(titles):
  new_lines = [title + '\n' for title in titles]
  formatted_titles = '  * ' + '  * '.join(new_lines)
  return formatted_titles

def person_description(name, planet, titles):
  description = f'{name} is from the planet {planet}. They appear in the following films:\n{titles}'
  return description

if __name__ == '__main__':
  import pprint

  person = search()
  name = parse_name(person)
  planet= parse_planet(person)
  film_list = parse_films(person)
  titles = format_titles(film_list)

  print(titles)

  description = person_description(name, planet, titles)

  print(description)
  
import fire
import search_api

def search(name='luke'):
  print(f'searching for {name}')

if __name__ == '__main__':
  fire.Fire(search)
  
python sw_characters/interface.py --name="boba"

import fire
import search_api

def search(name='luke'):
  characters = search_api.search(name)
  if characters is not None:
    pass
  else:
    print(f'Cannot find the character "{name}"')
    
if __name__ == '__main__':
  fire.Fire(search)
  
python3 sw_characters/interface.py --name="asdf"


## interface.py
import fire
import search_api

def parse_char(char):
  char_name = search_api.parse_name(char)
  planet= search_api.parse_planet(char)
  film_list = search_api.parse_films(char)
  titles = search_api.format_titles(film_list)
  description = search_api.person_description(char_name, planet, titles)
  return description
  
def search(name='luke'):
  characters = search_api.search(name)
  if characters is not None:
    print(parse_char(characters))
  else:
    print(f'Cannot find the character "{name}"')

if __name__ == '__main__':
  fire.Fire(search)


## search_api.py
import requests

def search(search_term='luke'):
  base_url = 'https://swapi.dev/api/people/?search='
  search_url = f'{base_url}{search_term}'
  resp = requests.get(search_url)
  resp_json = resp.json()
  if resp_json.get('results'):
    return resp.json()['results']
  else:
    return None

def parse_name(person):
  name = person.get('name')
  return name

def parse_planet(person):
  planet_url = person.get('homeworld')
  resp = requests.get(planet_url)
  planet = resp.json().get('name')
  return planet

def parse_films(person):
  film_urls = person.get('films')
  films =[fetch_title(film_url) for film_url in film_urls]
  return films

def fetch_title(url):
  film_json = requests.get(url).json()
  film_title = film_json.get('title')
  return film_title

def format_titles(titles):
  new_lines = [title + '\n' for title in titles]
  formatted_titles = '  * ' + '  * '.join(new_lines)
  return formatted_titles

def person_description(name, planet, titles):
  description = f'{name} is from the planet {planet}. They appear in the following films:\n{titles}'
  return description

if __name__ == '__main__':
  import pprint

  person = search()
  name = parse_name(person)
  planet= parse_planet(person)
  film_list = parse_films(person)
  titles = format_titles(film_list)

  print(titles)
  
## interface.py
import fire
import search_api

def search(name='luke'):
  characters = search_api.search(name)
  if characters is not None:
    parse_char_list(characters)
  else:
    print(f'Cannot find the character "{name}"')

def parse_char(char):
  char_name = search_api.parse_name(char)
  planet= search_api.parse_planet(char)
  film_list = search_api.parse_films(char)
  titles = search_api.format_titles(film_list)
  description = search_api.person_description(char_name, planet, titles)
  return description

def parse_char_list(chars):
  for char in chars:
    char_name = search_api.parse_name(char)
    planet= search_api.parse_planet(char)
    film_list = search_api.parse_films(char)
    titles = search_api.format_titles(film_list)
    description = search_api.person_description(char_name, planet, titles)
    print(description)

if __name__ == '__main__':
  fire.Fire(search)
  
conda activate sw
conda install --channel=conda-forge tinydb

## interface.py

import fire
from tinydb import TinyDB, Query
import search_api

db = TinyDB('db.json')
User = Query()

def search(name='luke'):
  characters = search_api.search(name)
  if characters is not None:
    check_db(characters)
  else:
    print(f'Cannot find the character "{name}"')

def parse_char(char):
  char_name = search_api.parse_name(char)
  planet= search_api.parse_planet(char)
  film_list = search_api.parse_films(char)
  titles = search_api.format_titles(film_list)
  description = search_api.person_description(char_name, planet, titles)
  db.insert({'name':char_name, 'planet':planet, 'titles':titles})
  return description

def parse_char_list(chars):
  for char in chars:
    char_name = search_api.parse_name(char)
    planet= search_api.parse_planet(char)
    film_list = search_api.parse_films(char)
    titles = search_api.format_titles(film_list)
    description = search_api.person_description(char_name, planet, titles)
    print(description)

def check_db(chars):
  for char in chars:
    char_name = search_api.parse_name(char)
    results = db.search(User.name == char_name)
    if not results:
      description = parse_char(char)
    else:
      name = results[0]['name']
      planet = results[0]['planet']
      titles = results[0]['titles']
      description = search_api.person_description(name, planet, titles)
    print(description)

if __name__ == '__main__':
  fire.Fire(search)
  

# challenge
conda create -y --name lab-challenge python==3.10.4 
conda activate lab-challenge
conda list

# assignment
poetry remove requests 
poetry add fire
poetry add black --dev 

poetry add beautifulsoup4@latest fire@latest pygame@latest python-twitter@latest
#poetry add beautifulsoup4==4.11.1
#poetry add fire==0.4.0
#poetry add pygame==2.1.2
#poetry add python-twitter==3.5 
#poetry update
#poetry update beautifulsoup4 fire pygame python-twitter
poetry show | grep -E 'beautifulsoup4|fire|pygame|python-twitter'

conda list --revisions
conda install --revision=2


poetry build --format wheel


conda create -y --name ex5 python==3.7
conda activate ex5
conda install scipy flask matplotlib
pip install python-twitter
conda env export > requirements.yaml

## init.py
import today.date, today.fram

## date.py
from datetime import datetime
from datetime import timedelta

def get_info(day):
  offset = -1 if day =='yesterday' else 1 if day =='tomorrow' else 0
  dt_obj = datetime.now() + timedelta(hours = -4) + timedelta(days = offset)
  day = dt_obj.strftime('%A')
  date = dt_obj.strftime('%d')
  month = dt_obj.strftime('%B')
  year = dt_obj.strftime('%Y')
  dt_time = dt_obj.time()
  time = dt_time.strftime('%X')
  return {'day' : day, 'date' : date, 'month' : month, 'year' : year, 'time' : time}

if __name__ == '__main__':
  print(get_info('yesterday'))
  print(get_info('today'))
  print(get_info('tomorrow'))
  
  
## frame.py
import date
import fire

def main(day='today'):
  width = 25
  line = width * '-'
  info = date.get_info(day)
  print(line)
  display_date(day, width, info)
  print(line)

def display_date(day, width, info):
  display_title(day, width)
  center_text(width, info['day'])
  center_text(width, f'{info["date"]} {info["month"]}')
  center_text(width, info['year'])
  if day == 'today':
    center_text(width, info['time'])

def display_title(day, width):
  if day == 'tomorrow':
    title = 'Tomorrow Will Be:'
  elif day == 'yesterday':
    title = 'Yesterday Was:'
  else:
    title = 'Today Is:'
  line = len(title) * '-'
  center_text(width, title)
  center_text(width, line)

def center_text(width, txt):
  print(f'|{txt.center(width - 2)}|')

if __name__ == '__main__':
  fire.Fire(main)
  
pyinstaller frame.py --name day --paths='/home/codio/workspace/day'
ls dist/day
./dist/day/day

pyi-makespec frame.py --name day --paths='/home/codio/workspace/day' --onefile
./dist/day


from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

class ClickButtons(App):
  def build(self):
    # define the window
    Window.clearcolor = '#34495e'
    Window.size = (150, 300)
    self.window = GridLayout(cols=1)

    # define the widgets
    title = Label(text='Click a Button')
    self.count = 0
    self.count_label = Label(text=str(self.count))
    self.add_button = Button(text='+')
    self.subtract_button = Button(text='-')

    # add widgets
    self.window.add_widget(title)
    self.window.add_widget(self.add_button)
    self.window.add_widget(self.count_label)
    self.window.add_widget(self.subtract_button)

    return self.window

if __name__ == "__main__":
  ClickButtons().run()
  
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

class ClickButtons(App):
  def build(self):
    # define the window
    Window.clearcolor = '#34495e'
    Window.size = (150, 300)
    self.window = GridLayout(cols=1)
    self.window.size_hint = (0.8, 0.95)
    self.window.pos_hint = {'center_x' : 0.5, 'center_y' : 0.5}

    # define the widgets
    title = Label(text='Click a Button',
                  font_size = 18,
                  bold = True,
                  color = '#ecf0f1')
    self.count = 0
    self.count_label = Label(text=str(self.count),
                             font_size = 24,
                             bold = True,
                             color = '#ecf0f1')
    self.add_button = Button(text='+',
                             font_size = 24,
                             bold = True,
                             background_normal = '',
                             background_color = '#27ae60')
    self.subtract_button = Button(text='-',
                                  font_size = 24,
                                  bold = True,
                                  background_normal = '',
                                  background_color = '#c0392b')

    # add widgets
    self.window.add_widget(title)
    self.window.add_widget(self.add_button)
    self.window.add_widget(self.count_label)
    self.window.add_widget(self.subtract_button)

    self.add_button.bind(on_press=self.add_callback)
    self.subtract_button.bind(on_press=self.subtract_callback)

    return self.window

  def add_callback(self, instance):
    self.count += 1
    self.count_label.text = str(self.count)

  def subtract_callback(self, instance):
    self.count -= 1
    self.count_label.text = str(self.count)

if __name__ == "__main__":
  ClickButtons().run()
  
## flask app
# main.py
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def birthday():
    return render_template('birthday.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/check_birthday', methods=['POST'])
def check_birthday():
    user_month = request.form['month']
    user_day = request.form['day']
    dt_obj = datetime.now()
    today_month = dt_obj.strftime('%B')
    today_day = dt_obj.strftime('%d')

    check_month = today_month == user_month
    check_day = today_day == user_day

    if check_month and check_day:
        msg = 'Happy birthday!'
        txt = 'Today is your birthday. Spend it doing something you enjoy with those you enjoy being around.'
    else:
        msg = 'It is not your birthday'
        txt = 'Sadly, today is not your birthday. Try again later.'
        
    return render_template('check.html', value=(msg, txt))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
	
## birthday.html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Birthday</title>
  </head>
  <body>
    {% extends "template.html" %}
    {% block content %}
    
    <h2> Enter your birthday to find out </h2>
    <form action="{{ url_for('check_birthday') }}" method="POST">
        <label for="month">Select a month:</label>
        <select name="month" class="dropdown">
          <option value="January">January</option>
          <option value="February">February</option>
          <option value="March">March</option>
          <option value="April">April</option>
          <option value="May">May</option>
          <option value="June">June</option>
          <option value="July">July</option>
          <option value="August">August</option>
          <option value="September">September</option>
          <option value="October">October</option>
          <option value="November">November</option>
          <option value="December">December</option>
        </select><br>
     <label for="day">Select a day:</label>
        <select name="day" class="dropdown">
          <option value="01">1</option>
          <option value="02">2</option>
          <option value="03">3</option>
          <option value="04">4</option>
          <option value="05">5</option>
          <option value="06">6</option>
          <option value="07">7</option>
          <option value="08">8</option>
          <option value="09">9</option>
          <option value="10">10</option>
          <option value="11">11</option>
          <option value="12">12</option>
          <option value="13">13</option>
          <option value="14">14</option>
          <option value="15">15</option>
          <option value="16">16</option>
          <option value="17">17</option>
          <option value="18">18</option>
          <option value="19">19</option>
          <option value="20">20</option>
          <option value="21">21</option>
          <option value="22">22</option>
          <option value="23">23</option>
          <option value="24">24</option>
          <option value="25">25</option>
          <option value="26">26</option>
          <option value="27">27</option>
          <option value="28">28</option>
          <option value="29">29</option>
          <option value="30">30</option>
          <option value="31">31</option>
        </select>
        <br>
        <input type="submit" value="Check" id="check">
    </form>
    <a href="{{ url_for('about') }}">About</a>
      
    {% endblock %}
  </body>
  
## about.html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>About</title>
  </head>
  <body>
    {% extends "template.html" %}
    {% block content %}
    
    <h2>About This Site</h2>
    <p>This is site is a quick example for learning how to get dockerized Flask app deployed to Heroku.</p>
    <a href="{{ url_for('birthday') }}">Home</a>

    {% endblock %}
  </body>
  
## template.html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Parent Template</title>
  </head>
  <body>
    <header>
      <h1 class="title">Is it My Birthday?</h1>
    </header>

    {% block content %}
    {% endblock %}

  </body>
</html>

## check.html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Check Birthday</title>
  </head>
  <body>
    {% extends "template.html" %}
    {% block content %}
    
    <h2>{{ value[0] }}</h2>
    <p>{{ value[1] }}</p>
    <a href="{{ url_for('birthday') }}">Home</a><br>
    <a href="{{ url_for('about') }}">About</a>
    {% endblock %}
  </body>
  
## style.css
body {
  font-family: "Open Sans", sans-serif;
  text-align: center;
  background-color: #ecf0f1;
  color: #2c3e50;
  font-size: 22px;
}
h1 {
  font-size: 96px;
  color: #2980b9;
}

h2 {
  font-size: 60px;
  color: #2980b9;
}
input {
  font-size: 22px;
  color: #2c3e50;
  margin-bottom: 10px;
  border-radius: 5px;
  border: 2px solid #2c3e50;
  background-color: #ecf0f1;
}
.dropdown {
  font-size: 16px;
  padding: 5 5px;
  text-align: center;
  border-radius: 5px;
  border: 2px solid #2c3e50;
  font-size: 22px;
  color: #2c3e50;
  margin-bottom: 10px;
  background-color: #ecf0f1;
}

#### ASCII art
## parent.html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
  <link rel="stylesheet"  type="text/css" href="{{url_for('.static', filename='style.css')}}">
    <title>Parent Template</title>
  </head>
  <body>
    <header>
      <h1 class="title">Create ASCII Art</h1>
    </header>
    
    <div class="container">
      {% block content %}
      {% endblock %}
    </div>

  </body>
</html>

## art.html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Create ASCII Art</title>
  </head>
  <body>
    {% extends "parent.html" %}
    {% block content %}

    {% if ascii['valid'] %}
      <h2> Converted Image </h2>
      <div id='ascii-art'>
        {% for line in ascii['img'] %}
          {{line}}<br>
        {% endfor %}
      </div>
    {% else %}
        <h2 class="urlMsg"> Invalid URL </h2>
        <h3 class="urlMsg">{{ ascii['img'] }}</h3>
    {% endif %}
    <a href="{{ url_for('home') }}">Home</a>
      
    {% endblock %}
  </body>
</html>

## input.html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Create ASCII Art</title>
  </head>
  <body>
    {% extends "parent.html" %}
    {% block content %}
    
    <h2> Enter the URL of an image </h2>
    <form action="{{ url_for('ascii') }}" method="POST">
      <input type="text" id="urlBox" name="url" value="Image URL" onfocus="this.value=''"><br>
      <input type="submit" id="urlButton" value="Create">
    </form>
    <details>
      <summary><strong>How do I get an image URL?</strong></summary>
      <p id="findImg">Right-click on an image. You should see a window pop up. The action you select depends on your browser. It should say something like "Copy image address" or "Copy image link". Select the action that appears in your browser and paste into the box below.</p>
    </details>
      
    {% endblock %}
  </body>
</html>

## lena image url
https://camo.githubusercontent.com/ec8cf13388b98a7133c6850afcf17ab4af5042802e0229c49f2242ea36d37090/68747470733a2f2f7261772e6769746875622e636f6d2f6d696b6f6c616c7973656e6b6f2f6c656e612f6d61737465722f6c656e612e706e67

## main.py
from flask import Flask, render_template, request
from ascii_art import create_ascii

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('input.html')

@app.route('/ascii', methods=['POST'])
def ascii():
  url = request.form['url']
  img = create_ascii(url)
  if type(img) == list:
    resp = {'valid': True, 'img': img}
  else:
    resp = {'valid': False, 'img': img}
  return render_template('art.html', ascii = resp)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3000, debug=True)
  
## Exercise
pyinstaller exercise1.py --paths='/home/codio/workspace/ex1'

## Docker
FROM continuumio/python:3.9
ADD . /project 
WORKDIR /project 
ENTRYPOINT ["python", "my_script.py"]

#pyi-makespec exercise3.py --name my_app --paths='code/coding_exercise_3' --onefile
pyi-makespec exercise3.py --name my_app --paths=code/coding_exercise3
cat my_app.spec


# WRITE YOUR CODE HERE
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

class Exercise4(App):
  def build(self):
    # define the window
    Window.clearcolor = '#34495e'
    Window.size = (500, 300)
    self.window = GridLayout(cols=3)
    #self.window.size_hint = (0.8, 0.95)
    self.window.pos_hint = {'center_x' : 0.5, 'center_y' : 0.5}

    # define the widgets
    self.label1 = Label(text='Hello',
                             font_size = 36,
                             bold = True,
                             color = '#ecf0f1')
    self.label2 = Label(text='from',
                             font_size = 36,
                             bold = True,
                             color = '#ecf0f1')
    self.label3 = Label(text='Kivy',
                             font_size = 36,
                             bold = True,
                             color = '#ecf0f1')
    

    # add widgets
    self.window.add_widget(self.label1)
    self.window.add_widget(self.label2)
    self.window.add_widget(self.label3)

    return self.window


if __name__ == "__main__":
  Exercise4().run()
  
pyinstaller exercise4.py --name hello -w

# WRITE YOUR CODE HERE

while True:
  text = input("Input Text: ")
  if text == 'q':
    print('Goodbye!')
    break
  print(f'length = {len(text)}')

conda activate exercise5
pyi-makespec exercise5.py --onefile
pyinstaller exercise5.spec
