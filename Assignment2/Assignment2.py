#####################################################################################################
#    Assignment 2                                                                                   #
# Your assignment is to use the Datamuse API to generate a predictive text-driven Haiku on a        #
# topic of the user’s choice. Your program should first request that the user provide a topic to    #
# begin the Haiku generation. Then, your program should connect to the Datamuse API to find         #
# related words that satisfy the requirements of a Haiku (described below). Print your completed    #
# Haiku for the user to enjoy. Finally, your program should allow the user to generate as many      #
# Haikus as desired.                                                                                #
#####################################################################################################

import json
import requests


# function to ask user input whether user wants to continue or not
def to_continue():
    choice = input("\nWould you like to see another Haiku (yes/no)?")
    return choice


# function takes url and number of syllables. Extract the data if connection is okay
# then iteratively will check whether numSyllables are matched to get word and check if
# word is not stored in displayed before to avoid getting same word.

def get_data(url, n):
    response = requests.get(url)
    if response:
        data = json.loads(response.text)
    else:
        print("Sorry! Connection Error")

    for value in data:
        if value["numSyllables"] == n and value["word"] not in displayed:
            word = value["word"]
            displayed.append(word)
            return word


# Declared global variables
repeat = "yes"
displayed = []

# Entry message
print("\nHello, welcome to the predictive text Haiku generator! ")

# Generating haiku as much as user wants
while repeat.lower() == "yes":

    # storing 3 lines of generated haiku in haiku_lines list, where each line is stored in string.
    # Below code calling the get_data function by passing url and numSyllables, returned result stored
    # in word0.

    haiku_lines = []
    base_url1 = "https://api.datamuse.com/words?md=s&rel_trg="
    search = input("What would you like to see a Haiku about?")
    full_url1 = base_url1 + search
    word0 = get_data(full_url1, 3)          # Generated word 0 of first line with 3 syllables.

    # Below condition is checking whether topic result a valid haiku's or not.
    # If no word is generated then, printing message and calling function to_continue()
    # to user choice whether user wants to continue or not. Then skipping the rest of the code
    # using continue statement.
    if not word0:
        print("\nSorry, a valid Haiku could not be generated. \n")
        repeat = to_continue()
        continue

    base_url2 = "https://api.datamuse.com/words?md=s&lc="
    full_url2 = base_url2 + word0
    response = requests.get(full_url2)
    word1 = get_data(full_url2, 2)             # Generated word 1 of first line with 2 syllables.

    if not word1:
        print("\nSorry, a valid Haiku could not be generated. \n")
        repeat = to_continue()
        continue

    haiku_lines.append(word0 + " " + word1)      # first line is appended in result list.

    full_url2 = base_url2 + word1
    word2 = get_data(full_url2, 3)               # Generated word 2 of second line with 3 syllables

    if not word2:
        print("Sorry, a valid Haiku could not be generated. ")
        repeat = to_continue()
        continue

    full_url2 = base_url2 + word2
    word3 = get_data(full_url2, 2)              # Generated word 3 of second line with 2 syllables
    if not word3:
        repeat = to_continue()
        continue

    full_url3 = "https://api.datamuse.com/words?md=s&lc=" + word3 + "&rel_rhy=" + word1
    word4 = get_data(full_url3, 2)              # Generated word 4 of second line with 2 syllables

    if not word4:
        print("\nSorry, a valid Haiku could not be generated. \n")
        repeat = to_continue()
        continue

    haiku_lines.append(word2 + " " + word3 + " " + word4)        # second line is appended in result.

    full_url3 = base_url2 + word4
    word5 = get_data(full_url3, 3)              # Generated word 5 of third line with 3 syllables

    if not word5:
        print("\nSorry, a valid Haiku could not be generated. \n")
        repeat = to_continue()
        continue

    full_url3 = "https://api.datamuse.com/words?md=s&lc=" + word5 + "&rel_rhy=" + word1
    word6 = get_data(full_url3, 2)              # Generated word 6 of third line with 2 syllables

    if not word6:
        print("\nSorry, a valid Haiku could not be generated. \n")
        repeat = to_continue()
        continue

    haiku_lines.append(word5 + " " + word6)     # third line is appended in result.

    for line in haiku_lines:                    # printing the haiku_lines as final result
        print(line)

    repeat = to_continue()                      # Asking user whether they want to continue or not.

# exit message.
print("\nThank you for using haiku generator!")
