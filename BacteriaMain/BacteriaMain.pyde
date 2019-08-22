import string, random, math, names
import User, Bacteria, Bacterium

debug = False
drawn = False
drawCount = 0
sizeBuffer = 50
drawLabelEnabled = False

currentUser = None
currentBacteria = None

# ---Modes---

# INSTANCE
# Instance will draw a single frame from given inputs

# SERIES
# Series will draw a series of frames, for the value of drawFor

# LIFE
# Life will draw the lifetime of given inputs by going through levels starting at input

# Probably would have implemented more modes but these are the ones that are mainly important

modeList = {
	"instance": lambda: instance(),
	"series": lambda: series(),
	"life": lambda: life()
}

# Customisable variables
mode = "life"
# How many draw loops (doesn't work for life)
drawFor = 20
drawTimer = 0.5
doSaveFrame = False
doSaveFrameEvery = 1

# Empty fields will generate randomly
# Fill fields to pass args
firstName = ""
lastName = ""
email = ""
password = ""
level = 1

def setup():
	size(800, 800)


def draw():
	global drawn, drawCount, drawFor, drawTimer, modeList, currentUser
	global doSaveFrame, doSaveFrameEvery
	noFill()
	noStroke()
	if(frameCount % (drawTimer * 60) == 0) and not drawn:
		try:
			modeList[mode.lower()]()
		except Exception as e:
			print("IMPROPER MODE:", e)
			noLoop()
		if frameCount % doSaveFrameEvery == 0 and doSaveFrame and currentUser != None:
			saveName = (
				str(currentUser.firstName[0])+
				str(currentUser.lastName)+
				"LVL"+str(currentUser.level)+
				"FRAME"+str(frameCount)+
				".png"
			)
			saveFrame(saveName)


def series():
	global drawLabelEnabled, sizeBuffer, drawn, drawCount, drawFor
	global currentUser, currentBacteria
	global firstName, lastName, email, password, level

	if not drawCount <= drawFor-1:
		noLoop()
		return
	currentUser = User.User(
		firstName=firstName,
		lastName=lastName,
		email=email,
		password=password,
		level=level
	)
	seeds = drawDish(currentUser, sizeBuffer)
	currentBacteria = Bacteria.Bacteria(currentUser, sizeBuffer, seeds, debug)
	generatedLevel = currentUser.level
	currentBacteria.drawMetaball = False
	for x in range(generatedLevel):
		if x == generatedLevel-1:
			currentBacteria.drawMetaball = True
		currentBacteria.level = x
		currentBacteria.walk()
		currentBacteria.checkCollisions()
	currentBacteria.drawBacteria()
	if drawLabelEnabled:
		currentLabel = drawLabel(currentUser)
	drawCount += 1


def instance():
	global drawLabelEnabled, sizeBuffer, drawn
	global firstName, lastName, email, password, level
	global currentUser, currentBacteria

	if currentUser != None:
		noLoop()
		return
	currentUser = User.User(
		firstName=firstName,
		lastName=lastName,
		email=email,
		password=password,
		level=level
	)
	seeds = drawDish(currentUser, sizeBuffer)
	currentBacteria = Bacteria.Bacteria(currentUser, sizeBuffer, seeds, debug)
	generatedLevel = currentUser.level
	currentBacteria.drawMetaball = False
	for x in range(generatedLevel):
		if x == generatedLevel-1:
			currentBacteria.drawMetaball = True
		currentBacteria.level = x
		currentBacteria.walk()
		currentBacteria.checkCollisions()
	currentBacteria.drawBacteria()
	if drawLabelEnabled:
		currentLabel = drawLabel(currentUser)
	drawn = True


def life():
	global drawLabelEnabled, sizeBuffer, drawn, drawCount, drawFor
	global firstName, lastName, email, password, level
	global currentUser, currentBacteria
	if drawCount <= drawFor-1:
		if currentUser == None:
			currentUser = User.User(
				firstName=firstName,
				lastName=lastName,
				email=email,
				password=password,
				level=level
			)
		seeds = drawDish(currentUser, sizeBuffer)
		if currentBacteria == None:
			currentBacteria = Bacteria.Bacteria(currentUser, sizeBuffer, seeds, debug)
		currentBacteria.walk()
		currentBacteria.checkCollisions()
		currentBacteria.drawBacteria()
		if drawLabelEnabled:
			currentLabel = drawLabel(currentUser)
		currentUser.level += 1
		drawCount += 1
	else:
		noLoop()
		return


# Generates dish colors and seed
def drawDish(currentUser, sizeBuffer):
	dishHeight = height - sizeBuffer
	dishWidth = width - sizeBuffer
	firstName = currentUser.firstName
	lastName = currentUser.lastName
	password = currentUser.password

	seed = []
	exponent = 5

	# Return integer value (index) of passed character
	findIndex = lambda char: string.printable.index(char)

	inputList = [
		[firstName, 0],
		[lastName, 0],
		[password, 0]
	]

	# For each input, get sum value of all characters + their positions in input
	for x in range(len(inputList)):
		word = inputList[x][0]
		for y in range(len(word)):
			character = word[y]
			inputList[x][1] += findIndex(character) + y
			if not character.isnumeric():
				inputList[x][1] += character.isupper()

	firstNameVal = inputList[0][1]
	lastNameVal = inputList[1][1]
	passwordVal = inputList[2][1]

	# Convert exponentiated number to hex, take last 6 characters and turn
	# into hex color for dish

	exponentiate = lambda value: ((value+1)**5)
	hexify = lambda value: "#" + str(hex(value%16777215))[-6:].upper()
	colorList = []

	for value in (firstNameVal, lastNameVal, passwordVal):
		exponentiated = exponentiate(value)
		colorList += [hexify(exponentiate(value))]
		seed += [exponentiated]

	dishBorderThickness = (
		len(firstName) + len(lastName) + len(password)
	) / 2.5

	backgroundColor, dishColor, dishBorderColor = colorList

	# Draws dish based on inputs
	pushMatrix()
	fill(backgroundColor)
	rect(0, 0, width, height)
	stroke(dishBorderColor)
	strokeWeight(dishBorderThickness)
	fill(dishColor)
	translate(width / 2, height / 2)
	ellipse(0, 0, dishWidth, dishHeight)
	popMatrix()

	return seed


# Draws label displaying all user info
def drawLabel(currentUser):

	labelList = (
		("First Name: ", currentUser.firstName),
		("Last Name: ", currentUser.lastName),
		("Email: ", currentUser.email),
		("Password: ", currentUser.password),
		("Level: ", str(currentUser.level))
	)

	pushMatrix()
	translate(width / 2 + 50, height / 2 + 270)
	colorMode(RGB)
	noStroke()
	fill(255, 255, 255, 255 / 1.3)
	rect(0, 0, 340, 120)
	fill(0)

	for x in range(len(labelList)):
		text(labelList[x][0] + labelList[x][1], 10, 25 + 20 * x)
	popMatrix()
