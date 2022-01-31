"""
 *****************************************************************************
   FILE:        metricTime.py

   AUTHOR:		Jack Kaffenbarger

   ASSIGNMENT:	Calculations (metricTime.py)

   DATE:		9/6/18

   DESCRIPTION:	Converting Earth time to 'Metric Time' using mods, remainder
   division, and basic splice and find functions.

 *****************************************************************************
"""

import math
def main():
    """ metricTime """
    #Asking for user input
    military_time = \
    input('Enter the time of day in military time (HH:MM:SS): ')
   
    #Next few lines are dedicated to sorting through the input to get 
    #variables their appropriate values
    length = military_time.find(':')
    length_useless = military_time[length+1:]
    length2 = length_useless.find(':')
    military_hours = int(military_time[:length])
    military_minutes = int(military_time[length+1:length2+length+1])
    military_seconds = int(military_time[length+length2+2:])
    #CITE: Professor Campbell
    #DESC: Helped work through making the program more resilient to different
    #      inputs
    
    #Converting everything to seconds
    total_military_seconds = \
    (((military_hours * 60)+military_minutes)*60)+military_seconds
    
    #Developing a constant to convert earth seconds to martian seconds, the 
    #number of seconds in a day was found on the calculations prompt
    military_to_metric_seconds = float(100000/86400)
    #CITE: Piazza resource page
    #DESC: Used the seconds in a day from the calculations page on piazza
    total_metric_seconds = \
    round(total_military_seconds * military_to_metric_seconds, 2)
    
    #Breaking down the metric seconds into their respective categories
    metric_hours = int(total_metric_seconds // 1000)
    metric_minutes = int((total_metric_seconds % 1000) // 100)
    metric_seconds = round(total_metric_seconds % 100, 2)

    #Printing final product
    print('The "metric" time is:')
    print('{:02d}:{:01d}:{:05.2f}'.format
          (metric_hours, metric_minutes, metric_seconds))
    #CITE: Earlier code used by myself
    #DESC: My pool.py formula's print statement


if __name__ == "__main__":
    main()