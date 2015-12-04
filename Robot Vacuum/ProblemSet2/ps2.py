# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

# For Python 2.7:
from ps2_verify_movement27 import testRobotMovement

# If you get a "Bad magic number" ImportError, you are not using
# Python 2.7 and using most likely Python 2.6:


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        #raise NotImplementedError
        self.width = width
        self.height = height
        self.cleanTiles = []

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        #raise NotImplementedError
        if (int(pos.getX()), int(pos.getY())) not in self.cleanTiles:
            self.cleanTiles.append((int(pos.getX()), int(pos.getY())))

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        #raise NotImplementedError
        return (m, n) in self.cleanTiles

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        #raise NotImplementedError
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        #raise NotImplementedError
        return len(self.cleanTiles)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        #raise NotImplementedError
        x = random.randint(0, self.width-1)
        y = random.randint(0, self.height-1)
        return Position(x, y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        #raise NotImplementedError
        x = math.floor(pos.getX())
        y = math.floor(pos.getY())
        return (x in range(0, self.width)) and (y in range(self.height))

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        #raise NotImplementedError
        self.position = room.getRandomPosition()
        self.direction = random.randint(0, 360-1)
        self.speed = speed
        self.room = room
        self.room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        #raise NotImplementedError
        return self.position

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        #raise NotImplementedError
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        #raise NotImplementedError
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        #raise NotImplementedError
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        #raise NotImplementedError
        current_position = self.getRobotPosition()
        new_position = current_position.getNewPosition(self.getRobotDirection(), self.speed)

        if self.room.isPositionInRoom(new_position):
            self.setRobotPosition(new_position)
            self.room.cleanTileAtPosition(new_position)
        else:
            direction_set = False
            current_direction = self.getRobotDirection()
            direction = None
            while not direction_set:
                direction = random.randint(0, 360-1)
                if direction != current_direction:
                    self.setRobotDirection(direction)
                    direction_set = True
# Uncomment this line to see your implementation of StandardRobot in action!
##testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 3
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    #raise NotImplementedError
    time_steps = []
    tiles_to_clean = math.ceil(width * height * min_coverage)
    for trial in range(num_trials):
        #create a room, a variable to keep record number of tiles
        #cleaned and a variable to keep of the total number of
        #time steps required to clean tiles_to_clean number of tiles
        room = RectangularRoom(width, height)
        tiles_cleaned = room.getNumCleanedTiles()
        time_steps_required = 0
        #create an array of robots
        robots = []
        for robot_index in range(num_robots):
            robot = robot_type(room, speed)
            robots.append(robot)
        while (tiles_cleaned < tiles_to_clean):
            time_steps_required += 1
            for robot in robots:
                robot.updatePositionAndClean()
            tiles_cleaned = room.getNumCleanedTiles()
        time_steps.append(time_steps_required)
    return sum(time_steps)/float(num_trials)

# Uncomment this line to see how much your simulation takes on average
##print  runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot)


# === Problem 4
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        #raise NotImplementedError
        '''
        #Solution 1 (doesn't always work)
        current_position = self.getRobotPosition()
        new_position = current_position.getNewPosition(self.getRobotDirection(), self.speed)

        if self.room.isPositionInRoom(new_position):
            self.setRobotPosition(new_position)
            self.setRobotDirection(random.randint(0, 360-1))
            self.room.cleanTileAtPosition(new_position)
        '''

        #Alternate implementation (more reliable and works always)
        current_position = self.getRobotPosition()
        updated = False
        while not updated:
            direction = random.randint(0, 360-1)
            new_position = current_position.getNewPosition(direction, self.speed)
            if self.room.isPositionInRoom(new_position):
                self.setRobotPosition(new_position)
                self.setRobotDirection(direction)
                self.room.cleanTileAtPosition(new_position)
                updated = True


def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


# === Problem 5
#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#showPlot1("Mean number of time-steps to clean 80% of the tiles", "Number of Robots", "Time-steps")
#showPlot1("Time It Takes 1 - 10 Robots To Clean 80% Of A Room", "Number of Robots", "Time-steps")
#

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#showPlot2("Time It Takes 2 Robots To Clean 80% Of A Room For Decreasing Aspect Ratios", "Aspect ratio", "Time-steps")
#showPlot2("Time It Takes Two Robots To Clean 80% Of Variously Shaped Rooms", "Aspect Ratio", "Time-steps")
#
