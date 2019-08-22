import Bacterium

# Controls and generates bacterium within given instance
class Bacteria:
    def __init__(self, currentUser, sizeBuffer, seeds, debug):
        self.debug = debug
        self.seeds = seeds
        self.bacteriumList = []
        self.sizeBuffer = sizeBuffer
        self.drawMetaball = True

        for x in range(len(currentUser.email)):
            self.bacteriumList += [
                Bacterium.Bacterium(sizeBuffer, x, seeds, currentUser.level)
            ]
    
    # Checks collisions between threashold and delegates metaball beziers
    def checkCollisions(self):
        leaderList = []
        deleteList = []
        collisionList = []

        # Adjustable variables for metaballs
        v = 0.5
        handleSize = 2.4
        distanceVar = 1.5

        # Check collisions and create a list of largest bacterium (leaders)
        # which store all interconnecting bacterium (neighbors)

        for bacterium1 in self.bacteriumList:
            for bacterium2 in self.bacteriumList:
                if (bacterium1.id == bacterium2.id and
                        [bacterium2.id, bacterium1.id] not in collisionList):
                    continue
                collision, leader = self.neighbors(bacterium1, bacterium2, distanceVar)
                if collision:
                    if leader not in leaderList and collision:
                        leaderList += [leader]
                    collisionList += [[bacterium1.id, bacterium2.id]]
                elif leader != None:
                    deleteList = list(set(deleteList + [leader]))

        # Remove bacterium from list
        for bacterium in deleteList:
            self.bacteriumList.remove(bacterium)

        # Gravitate neighbors towards leader
        for leader in leaderList:
            for neighbor in leader.neighbors:
                if leader.id != neighbor.id:
                    # Additional cleanup
                    if neighbor in deleteList:
                        leader.neighbors.remove(neighbor)
                        continue
                    neighbor.gravitate()

        if self.drawMetaball:
            for leader in leaderList:
                for neighbor1 in leader.neighbors:
                    for neighbor2 in leader.neighbors:
                        if neighbor1.id == neighbor2.id:
                            continue
                        self.metaball(neighbor1, neighbor2, v, handleSize, distanceVar)

        # Resets leader if bacterium not connected
        for bacterium in self.bacteriumList:
            if bacterium.connectedTo == []:
                bacterium.blobLeader = bacterium
            bacterium.connectedTo = []
                    
    def neighbors(self, bacterium1, bacterium2, distanceVar):
        d = dist(*bacterium1.realPosition + bacterium2.realPosition)
        radius1 = bacterium1.radius
        radius2 = bacterium2.radius
        maxDist = radius1 + radius2 * distanceVar

        if radius1 == 0 or radius2 == 0 or d > maxDist:
            return False, None
        else:
            bacterium1.connectedTo += [bacterium2]
            bacterium2.connectedTo += [bacterium1]

        # Consumption
        # If bacterium's overlap, add to larger one's radius and return loser to delete list

        consuming = False
        if d < bacterium1.radius and bacterium1.radius > bacterium2.radius:
            consumer = bacterium1
            consumee = bacterium2
            consuming = True
        if d < bacterium2.radius and bacterium2.radius > bacterium1.radius:
            consumer = bacterium2
            consumee = bacterium1
            consuming = True

        if consuming:
            consumer.radius += int(sqrt(consumee.radius))
            for x in range(2):
                # If merging bacterium would result in a radius that overlaps the dish, move it in to fit
                if consumer.radius + abs(width/2 - consumer.realPosition[x]) > (width/2)-self.sizeBuffer:
                    consumer.realPosition[x] = (width/2)-self.sizeBuffer-consumer.radius
                    consumer.position[x] = consumer.realPosition[x] - (width/2)
            return False, consumee


        # If the bacterium has a leader, it will fetch the leader
        # But by default, a bacterium's leader will be itself
        # Meaning it will either compare leaders or compare themselves

        if bacterium1.blobLeader.radius > bacterium2.blobLeader.radius:
            primary = bacterium1.blobLeader
            secondary = bacterium2.blobLeader
        else:
            primary = bacterium2.blobLeader
            secondary = bacterium1.blobLeader

        # Merge losers neighbors to winner
        # Reassign new leader

        primary.neighbors = list(set(primary.neighbors + secondary.neighbors))
        for neighbor in secondary.neighbors:
            neighbor.blobLeader = primary.blobLeader
            if neighbor.id != primary.blobLeader.id:
                neighbor.neighbors = [neighbor]
        leader = primary.blobLeader

        return True, leader
            
    
    def metaball(self, bacterium1, bacterium2, v, handleSize, distanceVar):
        d = dist(*bacterium1.realPosition + bacterium2.realPosition)
        radius1 = bacterium1.radius
        radius2 = bacterium2.radius
        maxDist = radius1 + radius2 * distanceVar

        if d > maxDist:
            return

        # Generates bezier curves which connect merging bacteria
        if (d < radius1 + radius2):
            u1 = acos((radius1*radius1+d*d-radius2*radius2)/(2*radius1*d))
            u2 = acos((radius2*radius2+d*d-radius1*radius1)/(2*radius2*d))
        else:
            u1 = u2 = 0

        angle = lambda a, b: atan2(a[1] - b[1], a[0] - b[0])
        angleBetweenCenters = angle(bacterium2.realPosition, bacterium1.realPosition)
        maxSpread = acos((radius1 - radius2) / d)

        # Angles
        angle1 = angleBetweenCenters + u1 + (maxSpread - u1) * v
        angle2 = angleBetweenCenters - u1 - (maxSpread - u1) * v
        angle3 = angleBetweenCenters + PI - u2 - (PI - u2 - maxSpread) * v
        angle4 = angleBetweenCenters - PI + u2 + (PI - u2 - maxSpread) * v

        getVector = lambda vector, angle, r: [
            vector[0] + r * cos(angle), vector[1] + r * sin(angle)]

        # Points
        p1 = getVector(bacterium1.realPosition, angle1, radius1)
        p2 = getVector(bacterium1.realPosition, angle2, radius1)
        p3 = getVector(bacterium2.realPosition, angle3, radius2)
        p4 = getVector(bacterium2.realPosition, angle4, radius2)

        totalRadius = radius1 + radius2
        d2Base = min(v * handleSize, dist(p1[0], p1[1], p3[0], p3[1]) / totalRadius)
        d2 = d2Base * min(1, d * 2 / totalRadius)

        r1 = radius1 * d2
        r2 = radius2 * d2

        # Handles
        h1 = getVector(p1, angle1 - HALF_PI, r1)
        h2 = getVector(p2, angle2 + HALF_PI, r1)
        h3 = getVector(p3, angle3 + HALF_PI, r2)
        h4 = getVector(p4, angle4 - HALF_PI, r2)
    
        noStroke()
        strokeWeight(4)
        fill(bacterium1.blobLeader.colour)
        beginShape()
        vertex(p1[0], p1[1])
        bezierVertex(h1[0], h1[1], h3[0], h3[1], p3[0], p3[1])
        bezierVertex(p3[0], p3[1], p4[0], p4[1], p4[0], p4[1])
        bezierVertex(h4[0], h4[1], h2[0], h2[1], p2[0], p2[1])
        endShape()

        # Vertex shape goes 1, 3, 4, 2
        # 1--2
        # \  /
        # /  \
        # 3--4
    
    # Only leaders can walk freely
    def walk(self):
        for x in range(len(self.bacteriumList)):
            bacterium = self.bacteriumList[x]
            if bacterium.id == bacterium.blobLeader.id:
                bacterium.walk()

    def drawBacteria(self):
        global debug
        for x in range(len(self.bacteriumList)):
            self.bacteriumList[x].drawBacterium()
        if self.debug:
            for x in range(len(self.bacteriumList)):
                textContent = "ID: " + str(self.bacteriumList[x].id) + "\nRadius: " + str(self.bacteriumList[x].radius)
                fill("#000000")
                text(
                    textContent, self.bacteriumList[x].realPosition[0],
                    self.bacteriumList[x].realPosition[1]
                )
