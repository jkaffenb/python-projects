"""
 *****************************************************************************
   FILE:                 yahtzee.py, all but student methods written by 
                         Alistair Campbell for Computer Science 110

   STUDENT NAME:        Jack Kaffenbarger

   ASSIGNMENT:          yahtzee.py

   DATE:                10/23/18

   DESCRIPTION:         Program that allows user to roll five dice up to three
                        times, and then checks the outcomes with various 
                        scoring methods


 *****************************************************************************
"""

import random

# Information for drawing dice:
PIPSTRINGS = [None, ["   ", " * ", "   "], ["*  ", "   ", "  *"],
              ["*  ", " * ", "  *"], ["* *", "   ", "* *"],
              ["* *", " * ", "* *"], ["* *", "* *", "* *"]]

HAND_TYPES = ['aces', 'twos', 'threes', 'fours', 'fives', 'sixes',
              'three_of_a_kind', 'four_of_a_kind', 'full_house',
              'small_straight', 'large_straight', 'yahtzee',
              'chance']

# constants for controlling when to exit the program
END = 0       
CONTINUE = 1

# Constants describing rolls
ORDINALS = [None, "First", "Second", "Third"]

class Die:
    """ A class representing a multi-sided die """

    # constructor:
    def __init__(self, num_sides=6):
        self._num_sides = num_sides
        self._value = 1
    
    def roll(self):
        """ Change to a new random value """
        self._value = random.randint(1, self._num_sides)

    def get_value(self):
        """ Return the value of this die """
        return self._value

    def set_value(self, value):
        """ Set the value of this die """
        assert value in range(1, self._num_sides + 1)
        self._value = value

class YahtzeeHand:
    """ Represents a 5-dice hand of Yahtzee, supporting rolling 
        a selection of the dice, and calculating possible scores """
    def __init__(self):
        self._dice = []
        for _ in range(5):
            self._dice.append(Die())

    def set_hand(self, values):
        """ Make this yahtzee hand have the given values """
        assert len(values) == 5
        for val in values:
            assert val in range(1, 7)
        for i in range(5):
            self._dice[i].set_value(values[i])
    
    def roll(self, indices=range(5)):
        """ Roll dice given by the sequence of indices. """
        for i in indices:
            self._dice[i].roll()

    def _get_choice_indices(self, value_list):
        """ decide whether value_list represents  
        a selction of dice values from this hand.  Return 
        None if not.  Otherwise, return a list of indices. """
        # build a list of index/value pairs for the dice:
        iv_pairs = [(i, self._dice[i].get_value()) for i in range(5)]
        choices = [] # the pairs that match values we want to roll
        for value in value_list:
            # find value in iv_pairs, if possible
            items = [pair for pair in iv_pairs if pair[1] == value]
            if items == []:
                return None  # can't find any!
            # take the first match
            item = items[0]
            # add it to choices, remove it from iv_pairs
            choices.append(item)
            iv_pairs.remove(item)
        # return the indices
        return [tuple[0] for tuple in choices]
            
    def user_input_roll(self, roll_num):
        """ Ask the user for the values of dice to roll until valid 
        selection is made.  Roll those dice. """
        while True:  # loop exits from the middle
            response = input("{} roll.  Select dice values to roll: "
                             .format(ORDINALS[roll_num]))
            if response == "":
                return END
            # get rid of delimiters, and make a list of values
            # from input.
            value_list = [int(x) for x in
                          "".join([ch if ch in '0123456789' else ' '
                                   for ch in response]).split()]
            
            # see whether it's valid..
            indices = self._get_choice_indices(value_list)
            if indices is not None:
                # ..Got a valid input!  Roll them and be done!
                self.roll(indices)
                return CONTINUE
            # ..Not valid.  Chastize and repeat.
            print("Invalid input.  Try again.")
                    
    def show(self):
        """ Show the values of the Yahtzee hand in a nice way """
        print("+" + "---+" * 5)
        for row in range(3):
            print('|', end="")
            for i in range(5):
                print(PIPSTRINGS[self._dice[i].get_value()][row], end='|')
            print()
        print("+" + "---+" * 5)
        for i in range(5):
            print(" ({})".format(self._dice[i].get_value()), end="")
        print()

    def show_all_scores(self):
        """ Show all scores that could be entered for this 
        yahtzee hand """
        for hand_type in HAND_TYPES:
            score = getattr(self, hand_type+"_score")()
            print("{:>15s}: {}".format(hand_type, score))
            
    def _get_values(self):
        """ Return a list of the dice values """
        return [self._dice[i].get_value() for i in range(5)]

    def _total_dice_with(self, value):
        """ Return a sum of dice that have the given value """
        return sum([x for x in self._get_values() if x == value])

    # ------- Scoring methods begin here ---------
    
    def aces_score(self):
        """ Return total for aces """
        return self._total_dice_with(1)

    def twos_score(self):
        """ Return total for twos """
        return self._total_dice_with(2)

    def threes_score(self):
        """ Return total for threes """
        return self._total_dice_with(3)

    def fours_score(self):
        """ Return total for fours """
        return self._total_dice_with(4)

    def fives_score(self):
        """ Return total for fives """
        return self._total_dice_with(5)

    def sixes_score(self):
        """ Return total for sixes """
        return self._total_dice_with(6)

    def chance_score(self):
        """ Return total of dice """
        return sum(self._get_values())

    # ---------- Student helper methods go here ----------


    
    # ---------- Students implement these methods ----------
    # Please use the area above to write any private helper methods that you
    # would like.
    
    def three_of_a_kind_score(self):
        """ Return the sum of three dice with the same value, or zero """
        # runs through all possible combinations and checks if the sum >= to 3
        for i in range(1, 7):
            if (self._total_dice_with(i) / i) >= 3:
                return i * 3
        return 0

    def four_of_a_kind_score(self):
        """ Return the sum of four dice with the same value, or zero """
        # runs through all possible combinations and checks if the sum >= to 4
        for i in range(1, 7):
            if (self._total_dice_with(i) / i) >= 4:
                return i * 4
        return 0

    def full_house_score(self):
        """ Return 25 if this is a full house.  Or zero if not. """
        # initializing 
        count = 0
        # loops to see if there is a three of a kind score and two pairs
        for i in range(1, 7):
            if (self._total_dice_with(i) / i) >= 2:
                count += 1
        if self.three_of_a_kind_score() > 0 and count > 1:
            return 25
        return 0

    def small_straight_score(self):
        """ Return 30 if this is a small straight.  Or zero if not. """
        # runs through all three possible combinations of small straights
        if self.aces_score() >= 1 and self.twos_score() >= 2 and \
        self.threes_score() >= 3 and self.fours_score() >= 4:
            return 30

        if self.twos_score() >= 2 and self.threes_score() >= 3 and \
        self.fours_score() >= 4 and self.fives_score() >= 5:
            return 30

        if self.threes_score() >= 3 and self.fours_score() >= 4 and \
        self.fives_score() >= 5 and self.sixes_score() >= 6:
            return 30
        return 0

    def large_straight_score(self):
        """ Return 40 if this is a large straight.  Or zero if not. """
        # runs through both possible combinations of large straights
        if self.aces_score() >= 1 and self.twos_score() >= 2 and \
        self.threes_score() >= 3 and self.fours_score() >= 4 and \
        self.fives_score() >= 5:
            return 40
        if self.twos_score() >= 2 and self.threes_score() >= 3 and \
        self.fours_score() >= 4 and self.fives_score() >= 5 and \
        self.sixes_score() >= 6:
            return 40
        return 0

    def yahtzee_score(self):
        """ Return 50 if this is yahtzee.  Or zero if not. """
        # runs through all possible combinations and checks if the sum >= to 5 
        for i in range(1, 7):
            if (self._total_dice_with(i) / i) == 5:
                return 50
        return 0

    # ------------------------------------------------------------------

def main():
    """ The main program """
    yh = YahtzeeHand()
    _ = input("First roll.  Press enter to roll the dice!")
    yh.roll()
    yh.show()
    yh.show_all_scores()
    roll_num = 2
    while roll_num <= 3 and yh.user_input_roll(roll_num) == CONTINUE:
        yh.show()
        yh.show_all_scores()
        roll_num += 1

if __name__ == "__main__":
    main()
    
