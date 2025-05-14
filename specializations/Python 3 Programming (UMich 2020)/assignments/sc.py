def test():
	stopwords = ['to', 'a', 'for', 'by', 'an', 'am', 'the', 'so', 'it', 'and', 'The']
	#sent = "height and ewok wonder"  
	sent = "The water earth and air are vital"
	acro = ''
	for w in sent.split(' '):
		if not w in stopwords:
			acro += w[0:2].upper() + '.'
	acro = acro[:-1]
	print(acro)

def sentiment_analysis():
	def strip_punctuation(x):
		for c in punctuation_chars:
			x = x.replace(c, '')
		return x
				
	def get_pos(x):
		return len(filter(lambda x: (strip_punctuation(x) in positive_words), x.lower().split()))

	def get_neg(x):
		return len(filter(lambda x: (strip_punctuation(x) in negative_words), x.lower().split()))

	punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
	# lists of words to use
	positive_words = []
	with open("positive_words.txt") as pos_f:
		for lin in pos_f:
			if lin[0] != ';' and lin[0] != '\n':
				positive_words.append(lin.strip())


	negative_words = []
	with open("negative_words.txt") as pos_f:
		for lin in pos_f:
			if lin[0] != ';' and lin[0] != '\n':
				negative_words.append(lin.strip())

	tweets = open('project_twitter_data.csv').read().splitlines()
	out = open('resulting_data.csv', 'w')
	out.write('Number of Retweets, Number of Replies, Positive Score, Negative Score, Net Score\n')
	for i in range(1, len(tweets)):
		tweet_text, retweet_count, reply_count = tweets[i].split(',')
		pos_score, neg_score = get_pos(tweet_text), get_neg(tweet_text)
		net_score = pos_score - neg_score
		out.write('{}, {}, {}, {}, {}\n'.format(retweet_count, reply_count, pos_score, neg_score, net_score))
	out.close()

def visualize():	
	import pandas as pd
	import matplotlib.pylab as plt

	df = pd.read_csv('resulting_data.csv')
	print(df.head(20))
	print(df.columns)

	df.plot.scatter(x=' Net Score', y='Number of Retweets', c=' Net Score', cmap='RdYlGn', s=50)
	plt.grid()
	plt.title('Number of Retweets vs. Net Sentiment Score for Tweets', size=20)
	plt.show()
	
import json
import random
import time

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Repeatedly asks the user for a number between min & max (inclusive)
def getNumberBetween(prompt, min, max):
    userinp = input(prompt) # ask the first time

    while True:
        try:
            n = int(userinp) # try casting to an integer
            if n < min:
                errmessage = 'Must be at least {}'.format(min)
            elif n > max:
                errmessage = 'Must be at most {}'.format(max)
            else:
                return n
        except ValueError: # The user didn't enter a number
            errmessage = '{} is not a number.'.format(userinp)

        # If we haven't gotten a number yet, add the error message
        # and ask again
        userinp = input('{}\n{}'.format(errmessage, prompt))

# Spins the wheel of fortune wheel to give a random prize
# Examples:
#    { "type": "cash", "text": "$950", "value": 950, "prize": "A trip to Ann Arbor!" },
#    { "type": "bankrupt", "text": "Bankrupt", "prize": false },
#    { "type": "loseturn", "text": "Lose a turn", "prize": false }
def spinWheel():
    with open("wheel.json", 'r') as f:
        wheel = json.loads(f.read())
        return random.choice(wheel)

# Returns a category & phrase (as a tuple) to guess
# Example:
#     ("Artist & Song", "Whitney Houston's I Will Always Love You")
def getRandomCategoryAndPhrase():
    with open("phrases.json", 'r') as f:
        phrases = json.loads(f.read())

        category = random.choice(list(phrases.keys()))
        phrase   = random.choice(phrases[category])
        return (category, phrase.upper())

# Given a phrase and a list of guessed letters, returns an obscured version
# Example:
#     guessed: ['L', 'B', 'E', 'R', 'N', 'P', 'K', 'X', 'Z']
#     phrase:  "GLACIER NATIONAL PARK"
#     returns> "_L___ER N____N_L P_RK"
def obscurePhrase(phrase, guessed):
    rv = ''
    for s in phrase:
        if (s in LETTERS) and (s not in guessed):
            rv = rv+'_'
        else:
            rv = rv+s
    return rv

# Returns a string representing the current state of the game
def showBoard(category, obscuredPhrase, guessed):
    return """
Category: {}
Phrase:   {}
Guessed:  {}""".format(category, obscuredPhrase, ', '.join(sorted(guessed)))

category, phrase = getRandomCategoryAndPhrase()

guessed = []
for x in range(random.randint(10, 20)):
    randomLetter = random.choice(LETTERS)
    if randomLetter not in guessed:
        guessed.append(randomLetter)

print("getRandomCategoryAndPhrase()\n -> ('{}', '{}')".format(category, phrase))

print("\n{}\n".format("-"*5))

print("obscurePhrase('{}', [{}])\n -> {}".format(phrase, ', '.join(["'{}'".format(c) for c in guessed]), obscurePhrase(phrase, guessed)))

print("\n{}\n".format("-"*5))

obscured_phrase = obscurePhrase(phrase, guessed)
print("showBoard('{}', '{}', [{}])\n -> {}".format(phrase, obscured_phrase, ','.join(["'{}'".format(c) for c in guessed]), showBoard(phrase, obscured_phrase, guessed)))

print("\n{}\n".format("-"*5))

num_times_to_spin = random.randint(2, 5)
print('Spinning the wheel {} times (normally this would just be done once per turn)'.format(num_times_to_spin))

for x in range(num_times_to_spin):
    print("\n{}\n".format("-"*2))
    print("spinWheel()")
    print(spinWheel())


print("\n{}\n".format("-"*5))

print("In 2 seconds, will run getNumberBetween('Testing getNumberBetween(). Enter a number between 1 and 10', 1, 10)")

time.sleep(2)

print(getNumberBetween('Testing getNumberBetween(). Enter a number between 1 and 10', 1, 10))

VOWEL_COST = 250
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VOWELS = 'AEIOU'

'''
Part A: WOFPlayer

We’re going to start by defining a class to represent a Wheel of Fortune player, called WOFPlayer. Every instance of WOFPlayer has three instance variables:

.name: The name of the player (should be passed into the constructor)

.prizeMoney: The amount of prize money for this player (an integer, initialized to 0)

.prizes: The prizes this player has won so far (a list, initialized to [])

Of these instance variables, only name should be passed into the constructor.

It should also have the following methods (note: we will exclude self in our descriptions):

.addMoney(amt): Add amt to self.prizeMoney

.goBankrupt(): Set self.prizeMoney to 0

.addPrize(prize): Append prize to self.prizes

.__str__(): Returns the player’s name and prize money in the following format:
Steve ($1800) (for a player with instance variables .name == 'Steve' and prizeMoney == 1800)
'''

# Write the WOFPlayer class definition (part A) here
class WOFPlayer:
	def __init__(self, name):
		self.name = name
		self.prizeMoney = 0
		self.prizes = []
		
	def addMoney(self, amt):
		self.prizeMoney += amt
		
	def goBankrupt(self):
		self.prizeMoney = 0
		
	def addPrize(self, prize):
		self.prizes.append(prize)
		
	def __str__(self):
		return '{} (${})'.format(self.name, self.prizeMoney)
		
'''
Part B: WOFHumanPlayer

Next, we’re going to define a class named WOFHumanPlayer, which should inherit from WOFPlayer (part A). This class is going to represent a human player. In addition to having all of the instance variables and methods that WOFPlayer has, WOFHumanPlayer should have an additional method:

.getMove(category, obscuredPhrase, guessed): Should ask the user to enter a move (using input()) and return whatever string they entered.

.getMove()’s prompt should be:

{name} has ${prizeMoney}

Category: {category}
Phrase:  {obscured_phrase}
Guessed: {guessed}

Guess a letter, phrase, or type 'exit' or 'pass':
'''		
# Write the WOFHumanPlayer class definition (part B) here
class WOFHumanPlayer(WOFPlayer):
	def getMove(self, category, obscuredPhrase, guessed):
		print('{} has ${}'.format(self.name, self.prizeMoney))
		print('Category: {}'.format(category))
		print('Phrase: {}'.format(obscuredPhrase))
		print('Guessed: {}'.format(guessed))
		return input("Guess a letter, phrase, or type 'exit' or 'pass':")

'''
Part C: WOFComputerPlayer

Finally, we’re going to define a class named WOFComputerPlayer, which should inherit from WOFPlayer (part A). This class is going to represent a computer player.
Every computer player will have a difficulty instance variable. Players with a higher difficulty generally play “better”. There are many ways to implement this. We’ll do the following:
If there aren’t any possible letters to choose (for example: if the last character is a vowel but this player doesn’t have enough to guess a vowel), we’ll 'pass'
Otherwise, semi-randomly decide whether to make a “good” move or a “bad” move on a given turn (a higher difficulty should make it more likely for the player to make a “good” move)
To make a “bad” move, we’ll randomly decide on a possible letter.
To make a “good” move, we’ll choose a letter according to their overall frequency in the English language.
In addition to having all of the instance variables and methods that WOFPlayer has, WOFComputerPlayer should have:

Class variable

.SORTED_FREQUENCIES: Should be set to 'ZQXJKVBPYGFWMUCLDRHSNIOATE', which is a list of English characters sorted from least frequent ('Z') to most frequent ('E'). We’ll use this when trying to make a “good” move.

Additional Instance variable

.difficulty: The level of difficulty for this computer (should be passed as the second argument into the constructor after .name)

Methods

.smartCoinFlip(): This method will help us decide semi-randomly whether to make a “good” or “bad” move. A higher difficulty should make us more likely to make a “good” move. Implement this by choosing a random number between 1 and 10 using random.randint(1, 10) (see above) and returning True if that random number is greater than self.difficulty. If the random number is less than or equal to self.difficulty, return False.

.getPossibleLetters(guessed): This method should return a list of letters that can be guessed.
These should be characters that are in LETTERS ('ABCDEFGHIJKLMNOPQRSTUVWXYZ') but not in the guessed parameter.
Additionally, if this player doesn’t have enough prize money to guess a vowel (variable VOWEL_COST set to 250), then vowels (variable VOWELS set to 'AEIOU') should not be included

.getMove(category, obscuredPhrase, guessed): Should return a valid move.
Use the .getPossibleLetters(guessed) method described above.

If there aren’t any letters that can be guessed (this can happen if the only letters left to guess are vowels and the player doesn’t have enough for vowels), return 'pass'

Use the .smartCoinFlip() method to decide whether to make a “good” or a “bad” move
If making a “good” move (.smartCoinFlip() returns True), then return the most frequent (highest index in .SORTED_FREQUENCIES) possible character

If making a “bad” move (.smartCoinFlip() returns False), then return a random character from the set of possible characters (use random.choice())
'''
# Write the WOFComputerPlayer class definition (part C) here
class WOFComputerPlayer(WOFPlayer):
	SORTED_FREQUENCIES = 'ZQXJKVBPYGFWMUCLDRHSNIOATE'
	
	def __init__(self, name, difficulty):
		super().__init__(name)
		self.difficulty = difficulty
		
	def smartCoinFlip(self):
		return random.randint(1, 10) > self.difficulty		
		
	def getPossibleLetters(self, guessed): 
		possible_letters = set(self.SORTED_FREQUENCIES) - set(guessed)
		if self.prizeMoney < VOWEL_COST:
			possible_letters -= set(VOWELS)
		return list(possible_letters)
		
	def getMove(self, category, obscuredPhrase, guessed):
		available_letters = self.getPossibleLetters(guessed)
		if len(available_letters) == 0:
			return 'pass'
		if self.smartCoinFlip():
			return sorted(available_letters, key=WOFComputerPlayer.SORTED_FREQUENCIES.index, reverse=True)[0]
		return random.choice(available_letters)

def play_game():
	import sys
	sys.setExecutionLimit(600000) # let this take up to 10 minutes

	import json
	import random
	import time

	LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	VOWELS  = 'AEIOU'
	VOWEL_COST  = 250

	# Repeatedly asks the user for a number between min & max (inclusive)
	def getNumberBetween(prompt, min, max):
		userinp = input(prompt) # ask the first time

		while True:
			try:
				n = int(userinp) # try casting to an integer
				if n < min:
					errmessage = 'Must be at least {}'.format(min)
				elif n > max:
					errmessage = 'Must be at most {}'.format(max)
				else:
					return n
			except ValueError: # The user didn't enter a number
				errmessage = '{} is not a number.'.format(userinp)

			# If we haven't gotten a number yet, add the error message
			# and ask again
			userinp = input('{}\n{}'.format(errmessage, prompt))

	# Spins the wheel of fortune wheel to give a random prize
	# Examples:
	#    { "type": "cash", "text": "$950", "value": 950, "prize": "A trip to Ann Arbor!" },
	#    { "type": "bankrupt", "text": "Bankrupt", "prize": false },
	#    { "type": "loseturn", "text": "Lose a turn", "prize": false }
	def spinWheel():
		with open("wheel.json", 'r') as f:
			wheel = json.loads(f.read())
			return random.choice(wheel)

	# Returns a category & phrase (as a tuple) to guess
	# Example:
	#     ("Artist & Song", "Whitney Houston's I Will Always Love You")
	def getRandomCategoryAndPhrase():
		with open("phrases.json", 'r') as f:
			phrases = json.loads(f.read())

			category = random.choice(list(phrases.keys()))
			phrase   = random.choice(phrases[category])
			return (category, phrase.upper())

	# Given a phrase and a list of guessed letters, returns an obscured version
	# Example:
	#     guessed: ['L', 'B', 'E', 'R', 'N', 'P', 'K', 'X', 'Z']
	#     phrase:  "GLACIER NATIONAL PARK"
	#     returns> "_L___ER N____N_L P_RK"
	def obscurePhrase(phrase, guessed):
		rv = ''
		for s in phrase:
			if (s in LETTERS) and (s not in guessed):
				rv = rv+'_'
			else:
				rv = rv+s
		return rv

	# Returns a string representing the current state of the game
	def showBoard(category, obscuredPhrase, guessed):
		return """
	Category: {}
	Phrase:   {}
	Guessed:  {}""".format(category, obscuredPhrase, ', '.join(sorted(guessed)))

	# GAME LOGIC CODE
	print('='*15)
	print('WHEEL OF PYTHON')
	print('='*15)
	print('')

	num_human = getNumberBetween('How many human players?', 0, 10)

	# Create the human player instances
	human_players = [WOFHumanPlayer(input('Enter the name for human player #{}'.format(i+1))) for i in range(num_human)]

	num_computer = getNumberBetween('How many computer players?', 0, 10)

	# If there are computer players, ask how difficult they should be
	if num_computer >= 1:
		difficulty = getNumberBetween('What difficulty for the computers? (1-10)', 1, 10)

	# Create the computer player instances
	computer_players = [WOFComputerPlayer('Computer {}'.format(i+1), difficulty) for i in range(num_computer)]

	players = human_players + computer_players

	# No players, no game :(
	if len(players) == 0:
		print('We need players to play!')
		raise Exception('Not enough players')

	# category and phrase are strings.
	category, phrase = getRandomCategoryAndPhrase()
	# guessed is a list of the letters that have been guessed
	guessed = []

	# playerIndex keeps track of the index (0 to len(players)-1) of the player whose turn it is
	playerIndex = 0

	# will be set to the player instance when/if someone wins
	winner = False

	def requestPlayerMove(player, category, guessed):
		while True: # we're going to keep asking the player for a move until they give a valid one
			time.sleep(0.1) # added so that any feedback is printed out before the next prompt

			move = player.getMove(category, obscurePhrase(phrase, guessed), guessed)
			move = move.upper() # convert whatever the player entered to UPPERCASE
			if move == 'EXIT' or move == 'PASS':
				return move
			elif len(move) == 1: # they guessed a character
				if move not in LETTERS: # the user entered an invalid letter (such as @, #, or $)
					print('Guesses should be letters. Try again.')
					continue
				elif move in guessed: # this letter has already been guessed
					print('{} has already been guessed. Try again.'.format(move))
					continue
				elif move in VOWELS and player.prizeMoney < VOWEL_COST: # if it's a vowel, we need to be sure the player has enough
						print('Need ${} to guess a vowel. Try again.'.format(VOWEL_COST))
						continue
				else:
					return move
			else: # they guessed the phrase
				return move


	while True:
		player = players[playerIndex]
		wheelPrize = spinWheel()

		print('')
		print('-'*15)
		print(showBoard(category, obscurePhrase(phrase, guessed), guessed))
		print('')
		print('{} spins...'.format(player.name))
		time.sleep(2) # pause for dramatic effect!
		print('{}!'.format(wheelPrize['text']))
		time.sleep(1) # pause again for more dramatic effect!

		if wheelPrize['type'] == 'bankrupt':
			player.goBankrupt()
		elif wheelPrize['type'] == 'loseturn':
			pass # do nothing; just move on to the next player
		elif wheelPrize['type'] == 'cash':
			move = requestPlayerMove(player, category, guessed)
			if move == 'EXIT': # leave the game
				print('Until next time!')
				break
			elif move == 'PASS': # will just move on to next player
				print('{} passes'.format(player.name))
			elif len(move) == 1: # they guessed a letter
				guessed.append(move)

				print('{} guesses "{}"'.format(player.name, move))

				if move in VOWELS:
					player.prizeMoney -= VOWEL_COST

				count = phrase.count(move) # returns an integer with how many times this letter appears
				if count > 0:
					if count == 1:
						print("There is one {}".format(move))
					else:
						print("There are {} {}'s".format(count, move))

					# Give them the money and the prizes
					player.addMoney(count * wheelPrize['value'])
					if wheelPrize['prize']:
						player.addPrize(wheelPrize['prize'])

					# all of the letters have been guessed
					if obscurePhrase(phrase, guessed) == phrase:
						winner = player
						break

					continue # this player gets to go again

				elif count == 0:
					print("There is no {}".format(move))
			else: # they guessed the whole phrase
				if move == phrase: # they guessed the full phrase correctly
					winner = player

					# Give them the money and the prizes
					player.addMoney(wheelPrize['value'])
					if wheelPrize['prize']:
						player.addPrize(wheelPrize['prize'])

					break
				else:
					print('{} was not the phrase'.format(move))

		# Move on to the next player (or go back to player[0] if we reached the end)
		playerIndex = (playerIndex + 1) % len(players)

	if winner:
		# In your head, you should hear this as being announced by a game show host
		print('{} wins! The phrase was {}'.format(winner.name, phrase))
		print('{} won ${}'.format(winner.name, winner.prizeMoney))
		if len(winner.prizes) > 0:
			print('{} also won:'.format(winner.name))
			for prize in winner.prizes:
				print('    - {}'.format(prize))
	else:
		print('Nobody won. The phrase was {}'.format(phrase))

def movie_rec_rest_api():
	import requests_with_caching, json

	def get_movies_from_tastedive(name):
		res = requests_with_caching.get('https://tastedive.com/api/similar',
										 params={'q': name, 'type':'movies', 'limit':5})
		#print(res)
		return res.json() #text #json

	def extract_movie_titles(res):
		return [x['Name'] for x in res['Similar']['Results']]

	def get_related_titles(lst):
		titles = set([])
		for mov in lst:
			titles |= set(extract_movie_titles(get_movies_from_tastedive(mov)))
		return list(titles)
		
	def get_movie_data(name):
		res = requests_with_caching.get('http://www.omdbapi.com/',
										 params={'t': name, 'r':'json'})
		#print(res)
		return res.json() #text #json

	def get_movie_rating(res):
		for x in res['Ratings']:
			if x['Source'] == 'Rotten Tomatoes':
				return int(x['Value'][:-1])
		return 0

	def get_sorted_recommendations(titles):
		rel_titles = get_related_titles(titles)
		return sorted(rel_titles, key=lambda x: (get_movie_rating(get_movie_data(x)), x), reverse=True)

	# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
	get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

def pil_test():
	import PIL
	from PIL import Image, ImageDraw, ImageFont
	from PIL import ImageEnhance
	import numpy as np

	# read image and convert to RGB
	image=Image.open("readonly/msi_recruitment.gif")
	image=image.convert('RGB')

	# Split into 3 channels
	r, g, b = image.split()
	fracs = [0.1, 0.5, 0.9]
	images = []
	j = 0
	for i in range(9):
		if i < 3:
			r1 = r.point(lambda x: x * fracs[j])
			g1, b1 = g, b
		elif i < 6:
			g1 = g.point(lambda x: x * fracs[j])
			r1, b1 = r, b
		else:
			b1 = b.point(lambda x: x * fracs[j])
			r1, g1 = r, g
		j = (j + 1) % 3
		# Recombine back to RGB image
		result = Image.merge('RGB', (r1, g1, b1))
		images.append(result)

	# create a contact sheet from different brightnesses
	first_image = images[0]
	gap = 60
	contact_sheet = PIL.Image.new(first_image.mode, (first_image.width*3,first_image.height*3+gap*3))
	x, y = 0, 0
	draw = ImageDraw.Draw(contact_sheet)  
	font = ImageFont.truetype(r'readonly/fanwood-webfont.ttf', 75)  

	j = 0
	for img in images:
		# Lets paste the current image into the contact sheet
		contact_sheet.paste(img, (x, y) )
		text = 'channel {} intensity {}'.format(j // 3, fracs[j % 3])
		imga = np.array(img)
		color = int(np.mean(imga[...,0])), int(np.mean(imga[...,1])), int(np.mean(imga[...,2]))
		# drawing text size 
		draw.text((x, y+img.size[1]), text, font = font, align ="left", fill=color)  

		# Now we update our X position. If it is going to be the width of the image, then we set it to 0
		# and update Y as well to point to the next "line" of the contact sheet.
		if x+first_image.width == contact_sheet.width:
			x=0
			y=y+first_image.height+gap
		else:
			x=x+first_image.width
		j += 1

	# resize and display the contact sheet
	contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
	display(contact_sheet)

def im_face_text():
	import zipfile

	from PIL import Image
	import pytesseract
	import cv2 as cv
	import numpy as np

	# the rest is up to you!
	
	# loading the face detection classifier
	def pre_process(im_zipfile):
		face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
		image_info = []
		with zipfile.ZipFile(im_zipfile) as imzip:    
			for f in imzip.infolist():
				face_txt_dict = {}
				print('Processing {}'.format(f.filename))
				im = Image.open(imzip.open(f))
				#display(im)
				gray = cv.cvtColor(np.array(im), cv.COLOR_RGB2GRAY)
				faces = face_cascade.detectMultiScale(gray).tolist()
				im_faces = []
				for x,y,w,h in faces:
					im_faces.append(im.crop((x, y, x+w, y+h)))     
				face_txt_dict['filename'] = f.filename
				face_txt_dict['mode'] = im.mode
				face_txt_dict['faces'] = im_faces
				face_txt_dict['txt'] = pytesseract.image_to_string(im)
				image_info.append(face_txt_dict)
		return image_info
		
	def search(text, image_info):
		size = 128, 128
		for i in image_info:
			if text in i['txt']:
				print('Results found in file {}'.format(i['filename']))
				if len(i['faces']) == 0:
					print('But there were no faces in that file!')
				else:
					contact_sheet=Image.new(i['mode'], (128*(len(i['faces'])//5+1),128*5))
					x, y = 0, 0
					for im in i['faces']:
						# Lets paste the current image into the contact sheet
						contact_sheet.paste(im.thumbnail(size), (x, y) )
						# Now we update our X position. If it is going to be the width of the image, then we set it to 0
						# and update Y as well to point to the next "line" of the contact sheet.
						if x + 128 == contact_sheet.width:
							x, y = 0, y + 128
						else:
							x = x + 128
					display(contact_sheet)
					
	im_info = pre_process('readonly/small_img.zip')
	search('Christopher', im_info)