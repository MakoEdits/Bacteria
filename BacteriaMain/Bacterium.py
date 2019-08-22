import random

class Bacterium:
    def __init__(self, sizeBuffer, number, seeds, level):
        self.level = level
        self.seeds = seeds
        self.id = number
        self.sizeBuffer = sizeBuffer
        self.genColour()
        self.genRadius()
        self.neighbors = [self]
        self.blobLeader = self
        self.connectedTo = []

        # Generate intial position
        dishRadius = height/2 - self.sizeBuffer
        sumSeed = seeds[0] + seeds[1] + seeds[2]
        # Mutate from seed
        mutation = ((((self.id+1)**2)*sumSeed)+self.id**2)**5
        congruence = (mutation % dishRadius)+1
        # Map min and max to 0 and 1 so that it fits into uniformly random position algorithm
        mapped = map(congruence, 1, dishRadius, 0, 1)
        a = mapped * 2 * PI
        r = (height-self.sizeBuffer*2-self.radius*2)/2*sqrt(mapped)
        x = r * cos(a)
        y = r * sin(a)
        # Position is used after translation is applied when drawing
        self.position = [x, y]
        # Real position reflects actual position
        self.realPosition = [width/2 + self.position[0], height/2 + self.position[1]]

    # Apply linear congruence algorithm using id and seed to generate bacterium color
    def genColour(self):
        # Seed mutation based on id mod FFFFFF in decimal
        congurence = ((((self.id+1)*self.seeds[0])+self.id)**5) % 16777215
        self.colour = "#" + str(hex(congurence))[-6:]
        self.originalColour = self.colour

    # Apply linear congruence algorithm using id and seed to generate radius size
    def genRadius(self):
        minSize = 5
        maxSize = 50
        # Lower bound + seed mutation based on id mod upper bound range
        mutation = (((self.id+1)*self.seeds[1])+self.id)**5
        self.radius = (minSize)+(mutation%(maxSize-minSize))

    # Draw bacterium instance using data
    def drawBacterium(self):
        pushMatrix()
        noStroke()
        translate(width / 2, height / 2)
        strokeWeight(3)
        fill(self.blobLeader.colour)
        ellipse(self.position[0], self.position[1], self.radius * 2, self.radius * 2)
        popMatrix()

    # Move bacterium in pseudo random increments (not very convincing, would redo)
    def walk(self):
        minMovement = 1
        maxMovement = 15

        # Mutate seed based on input
        mutation = lambda position, exponent: (
            (self.seeds[2]*self.level+position)+self.id+self.level+position
        )**exponent

        congruence = lambda position: (minMovement)+(mutation(position,3)%(maxMovement-minMovement))
        x = congruence(self.position[0])
        y = congruence(self.position[1])

        # Returns set of calculations to try get fair odds
        randomSeed = lambda var: len(str(self.id+self.level*var+self.seeds[2]))
        if randomSeed(x) % 2 == 0:
            x *= -1
        if randomSeed(y) % 2 == 0:
            y *= -1
        # If movement outside of circle
        radius = (height/2)-self.sizeBuffer

        if self.realPosition[0] + x > radius:
            x *= -1
        if self.realPosition[1] + y > radius:
            y *= -1

        self.position = [self.position[0]+x, self.position[1]+y]
        self.realPosition = [(width/2)+self.position[0], (height/2)+self.position[1]]

    # Pull bacterium towards leader for consumption
    def gravitate(self):
        p1x = self.realPosition[0]
        p2x = self.blobLeader.realPosition[0]
        p1y = self.realPosition[1]
        p2y = self.blobLeader.realPosition[1]

        distance = [p2x - p1x, p2y - p1y]

        self.position = [
            self.position[0] + (distance[0]/4),
            self.position[1] + (distance[1]/4)
        ]

        self.realPosition = [
            (width/2)+self.position[0],
            (height/2)+self.position[1]
        ]