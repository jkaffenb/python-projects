"""
 *****************************************************************************
   FILE:        decrypt.py

   AUTHOR:      Jack Kaffenbarger

   ASSIGNMENT:  keyword.py

   DATE:        9/20/18

   DESCRIPTION: Program that takes an encrypted input and key, and outputs an 
   unencrypted message, while also searching for clues embeded in the text

 *****************************************************************************
"""

def remove_spaces(text):
    """ Given string   text  , build and return a new string with all
    spaces removed.  For example, from "Happy birthday   to you", return
    "Happybirthdaytoyou" """
    
    squished_text = ''
    for char in text:
        #Getting rid of the spaces in text
        if char != ' ':
            squished_text = squished_text + char
    return squished_text


def subtract(text, key):
    """ Given two uppercase letters of the alphabet, determine and return the
    unencrypted letter from the encrypted_letter was generated using
    key_letter.  For example, when encrypted_letter is "J" and key_letter is
    "R", return "S". """ 
    
    #Defining alphabet and asking for user input
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    index_text = alphabet.find(text)
    index_key = alphabet.find(key)

    #Adding the values of the key and text and outputting the unencrypted 
    #characters
    unencrypted = alphabet[(26 - index_key + index_text) % 26] 
    return unencrypted

def decrypt(text, key):
    """ For each letter in   text  , determine the letter from which it was 
    encrypted using   key  . Build and return the string of these letters."""
    
    #Defining strings used in the loop
    converted_letter = ''
    converted_string = ''
    key_letter = ''
    text_letter = ''
    
    #Got help from TA _____ with using one loop to cycle through two strings
    for i in range(len(text)):
        #Cycling through both key and text
        key_letter = key[i % (len(key))]
        text_letter = text[i]
        #Using the subtract function to convert individual letters
        converted_letter = subtract(text_letter, key_letter)
        #Combining the letters into a single string
        converted_string = converted_string + converted_letter
    return converted_string

def report(message, clues):
    """ Print the   message  , and, for each clue in   clues  , if it occurs in 
      message  , indicate so on the output. """
    print("The decrypted message is", message)
    for entry in clues:
        if entry in message:
            print('Clue', entry, 'discovered in', message)


def main():
    """
    This function is provided in full. Its job is to control
    the flow of the program, and offload the details to the
    other functions.
    """
    captured_text = input('Enter the captured text: ')
    keyword = input('Enter a keyword: ')
    clues = input('Enter the clues separated by one space: ')
    clueList = clues.split()

    # Take all spaces out of the captured text:
    squished_text = remove_spaces(captured_text)

    # Send the captured text for decryption:
    decrypted_text = decrypt(squished_text, keyword)

    # Check the decrypted text for clues that indicate a real message.
    report(decrypted_text, clueList)


# Here we invoke the main function. This code is always included in our
# python programs.
if __name__ == "__main__":
    main()
