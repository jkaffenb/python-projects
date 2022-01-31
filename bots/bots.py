"""
 *****************************************************************************
   FILE:  bots.py

   AUTHOR: Jack Kaffenbarger    

   ASSIGNMENT: bots.py

   DATE: 12/2/18

   DESCRIPTION: Program that constructs two bots that will move around the 
   graphics window when clicked on, and transform when they overlap

 *****************************************************************************
"""


from cs110graphics import *
import random

class Bot:
    def __init__(self, win, width, center, direction='east', speed=20):
        """ constructor  """
        
        self._width = width
        self._center = center
        self._direction = direction
        self._speed = speed
        self._win = win
        
        #contructing parts of the bot
        square = Square(win, self._width, self._center)
        square.set_depth(30)
        
        eye = Circle(win, self._width // 2, self._center)
        eye.set_fill_color('green')
        eye.set_depth(20)

        text_go = Text(win, 'Go!', self._width // 3, self._center)
        text_go.set_depth(10)

        text_stop = Text(win, 'Stop', self._width // 3, self._center)
        text_stop.set_depth(40)
        
        #adding all the graphical parts to a list to be manipulated later
        self._parts = [square, eye, text_go, text_stop]


        
    def add_to_window(self):
        """ adds all the parts to the window """
        for part in self._parts:
            self._win.add(part)
    
    def add_handler(self, handler):
        """ provide call-back function for user interaction """
        # don't modify this.
        for part in self._parts:
            part.add_handler(handler)
            
    def move(self):
        """ moves the bot in the direction it is 'facing', and updates 
        the center """
        
        if self._direction == 'east':
            dx, dy = self._speed, 0
        if self._direction == 'south':
            dx, dy = 0, self._speed
        if self._direction == 'west':
            dx, dy = -self._speed, 0
        if self._direction == 'north':
            dx, dy = 0, -self._speed

        # updating the center
        x, y = self._center
       
        x += dx
        y += dy
        self._center = x, y

        #moving each part the desired distance
        for part in self._parts:
            part.move(dx, dy)
        
            
    def turn_left(self):
        """ rotates the direction the bot is 'facing' """
        #CITE: TA Minh 
        #DESC: Helped me utilize 'elif' for running through if statements
        
        if self._direction == 'east':
            self._direction = 'north'
        elif self._direction == 'north':
            self._direction = 'west'
        elif self._direction == 'west':
            self._direction = 'south'
        elif self._direction == 'south':
            self._direction = 'east'

    def turn_right(self):
        """ rotates the direction the bot is 'facing' """
        
        if self._direction == 'east':
            self._direction = 'south'
        elif self._direction == 'north':
            self._direction = 'east'
        elif self._direction == 'west':
            self._direction = 'north'
        elif self._direction == 'south':
            self._direction = 'west'
    
    def speed_up(self):
        """ multiplies the current speed by 3 """
        
        self._speed *= 3

    def slow_down(self):
        """ divides the current speed by 3 """
        
        self._speed //= 3
    
    def crash(self):
        """ changes the bot's eye color """
        #CITE: Dan Comey 
        #DESC: suggested indexing from self._parts to change the color
        
        self._parts[1].set_fill_color('red')
        self._parts[2].set_depth(40)
        self._parts[3].set_depth(10)

    def uncrash(self):
        """ reverts the bot back to its original state """
        
        self._parts[1].set_fill_color('blue')
        self._parts[2].set_depth(10)
        self._parts[3].set_depth(40)

    def get_width(self):
        """ returns the width """
        return self._width

    def get_center(self):
        """ returns the center """
        return self._center

    def overlaps(self, other):
        """ obtains the max and min x and y values for both bots, and then 
        checks if they are contained within each other """
        

        x, y = self._center

        # get x range for the bot
        x_min = x - self._width // 2 
        x_max = x + self._width // 2 
        
        # get y range for the bot
        y_min = y - self._width // 2
        y_max = y + self._width // 2

        other_x, other_y = other.get_center()
        
        # x range for other bot
        other_x_min = other_x - other.get_width() // 2
        other_x_max = other_x + other.get_width() // 2

        # y range for other bot
        other_y_min = other_y - other.get_width() // 2
        other_y_max = other_y + other.get_width() // 2

        #checks if either either max and min values are contained within the 
        #other bot's range. If both the x range and y range overlap then 
        #returns true
        if (x_min <= other_x_min <= x_max or x_min <= other_x_max <= x_max) \
        and (y_min <= other_y_min <= y_max or y_min <= other_y_max <= y_max):
            return True

        #if above is not met, return false
        return False
        
   
class BotHandler(EventHandler):
    """ A class for handling events for Bots. """
    def __init__(self, bot):
        """ Constructor """
        EventHandler.__init__(self)
        self._bot = bot
        
    def handle_mouse_release(self, event):
        """ This code will run when the user clicks on a bot, randomly turns 
        the bot """
       
        self._bot.move()
        x = random.randrange(0, 2)

        if x == 1:
            self._bot.turn_left()
        else:
            self._bot.turn_right()

            
def program(win):
    """ Set up the graphics in the window """
    # change this as you see fit!
    bot = Bot(win, random.randrange(20, 100), \
        (random.randrange(0, 400), random.randrange(0, 400)))
    bot2 = Bot(win, random.randrange(20, 100), \
        (random.randrange(0, 400), random.randrange(0, 400)))
    bot.add_to_window()
    bot2.add_to_window()
    bot.add_handler(BotHandler(bot))
    bot2.add_handler(BotHandler(bot2))


def main():
    """ The main program """
    StartGraphicsSystem(program)

if __name__ == "__main__":
    main()
