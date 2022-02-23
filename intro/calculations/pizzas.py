"""
 *****************************************************************************
   FILE:        pizzas.py

   AUTHOR:		Jack Kaffenbarger

   ASSIGNMENT:	Calculations(pizzas.py)

   DATE:		9/3/2018

   DESCRIPTION:	Simple program to convert normal pizzas to "Super Pies!" using 
   basic area formulas

 *****************************************************************************
"""


def main():
    """ Pizza Program """
    import math
    
    #Asking user for inputs relevant to the problem
    standard_diameter = \
    float(input('What is the diameter of a "standard" size pie? '))
    standard_slices = \
    float(input('How many slices are in a standard size pie? '))
    standard_slices_number = \
    float(input('How many standard slices do you want? '))
    diameter_super_pie = \
    float(input('What is the diameter of the pies you will buy? '))

    #Converting given inputs into total area of pie, so it's easier to change
    #to "Super Pies!"
    area_of_pie = float((((standard_diameter/2)**2)/standard_slices) * 
                        standard_slices_number)
    #Converting area of pie into number of Super Pies
    number_of_super_pies = area_of_pie/(diameter_super_pie/2)**2

    #Converting to whole numbers that make sense
    diameter_super_pie = int(diameter_super_pie)
    number_of_super_pies = math.ceil(number_of_super_pies)
    
    #Printing computed values
    print("You will need to buy", str(number_of_super_pies), 
          str(diameter_super_pie) + "-inch diameter pies.")
    #CITE: TA Geo
    #DESC: Helped me print a string and how to use appropriate line breaks

if __name__ == "__main__":
    main()
