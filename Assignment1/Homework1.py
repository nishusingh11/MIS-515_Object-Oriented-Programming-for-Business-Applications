"""
Assignment 1 : Create a Python program that utilizes historical name popularity to
perform two types of analyses. The program should first ask the user which mode they would
like to use (name comparison or maximum popularity). If the user chooses name comparison,
then the user should be asked for two names to compare. The program should compute the
totals for each name (sum) between 1900 and 2014. The program should report totals for each
name as well as which name was most common. If the user chooses the maximum popularity
option, then the program should ask the user for a single name. The program should report the
year between 1900 and 2014 in which that name was most popular. If the user chooses an
invalid analysis, the program should alert them but allow them to perform another analysis.

Intuition for building tool for baby name analyzer.
        1. Download the usa_baby_names.csv using wget
        2. Read file and traverse all data of this file according to what functionality user wants.
        3. If functionality not present then print the alter message, otherwise print the result.
        4. Repeat step 2 and 3 until user wants to quit.
"""

#!wget - nc http://dgoldberg.sdsu.edu/515/usa_baby_names.csv
import csv

repeat = "yes"
print('\n')
print("Welcome to the baby name analyzer! ")

# opening file in read mode, file pointer pointing to file
with open("usa_baby_names.csv", "r") as file:
    reader = csv.reader(file)
    while repeat == "yes":
         # seek() to reset the file pointer to the first index
        file.seek(0)
        analysis = input("\nWhat analysis would you like to run (name comparison/maximum popularity)?")

        # If user entered "name comparison" then code in if-statement will be executed
        if analysis == "name comparison":
            # sum1 and sum2 are storing the total frequency of first name and second name
            sum1, sum2 = 0, 0
            first_name = input("enter first name")
            second_name = input("enter last name")
            for row in reader:
                # If name matches with first name then add the frequency in sum1
                if row[0].lower() == first_name.lower():
                    sum1 += int(row[2])
                # If name matches with second name then add the frequency in sum2
                if row[0].lower() == second_name.lower():
                    sum2 += int(row[2])

            # comparing the frequencies of both the names and printing results accordingly
            if sum1 > sum2:
                print(f"{first_name.title()} was more popular than {second_name.title()} ({sum1} to {sum2})!")

            elif sum2 > sum1:
                print(f"{second_name.title()} was more popular than {first_name.title()} ({sum2} to {sum1})!")

            else:
                print(f"{second_name}:{sum1} and {first_name}:{sum2} have equal popularity")

        # If user entered "maximum popularity" then code in elif-statement will be executed
        elif analysis == "maximum popularity":
            name = input("Enter the name to analyze")

            year = 0
            mx_popularity = 0
            for row in reader:

                if row[0].lower() == name.lower():
                    if int(row[2]) > mx_popularity:
                        mx_popularity = int(row[2])
                        year = row[1]

            print(f"\n{name.title()} was most popular in {year} with a frequency of {mx_popularity}.")

        # If user wants some other type of analysis, the letting user that this tool doesn't support other type of analysis
        else:
            print("\nSorry, that type of analysis is not supported.")

        repeat = input("Do you want to continue(yes/no)?")

# exit message
print("\nThanks for visiting.")
