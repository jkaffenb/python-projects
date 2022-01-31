"""
 *****************************************************************************
   FILE:  game.py

   AUTHOR: Jack Kaffenbarger

   ASSIGNMENT: Final Project

   DATE: 12/3/18

   DESCRIPTION: Program that allows two users to play backgammon

 *****************************************************************************
"""

import random
from cs110graphics import *

#CITE: We worked on this die class in class
#DSEC: Used some of the componets from our yahtzee example
class Die(EventHandler):
    """ A die class """
    # class variables
    SIDES = 6
    POSITIONS = [None,
                 [(0, 0), None, None, None, None, None],
                 [(-.25, -.25), (.25, .25), None, None, None, None],
                 [(-.25, -.25), (.25, .25), (0, 0), None, None, None],
                 [(-.25, -.25), (.25, .25), (.25, -.25), (-.25, .25),
                  None, None],
                 [(-.25, -.25), (.25, .25), (.25, -.25), (-.25, .25), (0, 0),
                  None],
                 [(-.25, -.25), (.25, .25), (.25, -.25), (-.25, .25),
                  (-.25, 0), (.25, 0)]]
                 
    def __init__(self, win, width=30, center=(200, 200),
                 diecolor='white', pipcolor='black'):
        """ building attributes used in die """
        EventHandler.__init__(self)
        self._value = 1
        self._square = Rectangle(win, width, width, center)
        self._square.set_depth(20)
        self._square.set_fill_color(diecolor)
        self._square.add_handler(self)
        self._width = width
        self._center = center
        self._kept = False
        self._used = False
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(win, round(width / 12), center)
            pip.set_border_color(pipcolor)
            pip.set_fill_color(pipcolor)
            pip.set_depth(30)
            self._pips.append(pip)

    def handle_mouse_release(self, _):
        """ if the die is used toggle kept """
        if self._used:
            return
        self.toggle_kept()
        
            
    def used_on(self):
        """ turns used attribute on """
        self._used = True
        self._update()
         
    
    def used_off(self):
        """ turns used attribute off """
        self._used = False
        self._update()

        
    def toggle_kept(self):
        """ toggles kept attribute """
        self._kept = not self._kept
        self._update()

    def unkeep(self):
        """ unkeeps die """
        self._kept = False
        self._update()
            
    def add_to(self, win):
        """ Add this die to the win """
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)
        self._update()
    
    def roll(self):
        """ Change the value of this die randomly """
        self._value = random.randrange(Die.SIDES) + 1
        self._kept = False
        self._used = False
        #change player
        self._update()

    def get_value(self):
        """ Die to number """
        return self._value

    def get_kept(self):
        """ return kept value """
        return self._kept
    
    def get_used(self):
        """ return used value """
        return self._used

    def _update(self):
        """ private method .  make the appearance of the die match 
            its value and current highlight """
        if self._kept:
            self._square.set_border_color('aqua')
        elif self._used:
            self._square.set_border_color('red')
        else:
            self._square.set_border_color('black')

        positions = Die.POSITIONS[self._value]
        cx, cy = self._center
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].set_depth(25)
            else:
                self._pips[i].set_depth(15)
                fx, fy = positions[i]
                self._pips[i].move_to((round(cx + fx * self._width),
                                       round(cy + fy * self._width)))


class Button(EventHandler):
    """ Button Event Handler """
    def __init__(self, win, text, action, center, width, height, color='white'):
        """ building attributes used in button """
        EventHandler.__init__(self)
        self._rect = Rectangle(win, width, height, center)
        self._rect.set_fill_color(color)
        self._rect.set_depth(20)
        self._text = Text(win, text, center=center)
        self._text.set_depth(10)
        win.add(self._rect)
        win.add(self._text)
        self._action = action
        self._rect.add_handler(self)

    def handle_mouse_release(self, event):
        """ button handler """
        self._action()
        
class Game:
    """ Game """
    def __init__(self, win):
        """ adds board to window """             
        board = Board(win)
        board.add_to_window()
        
class Board:
    """ A class representing the playing board"""
    def __init__(self, win, width=300, height=250, center=(200, 250)):
        """ constructing all the parts of the board """
        self._dice = []
        self._win = win
        self._width = width
        self._height = height
        self._center = center
        self._player = 0    
        self._doubles_count = 0

        self._turn_marker = Circle(self._win, 5, (440, 170))
        self._turn_marker.set_fill_color('green')
        self._turn_marker.set_depth(10)  

        #creating buttons used in the game
        self._rollbutton = Button(self._win,
                                  "Roll!", self.roll, (40, 40), 100, 80) 
        self._turnbutton = Button(self._win, 
                                  "No Move", self.toggle_player, 
                                  (340, 40), 100, 80, 'red')
                                  
        #adding dice to the window
        for i in range(2):
            self._dice.append(Die(win, width=50, center=(150 + i * 55, 50)))
        for die in self._dice:
            die.add_to(win)
            die.roll()
      
        x, y = self._center

        dx = self._width // 36      # values used for creating triangles
        dy = self._height // 2

        #creating the playing board
        self._board = Rectangle(win, self._width, self._height, self._center)
        self._board.set_depth(20)
        self._board.set_fill_color('brown')

        #creating the center bar
        self._bar = Rectangle(win, self._width // 20, \
                              self._height, self._center)
        self._bar.set_depth(5)
        self._bar.set_fill_color('Black')

        #appending all the graphical objects for later use
        self._parts = [self._board, self._bar]
        
        
        triangle = 0
        
        #each for loop below deals with creating a quadrant of triangles
        #giving each alternating colors appropriate for a backgammon board
        
        #bottom right
        for i in range(1, 7):
            triangle = Polygon(win, [(((3 * i) - 3) * dx + x + 12, y + dy), \
                (((3 * i) - 2) * dx + x + 12, y), \
                (((3 * i) - 1) * dx + x + 12, y + dy)])
            triangle.set_depth(5)
            if i / 2 == i // 2:
                triangle.set_fill_color('white')
            else:
                triangle.set_fill_color('black')

            self._parts.append(triangle)
        
        #bottom left    
        for i in range(1, 7):
            triangle = Polygon(win, [(((3 * i) - 3) * dx * -1 + x - 12, \
                y + dy), (((3 * i) - 2) * dx * -1 + x - 12, y), \
                (((3 * i) - 1) * dx * -1 + x - 12, y + dy)])
            triangle.set_depth(5)
            if i / 2 == i // 2:
                triangle.set_fill_color('white')
            else:
                triangle.set_fill_color('black')

            self._parts.append(triangle)

        #top left
        for i in range(1, 7):
            triangle = Polygon(win, [(((3 * i) - 3) * dx * -1 + x - 12, \
                y - dy), (((3 * i) - 2) * dx * -1 + x - 12, y), \
                (((3 * i) - 1) * dx * -1 + x - 12, y - dy)])
            triangle.set_depth(5)
            if i / 2 == i // 2:
                triangle.set_fill_color('black')
            else:
                triangle.set_fill_color('white')

            self._parts.append(triangle)

        #top right
        for i in range(1, 7):
            triangle = Polygon(win, [(((3 * i) - 3) * dx + x + 12, y - dy), \
                (((3 * i) - 2) * dx + x + 12, y), \
                (((3 * i) - 1) * dx + x + 12, y - dy)])
            triangle.set_depth(5)
            if i / 2 == i // 2:
                triangle.set_fill_color('black')
            else:
                triangle.set_fill_color('white')

            self._parts.append(triangle)

        #adding player score boxes to the window
        self._blue_score = 0
        self._gray_score = 0

        self._blue_square = Square(win, 60, (400, 215))
        self._blue_square.set_depth(10)
        self._blue_header = Text(win, 'Blue', 10, (400, 170))
        self._blue_header.set_depth(10)
        
        self._gray_square = Square(win, 60, (400, 315))
        self._gray_square.set_depth(10)
        self._gray_header = Text(win, 'Gray', 10, (400, 270))
        self._gray_header.set_depth(10)

        
        

        self._triangles = []
        k = 19
        # building the board list that keeps track of all the piece positions
        for i in range(1, 7):
            self._triangles.append([7 - i, \
                (((3 * i) - 2) * dx + x + 12, y - dy), 0, 0])
        
        for i in range(7, 13):
            self._triangles.append([i, \
                (((3 * (i - 6)) - 2) * dx * -1 + x - 12, y - dy), 0, 0])
        
        for i in range(13, 19):
            self._triangles.append([k - 1, \
                (((3 * (i - 12)) - 2) * dx * -1 + x - 12, y + dy), 0, 0])
            k = k - 1
        
        for i in range(19, 25):
            self._triangles.append([i, \
                (((3 * (i - 18)) - 2) * dx + x + 12, y + dy), 0, 0])
        
        #bar positions
        self._triangles.append([0, self._center, 0, 0])
        self._triangles.append([25, self._center, 0, 0])

        
        #appending starting pieces
        self._pieces = []       
        for triangle in self._triangles:
            if triangle[0] == 1:
                for i in range(2):
                    circle = Piece(win, triangle[0], triangle[1], i, 
                                   'gray', self)
                    triangle[2] = i + 1
                    triangle[3] = 'gray'
                    self._pieces.append(circle)
                    
            if triangle[0] == 6:
                for i in range(5):
                    circle = Piece(win, triangle[0], triangle[1], i, 
                                   'blue', self)
                    triangle[2] = i + 1
                    triangle[3] = 'blue'
                    self._pieces.append(circle)
                    
            if triangle[0] == 8:
                for i in range(3):
                    circle = Piece(win, triangle[0], triangle[1], i, 
                                   'blue', self)
                    triangle[2] = i + 1
                    triangle[3] = 'blue'
                    self._pieces.append(circle)
                    
            if triangle[0] == 12:
                for i in range(5):
                    circle = Piece(win, triangle[0], triangle[1], i, 
                                   'gray', self)
                    triangle[2] = i + 1
                    triangle[3] = 'gray'
                    self._pieces.append(circle)
                    
            if triangle[0] == 13:
                for i in range(5):
                    circle = Piece(win, triangle[0], triangle[1], i, 
                                   'blue', self)
                    triangle[2] = i + 1
                    triangle[3] = 'blue'
                    self._pieces.append(circle)
                    
            if triangle[0] == 17:
                for i in range(3):
                    circle = Piece(win, triangle[0], triangle[1], i, 
                                   'gray', self)
                    triangle[2] = i + 1
                    triangle[3] = 'gray'
                    self._pieces.append(circle)
                    
            if triangle[0] == 19:
                for i in range(5):
                    circle = Piece(win, triangle[0], triangle[1], i, 
                                   'gray', self)
                    triangle[2] = i + 1
                    triangle[3] = 'gray'
                    self._pieces.append(circle)
                    
            if triangle[0] == 24:
                for i in range(2):
                    circle = Piece(win, triangle[0], triangle[1], i, 
                                   'blue', self)
                    triangle[2] = i + 1
                    triangle[3] = 'blue'
                    self._pieces.append(circle)
                    
        #adding starting pieces to the window
        for piece in self._pieces:
            piece.add_to_window()

        #adding misc. to the window
        self._parts.append(self._blue_square)
        self._parts.append(self._gray_square)
        self._parts.append(self._blue_header)
        self._parts.append(self._gray_header)
        self._parts.append(self._turn_marker)
        self._new_blue_score = Text(self._win, 
                                    str(self._blue_score), 20, (400, 215))
        self._new_blue_score.set_depth(5)
        self._new_gray_score = Text(self._win, 
                                    str(self._gray_score), 20, (400, 315))
        self._new_gray_score.set_depth(5)
        self._win.add(self._new_blue_score)
        self._win.add(self._new_gray_score)

        
        
    def toggle_player(self):
        """change player and toggle used appropriately """
        if self._player == 0:
            self._player = 1
            self._turn_marker.move_to((440, 270))
        elif self._player == 1:
            self._player = 0
            self._turn_marker.move_to((440, 170))
        for die in self.get_dice():
            die.used_on()
    
    def get_player(self):
        """ return player """
        return self._player
    
    def check_turn_change(self):
        """ check to see if appropriate to change turns """
        count = 0
        for die in self.get_dice():
            if die.get_used():
                count += 1

        if count == 2:
            if self._doubles_count == 1:        #TA mitchel
                self._doubles_count = 0
                self.toggle_player()
                return
            
            if self.check_doubles() and self._doubles_count == 0:
                self._doubles_count += 1
                for die in self.get_dice():
                    die.used_off()
            else:
                self.toggle_player()

    def check_doubles(self):
        """ check if player rolled doubles """
        dice_lst = []
        for die in self.get_dice():
            dice_lst.append(die.get_value())
        if dice_lst[0] == dice_lst[1]:
            print('doubles')
            for die in self.get_dice():
                die.used_off()
            return True

    
    def remove_pieces(self):
        """ remove pieces """
        for piece in self._pieces:
            piece.piece_remove() 
    
    def add_pieces(self):
        """ add pieces """
        self._pieces = []
        for triangle in self._triangles:
            if triangle[2] > 0:
                for i in range(triangle[2]):
                    circle = Piece(self._win, triangle[0], triangle[1], 
                                   i, triangle[3], self)
                    triangle[2] = i + 1
                    self._pieces.append(circle)
        for piece in self._pieces:
            piece.add_to_window()
    
    def update_grid(self, position_lst):
        """ update grid and player scores """
        self._triangles = position_lst
        self._win.remove(self._new_blue_score)
        self._win.remove(self._new_gray_score)
        self._new_blue_score = Text(self._win, 
                                    str(self._blue_score), 20, (400, 215))
        self._new_blue_score.set_depth(5)
        self._new_gray_score = Text(self._win, 
                                    str(self._gray_score), 20, (400, 315))
        self._new_gray_score.set_depth(5)
        self._win.add(self._new_blue_score)
        self._win.add(self._new_gray_score)
        

    def update_blue_score(self):
        """ update blue scores """
        winning_text_blue = Text(self._win, 'Blue Wins!', 15, (200, 500))
        winning_text_blue.set_depth(20)
        
        self._blue_score += 1
        if self._blue_score == 15:
            self._win.add(winning_text_blue)

    
    def update_gray_score(self):
        """ update gray scores """
        winning_text_gray = Text(self._win, 'Gray Wins!', 15, (200, 500))
        winning_text_gray.set_depth(20)
        self._gray_score += 1
        if self._gray_score == 15:
            self._win.add(winning_text_gray)

    def add_to_window(self):
        """ adds all the parts to the window """
        for part in self._parts:
            self._win.add(part)
                     
    def get_move_value(self):
        """ get move values """
        move = 0
        for die in self._dice:
            if die.get_kept():
                move += die.get_value()
        return move


    def roll(self):
        """ calls the roll function for each die """
        count = 0
        for die in self._dice:
            if die.get_used():
                count += 1
        # if both are used, allow roll button to roll both dice
        if count == 2:
            for die in self._dice:
                die.roll()

    def get_dice(self):
        """ return dice """
        return self._dice

    def get_triangles(self):
        """ return triangles """
        return self._triangles

    
class Piece(EventHandler):
    """ Piece """
    def __init__(self, win, triangle, triangle_center, 
                 piece_num, piece_color, board):
        """ constructor, adds pieces to the board"""
        EventHandler.__init__(self)
        self._win = win
        self._triangle = triangle 
        self._triangle_center = triangle_center
        self._piece_num = piece_num
        self._piece_color = piece_color
        self._board = board
        self._num = 0
        self._col = 0
        self._original_triangle = 0
        self._player = self._board.get_player()
       
        dx = 300 // 36 
        self._radius = int(1.5 * dx)  # intializing variables for pieces 
        
        x, y = self._triangle_center

        #if piece is on the bar
        if self._triangle == 0 or self._triangle == 25:                     
            self._circle = Circle(win, self._radius, self._triangle_center)
            self._circle.add_handler(self)
            self._circle.set_depth(3)
            self._circle.set_fill_color(self._piece_color)
            return

        #if piece is on the top half
        if self._triangle < 13:
            y += self._radius
            self._circle = Circle(win, self._radius, \
                (x, y + self._radius * self._piece_num * 2))
            self._circle.add_handler(self)
            self._circle.set_depth(3)
            self._circle.set_fill_color(self._piece_color)
        
        #if piece is on the bottom half   
        else:
            y -= self._radius
            self._circle = Circle(win, self._radius, \
                (x, y - self._radius * self._piece_num * 2))
            self._circle.add_handler(self)
            self._circle.set_depth(3)
            self._circle.set_fill_color(self._piece_color)
                  

    def add_to_window(self):
        """ adding pieces to the board """
        self._win.add(self._circle)


    def handle_mouse_release(self, _):
        """ determines if the selected move is allowed, and if the player
        needs to be switched. Also allows for bearing off"""
        self._player = self._board.get_player()
        self._original_triangle = self._triangle
        blue_count = 0
        gray_count = 0
        die_kept = 0

        #only allows player to move their own pieces
        if self._player == 0 and self._piece_color != 'blue':
            print('wrong piece')
            return
        if self._player == 1 and self._piece_color != 'gray':
            print('wrong piece')
            return
        
        #checks if blue or gray are ready to bear off
        for triangle in self._board.get_triangles()[6:24]:        
            if triangle[3] == 'blue':
                blue_count = 1
        for triangle in self._board.get_triangles()[:18]:          
            if triangle[3] == 'gray':
                gray_count = 1
        
        #keeps track of kept values and if the user hasn't selected a die
        #returns
        for die in self._board.get_dice():
            if die.get_kept():
                die_kept += 1
                if self._piece_color == 'blue':
                    self._triangle -= die.get_value()
                else:
                    self._triangle += die.get_value()
        #CITE: TA Collen
        #DESC: suggested moving the below code outside of the for loop
        if die_kept == 0:                                   
            return

        #keeps track of original triangle
        for triangle in self._board.get_triangles():        
            if triangle[0] == self._original_triangle:
                self._num = triangle[2]
                self._col = triangle[3]
        
        #starts bearing off if appropriate
        if blue_count == 0 and self._board.get_triangles()[24][2] == 0:                  
            if self.bearing_off_blue():
                self.rebuild()
                self._board.check_turn_change()
                return
        if gray_count == 0 and self._board.get_triangles()[25][2] == 0:
            if self.bearing_off_gray():
                self.rebuild()
                self._board.check_turn_change()
                return       
        
        #checks all legal moves and if it is, moves the pieces and rebuilds, 
        #otherwiset tells the user it was an illegal move and
        #untoggles the dice
        if self.check_blot() or self.check_triangle_zero() or \
            self.check_triangle_max():
            
            for triangle in self._board.get_triangles():
                if triangle[0] == self._original_triangle:
                    triangle[2] = self._num
                    triangle[3] = self._col
            self.rebuild()
            self._board.check_turn_change()
        else:
            print('illegal move')
            for die in self._board.get_dice():
                if die.get_kept():
                    die.toggle_kept()   
                     

    def rebuild(self):
        """ rebuilds the board and toggles the dice """
        for die in self._board.get_dice():
            if die.get_kept():
                die.used_on()
                die.toggle_kept()
                die._update()
        self._board.remove_pieces()
        self._board.update_grid(self._board.get_triangles())   
        self._board.add_pieces()

    def bearing_off_gray(self):
        """ starts bearing off for gray and updates the score"""
        if self._triangle > 24:
            self._board.update_gray_score()                  
            self._num -= 1
            if self._num == 0:
                self._col = 0
            
            for triangle in self._board.get_triangles():
                if triangle[0] == self._original_triangle:
                    triangle[2] = self._num
                    triangle[3] = self._col
            return True

    def bearing_off_blue(self):
        """ starts bearing off for blue and updates the score"""
        if self._triangle < 1:
            self._board.update_blue_score()                  
            self._num -= 1
            if self._num == 0:
                self._col = 0
            
            for triangle in self._board.get_triangles():
                if triangle[0] == self._original_triangle:
                    triangle[2] = self._num
                    triangle[3] = self._col
            return True
        

    def check_triangle_max(self):
        """ checks if the new spot is the same color and less than 5 """
        for triangle in self._board.get_triangles():
            if triangle[0] == self._triangle:
                if triangle[3] == self._piece_color and triangle[2] < 5: 
                    triangle[2] += 1
                    self._num -= 1
                    if self._num == 0:
                        self._col = 0
                    return True
        self._triangle = self._original_triangle
        return False

    def check_blot(self):
        """ checks if the new spot has only one piece of a different color,
        if so it moves the piece to the bar """

        for triangle in self._board.get_triangles():
            if triangle[0] == self._triangle:
                if triangle[2] == 1 and triangle[3] != self._piece_color:
                    self._num -= 1
                    if self._piece_color == 'blue':
                        self._board.get_triangles()[24][2] += 1             
                        self._board.get_triangles()[24][3] = triangle[3]
                    if self._piece_color == 'gray':
                        self._board.get_triangles()[25][2] += 1             
                        self._board.get_triangles()[25][3] = triangle[3]

                    triangle[3] = self._piece_color
                    if self._num == 0:
                        self._col = 0
                    return True
        return False

    def check_triangle_zero(self):
        """ checks if the new spot has no pieces on it """
        for triangle in self._board.get_triangles():
            if triangle[0] == self._triangle:
                if triangle[2] == 0:
                    triangle[2] += 1
                    triangle[3] = self._piece_color                  
                    self._num -= 1
                    if self._num == 0:
                        self._col = 0
                    return True
        return False

     
    def piece_remove(self):
        """ removes the piece from the window """
        self._win.remove(self._circle)

    
def program(win):
    """ play a game """
    _ = Game(win)
    
        

def main():
    """ Main pgm """
    StartGraphicsSystem(program, 600, 600)

if __name__ == "__main__":
    main()