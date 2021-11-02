# Python program to implement Morse Code Translator
'''
VARIABLE KEY
'cipher' -> 'stores the morse translated form of the english
string'
'decipher' -> 'stores the english translated form of the morse
string'
'citext' -> 'stores morse code of a single character'
'i' -> 'keeps count of the spaces between morse characters'
'message' -> 'stores the string to be encoded or decoded'
'''
# Dictionary representing the morse code chart
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
  'C':'-.-.', 'D':'-..', 'E':'.',
  'F':'..-.', 'G':'--.', 'H':'....',
  'I':'..', 'J':'.---', 'K':'-.-',
  'L':'.-..', 'M':'--', 'N':'-.',
  'O':'---', 'P':'.--.', 'Q':'--.-',
  'R':'.-.', 'S':'...', 'T':'-',
  'U':'..-', 'V':'...-', 'W':'.--',
  'X':'-..-', 'Y':'-.--', 'Z':'--..', 
  '1':'.----', '2':'..---', '3':'...--',
  '4':'....-', '5':'.....', '6':'-....',
  '7':'--...', '8':'---..', '9':'----.',
  '0':'-----', ',':'--..--', '.':'.-.-.-',
  '?':'..--..', '/':'-..-.', '-':'-....-',
  '(':'-.--.', ')':'-.--.-'}
def encrypt(message):   # Function to encrypt the string according to the morse code chart

  cipher = ''
  for letter in message:
    if letter != ' ':
      cipher += MORSE_CODE_DICT[letter] + ' '     # Looks up the dictionary and adds the correspponding morse code along with a space to separate morse codes for different characters

    else:
      cipher += ' '   # 1 space indicates different characters and 2 indicates different words

  return cipher
def decrypt(message):   # Function to decrypt the string from morse to english
  message += ' '    # extra space added at the end to access the last morse code
  decipher = ''
  citext = ''
  for letter in message:
    if (letter != ' '):   # checks for space
      i = 0   # counter to keep track of space
      citext += letter    # storing morse code of a single character 
      
    else:   # in case of space
      i += 1    # if i = 1 that indicates a new character

    if i == 2 :   # if i = 2 that indicates a new word

      decipher += ' '   # adding space to separate words

    else:
      (reverse of encryption)   # accessing the keys using their values

      decipher +=list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
      citext = ''
return decipher

def main():   # Hard-coded driver function to run the program

  message = "MORSECAPTCHA"
  result = encrypt(message.upper())
  print (result)
  message = "-- --- .-. ... . -.-. .- .--. - .- "
  result = decrypt(message)
  print (result)
  
if __name__ == '__main__':    # Executes the main function
  main()
