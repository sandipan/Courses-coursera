class CelestialBody:
  def __init__(self, size, mass, composition, name):
    self.size = size
    self.mass = mass
    self.composition = composition
    self.name = name
    
# create the satellite class
class Satellite(CelestialBody):
  def __init__(self, size, mass, composition, name, host_planet):
    super().__init__(size, mass, composition, name)
    self.host_planet = host_planet

# create the planet class
class Planet(CelestialBody):
  def __init__(self, size, mass, composition, name, host_star):
    super().__init__(size, mass, composition, name)
    self.host_star = host_star
	

# parent class
class Book:
  def __init__(self, title, author, genre):
    self.title = title
    self.author = author
    self.genre = genre

# child class
class BlogPost(Book):
  def __init__(self, website, title, author, word_count, genre, page_views):
    super().__init__(title, author, genre)
    self.website = website
    self.word_count = word_count
    self.page_views = page_views

my_post = BlogPost("Vogue", "Hot Summer Trends", "Amy Gutierrez", 2319, "fashion", 2748)
print(my_post.website)
print(my_post.title)	
print(my_post.author)	
print(my_post.word_count)	
print(my_post.genre)	
print(my_post.page_views)	

'''
class Parent1:
  def identify(self):
    return "This method is called from Parent1"
    
class Parent2:
  def identify(self):
    return "This method is called from Parent2"
    
# declare child class here
class Child(Parent1, Parent2):
  def identify(self):
    return "This method is called from Child"
  def identify2(self):
    return Parent2.identify(self)
  
child_object = Child()
print(child_object.identify())
print(child_object.identify2())
'''

class Parent1:
  def identify(self):
    return "This method is called from Parent1"
    
class Parent2:
  def identify(self):
    return "This method is called from Parent2"
    
# declare child class here
class Child(Parent2, Parent1):
  def identify(self):
    return "This method is called from Child"
  
  def identify2(self):
    return super().identify()

child_object = Child()
print(child_object.identify())
print(child_object.identify2())
	
# DO NOT ALTER THIS CODE
import sys
strings = [l.split(",") for l in sys.argv[1].split("*")]
accounts = [[int(n) for n in s] for s in strings]

class Bank:
  def __init__(self, name, customers, accounts):
    self.name = name
    self.customers = customers
    self.accounts = accounts
    
  def branch_total(self, accounts):
    total = 0
    for account in accounts:
      total += account
    return total

# Write your code here
class RegionalBank(Bank):
  #def __init__(self, name, customers, accounts):
  #  super().__init__(name, customers, accounts)

  def regional_total(self):
    total = 0
    for account in self.accounts:
      total += self.branch_total(account)
    return total

accounts = [
              [10000, 13000, 22000],
              [30000, 7000, 19000],
              [15000, 23000, 31000]
           ]
my_bank = RegionalBank("Bank of America", 9, accounts)
print(my_bank.regional_total())

# parent classes
class Person:
  def __init__(self, name, address):
    self.name = name
    self.address = address
    
  def get_info(self):
    return f"{self.name} lives at {self.address}."
  
class CardHolder:
  def __init__(self, account_number):
    self.account_number = account_number
    self.balance = 0
    self.credit_limit = 5000
    
  def process_sale(self, price):
    self.balance += price
    
  def make_payment(self, amount):
    self.balance -= amount
    
# declare child class here
class PlatinumClient(Person, CardHolder):
  def __init__(self, name, address, account_number):
    Person.__init__(self, name, address)
    CardHolder.__init__(self, account_number)
    self.cash_back = 0.02
    self.rewards = 0

  def process_sale(self, price):
    super().process_sale(price)
    self.rewards += price*self.cash_back
    
platinum = PlatinumClient("Sarah", "101 Main Street", 123364)
print(platinum.process_sale(100))
print(platinum.rewards)
print(platinum.balance)
print(platinum.make_payment(50))
print(platinum.balance)	
print(platinum.get_info())




class Country:
  
  def __init__(self, name, capital, population, continent):
    self._name = name
    self._capital = capital
    self._population = population
    self._continent = continent

  @property
  def name(self):
    return self._name

  @property
  def capital(self):
    return self._capital

  @property
  def population(self):
    return self._population

  @property
  def continent(self):
    return self._continent

my_country = Country('France', 'Paris', 67081000, 'Europe')
print(my_country.name)
print(my_country.capital)
print(my_country.population)
print(my_country.continent)


class Artist:
  
  def __init__(self, name, medium, style, famous_artwork):
    self.__name = name
    self.__medium = medium
    self.__style = style
    self.__famous_artwork = famous_artwork


my_artist = Artist('Bill Watterson', 'ink and paper', 'cartoons', 'Calvin and Hobbes')
#print(my_artist.__name)
print(my_artist._Artist__name)
print(my_artist._Artist__medium)
print(my_artist._Artist__style)
print(my_artist._Artist__famous_artwork)



class BankAccount:
  def __init__(self):
    self._checking = 0
    self._savings = 0

  def get_checking(self):
    return self._checking

  def get_savings(self):
    return self._savings

  def set_checking(self, new_checking):
    self._checking = new_checking

  def set_savings(self, new_savings):
    self._savings = new_savings

my_account = BankAccount()
print(my_account.set_checking(523.48))
print(my_account.get_checking())	
print(my_account.set_savings(386.15))
print(my_account.get_savings())	



class Dancer:
  def __init__(self, name, nationality, style):
    self._name = name
    self._nationality = nationality
    self._style = style
    
  def get_name(self):
    return self._name
  
  def set_name(self, new_value):
    self._name = new_value
    
  def get_nationality(self):
    return self._nationality
  
  def set_nationality(self, new_value):
    self._nationality = new_value
    
  def get_style(self):
    return self._style
  
  def set_style(self, new_value):
    self._style = new_value
    
  name = property(get_name, set_name)
  nationality = property(get_nationality, set_nationality)
  style = property(get_style, set_style)
  
  
 class Cyclist:
  def __init__(self, name, nationality, nickname):
    self._name = name
    self._nationality = nationality
    self._nickname = nickname

  @property
  def name(self):
    return self._name

  @property
  def nationality(self):
    return self._nationality

  @property
  def nickname(self):
    return self._nickname

  @name.setter
  def name(self, new_name):
    self._name = new_name

  @nationality.setter
  def nationality(self, new_nationality):
    self._nationality = new_nationality

  @nickname.setter
  def nickname(self, new_nickname):
    self._nickname = new_nickname

my_cyclist = Cyclist("Greg LeMond", "American", "Le Montstre")
print(my_cyclist.name)	
print(my_cyclist.nationality)	
print(my_cyclist.nickname)	
my_cyclist.name = "Eddy Merckx"	
my_cyclist.nationality = "Belgian"	
my_cyclist.nickname = "The Cannibal"	
print(my_cyclist.name)	
print(my_cyclist.nationality)	
print(my_cyclist.nickname)	


import random

class Lottery:
  def shuffle(self):
    results = []
    for i in range(5):
      results.append(random.randint(1, 20))
    return results

class PowerBall(Lottery):
  def shuffle(self):
    results = []
    for i in range(6):
      results.append(random.randint(1, 99))
    return results
	
	
class Airplane:
  def __init__(self, first_class, business_class, coach):
    self.first_class, self.business_class, self.coach = first_class, business_class, coach
  def total(self):
    return self.first_class + self.business_class + self.coach

class Train:
  def __init__(self, car1, car2, car3, car4, car5):
    self.car1, self.car2, self.car3, self.car4, self.car5 = car1, car2, car3, car4, car5
  def total(self):
    return self.car1 + self.car2 + self.car3 + self.car4 + self.car5
  
def passengers(obj):
  print(f'There are {obj.total()} passengers on board.')

passengers(Airplane(20, 10, 5))
passengers(Train(20, 10, 5, 1, 2))

class Characters:
  def __init__(self, phrases):
    self.phrases = phrases
  def len(self):
    return sum([len(phrase) for phrase in self.phrases])
  def __lt__(self, other):
    return self.len() < other.len()
  def __gt__(self, other):
    return self.len() > other.len()
  def __eq__(self, other):
    return self.len() == other.len()

sample_phrases1 = ['cat in the hat', 'green eggs and ham', 'the lorax']
sample_phrases2 = ['the taming of the shrew', 'hamlet', 'othello']

c1 = Characters(sample_phrases1)
c2 = Characters(sample_phrases2)
print(c1 > c2) # prints 'True'
print(c1 < c2) # prints 'False'
print(c1 == c1) # prints 'True'


class Median:
  
  def median(self, arr):
    n = len(arr)
    arr = sorted(arr)
    return arr[n//2] if n % 2 == 1 else (arr[n//2-1] + arr[n//2]) / 2
  
  def calculate_median(self, x1, x2, x3=None, x4=None, x5=None):
    arr = [x1, x2]
    if x3 is not None:
      arr.append(x3)
    if x4 is not None:
      arr.append(x4)
    if x5 is not None:
      arr.append(x5)
    return self.median(arr)


m = Median()
print(m.calculate_median(3, 5, 1, 4, 2))
print(m.calculate_median(8, 6, 4, 2))
print(m.calculate_median(9, 3, 7))
print(m.calculate_median(5, 2))


source_file = '/home/codio/workspace/code/polymorphism/text_1_exercise5.txt'
answer_file = '/home/codio/workspace/code/polymorphism/answer_exercise5.txt'

class Substitute:
  def __init__(self, source_file, answer_file):
    self.source_file = source_file
    self.answer_file = answer_file
    self.words = None
    
  def string_to_list(self):
    '''Read text file, turn it into a
    2D list of words for each line'''
    words = []
    with open(self.source_file, 'r') as file_object:
      lines = file_object.read().split('\n')
      for line in lines:
        words.append(line.split())
    self.words = words
    
  def list_to_string(self):
    '''Convert 2D list back into a 
    string with newline characters'''
    lines = []
    for line in self.words:
      lines.append(' '.join(line))
    string = '\n'.join(lines)
    self.words = string
  
  def swap_words(self):
    self.string_to_list()
    for line in self.words:
      for i in range(len(line)):
        if (i + 1) % 5 == 0:
          word = line[i]
          line[i] = 'HELLO'
    self.list_to_string()

class Stars(Substitute):
  def swap_words(self):
    self.string_to_list()
    for line in self.words:
      for i in range(len(line)):
        if (i + 1) % 3 == 0:
          word = line[i]
          line[i] = '*'*len(word)
    self.list_to_string()

#s = Substitute(source_file, answer_file)
s = Stars(source_file, answer_file)
s.swap_words()
print(s.words)


source_file = '/home/codio/workspace/code/polymorphism/text_1_exercise5.txt'
answer_file = '/home/codio/workspace/code/polymorphism/answer_exercise5.txt'

class Substitute:
  def __init__(self, source_file, answer_file):
    self.source_file = source_file
    self.answer_file = answer_file
    self.words = None
    
  def string_to_list(self):
    '''Read text file, turn it into a
    2D list of words for each line'''
    words = []
    with open(self.source_file, 'r') as file_object:
      lines = file_object.read().split('\n')
      for line in lines:
        words.append(line.split())
    self.words = words
    
  def list_to_string(self):
    '''Convert 2D list back into a 
    string with newline characters'''
    lines = []
    for line in self.words:
      lines.append(' '.join(line))
    string = '\n'.join(lines)
    self.words = string
  
  def swap_words(self):
    self.string_to_list()
    for line in self.words:
      for i in range(len(line)):
        if (i + 1) % 5 == 0:
          word = line[i]
          line[i] = 'HELLO'
    self.list_to_string()

class Stars(Substitute):
  def swap_words(self):
    self.string_to_list()
    for line in self.words:
      for i in range(len(line)):
        if (i + 1) % 3 == 0:
          word = line[i]
          line[i] = '*'*len(word)
    self.list_to_string()

#s = Substitute(source_file, answer_file)
s = Stars(source_file, answer_file)
s.swap_words()
print(s.words)


import tech

my_phone = tech.Phone("Pixel 5", "sage", 128)
my_laptop = tech.Laptop("MacBook Pro", 15, 256)

print(my_phone)
print(my_laptop)


class Band:
  def __init__(self, name, genre, members):
    self.name = name
    self.genre = genre
    self.members = members
    
  def __str__(self):
    return f'{self.name} is a {self.genre} band.'
  
  def __repr__(self):
    return f'Band({self.name}, {self.genre}, {self.members})'
	
class Library:
  def __init__(self):
    self.books = []
    self.fiction = []
    self.nonfiction = []
    
  def add_book(self, book):
    '''Takes a Book object and adds it to self.books'''
    self.books.append(book)
    
  def search_title(self, title):
    '''Takes a string and returns a Boolean'''
    has_book = False
    for book in self.books:
      if title.lower() == book.title.lower():
        has_book = True
    return has_book
  
  def search_author(self, author):
    '''Takes a string and returns a list of Book objects'''
    author_books = []
    for book in self.books:
      if book.author.lower() == author.lower():
        author_books.append(book)
    return author_books
    
  def sort_books(self):
    '''Helper method for sort_fiction and sort_nonfiction'''
    self.fiction = self.sort_fiction()
    self.nonfiction = self.sort_nonfiction()
    
  def sort_fiction(self):
    '''Return list of Book objects where the genre is fiction'''
    fiction_books = []
    for book in self.books:
      if book.genre.lower() == 'fiction':
        fiction_books.append(book)
    return fiction_books
    
  def sort_nonfiction(self):
    '''Return list of Book objects where the genre is nonfiction'''
    nonfiction_books = []
    for book in self.books:
      if book.genre.lower() == 'nonfiction':
        nonfiction_books.append(book)
    return nonfiction_books
	
class Book:
  def __init__(self, title, author, genre):
    self.title, self.author, self.genre = title, author, genre
  def __repr__(self):
    return f'Book({self.title}, {self.author}, {self.genre})'
	
from library import Library
from book import Book

library = Library()
book1 = Book('Three Musketeers', 'Alexandre Dumas', 'fiction')
book2 = Book('The Count of Monte Cristo', 'Alexandre Dumas', 'fiction')
book3 = Book('Educated', 'Tara Westover', 'nonfiction')

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)
library.sort_books()

print(library.books)	
print(library.fiction)	
print(library.nonfiction)	
print(library.search_author('Alexandre Dumas'))
print(library.search_author('Herman Melville'))
print(library.search_title('Educated'))	
print(library.search_title('Moby Dick'))	


class Item:

  def __init__(self, name, price, quantity):
    self.name, self.price, self.quantity, self.subtotal = name, price, quantity, 0

  def calculate_subtotal(self):
    self.subtotal = self.quantity * self.price

  def get_subtotal(self):
    return self.subtotal
  
  def __repr__(self):
    return f'Item({self.name}, {self.price}, {self.quantity}, {self.subtotal})'



class ShoppingCart:
  
  def __init__(self):
    self.items = []
    self.total = 0

  def add_item(self, item):
    self.items.append(item)
    self.calulate_total()
  
  def calulate_total(self):
    self.total = 0
    for item in self.items:
      item.calculate_subtotal()
      self.total += item.get_subtotal()

  def get_total(self):
    return self.total

  def get_num_items(self):
    return len(self.items)

  def get_items(self):
    return self.items

  def __str__(self):
    return f'The cart has {self.get_num_items()} items for a total of ${self.get_total()}'

from item import Item
from shopping_cart import ShoppingCart

item1 = Item('milk', 1.5, 1)
item2 = Item('apple', 5, 0.75)
item3 = Item('bread', 2, 2.25)
cart = ShoppingCart()

cart.add_item(item1)
cart.add_item(item2)
cart.add_item(item3)

print(cart.get_total())
print(cart.get_num_items())
print(cart)
print(cart.get_items())
