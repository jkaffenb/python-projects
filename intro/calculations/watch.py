"""
 *****************************************************************************
   FILE:        watch.py

   AUTHOR:		Jack Kaffenbarger

   ASSIGNMENT:	Calculations (watch.py)

   DATE:		9/6/18

   DESCRIPTION:	Program designed to give the mirrored time, as Tom is a very 
   				poor consumer

 *****************************************************************************
"""
import math

def main():
    """ Watch Program """
    #Asking for user input
    upside_down = \
    input('What time does your upside-down watch read (hours:minutes)? ')
    
    #Finding the appropriate values
    length = upside_down.find(':')
    hours = int(upside_down[:length]) 
    minutes = int(upside_down[length+1:]) 
    
    #Flipping the clock
    hours_correct = (hours + 6) % 12
    minutes_correct = (minutes + 30) % 60
    
    #Printing values
    print('The right-side-up time is:', 
          str(hours_correct) + ':' + str(minutes_correct))
    #CITE: TA Geo
    #DESC: Helped me format to print the above string

if __name__ == "__main__":
    main()
