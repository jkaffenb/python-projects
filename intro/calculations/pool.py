"""
 *****************************************************************************
   FILE:        pool.py

   AUTHOR:		Jack Kaffenbarger

   ASSIGNMENT:	Calculations(pool.py)

   DATE:		9/3/2018

   DESCRIPTION:	Basic program to find out how long it will take a pool to fill
   using a simple units conversion and volume formula

 *****************************************************************************
"""


def main():
    """ Pool Calculations """
    import math
    #Asks user to input their desired parameters and converts to inches
    pool_length = float(input('Pool length (feet): ')) * 12 
    pool_width = float(input('Pool width (feet): ')) * 12
    additional_depth_desired = float(input
                                     ('Additional depth desired (inches): '))
    #CITE: TA Geo
    #DESC: Helped me use an appropriate line break
    water_fill_rate = float(input('Water fill rate (gal/min): '))
    gallons_to_cubic_inches = 231.0
    #CITE: Google's unit converter
    #DESC: Where I got the gallons to cubic inches constant
    
    #Fill-time formula
    time_minutes = ((pool_length * pool_width * additional_depth_desired) / 
                    gallons_to_cubic_inches * (1/water_fill_rate))

    #Converting minutes to the appropriate time
    hours = int(time_minutes // 60)
    minutes = math.floor(time_minutes % 60)
    seconds = round(((time_minutes % 60) - minutes) * 60)

    #Printing computed values
    print('Time:', '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)) 
    #CITE: Piazza.com
    #DESC: Used the given information on how to format with leading zeros and 
    #      desired widths
	  
if __name__ == "__main__":
    main()
