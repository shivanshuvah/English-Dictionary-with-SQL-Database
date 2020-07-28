import mysql.connector
from difflib import get_close_matches


con = mysql.connector.connect(user = "ardit700_student", password = "ardit700_student", host="108.167.140.122", database = "ardit700_pm1database")

cursor = con.cursor()

def translate(word):
    word = word.lower() # convert to lower case for scenarios like dELhi
    query = "SELECT DEFINITION FROM Dictionary WHERE Expression = '{}' OR Expression = '{}' OR Expression = '{}' ".format(word.lower(),word.title(),word.upper()) 
    #lower for random cases, title for city names, upper for abbreviations
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result)>0:
        return result
    else: # if no result is returned, try for similar words
        cursor.execute("select Expression from Dictionary") 
        result = cursor.fetchall()
        all_words_tuple = sum(result,()) # consolidate the list of tuples into a single tuple of all words
        word_close=get_close_matches(word, all_words_tuple)[0]  # check if a similar word exists
        if len(word_close)>0:
            choice = input("I found your illogical word closest to {}. Type Y for yes and N for no: ".format(word_close))
            if choice == 'Y' :
                cursor.execute("SELECT DEFINITION FROM Dictionary WHERE Expression = '{}'".format(word_close))
                return cursor.fetchall()
            elif choice == 'N':
                return "Hard luck! Please do no invent words of your own!"
            else:
                return "invalid choice" 

input_word = input("Here to learn something? Shoot :  ") #program main execution---user input
output = translate(input_word)
if type(output)==list: # formatting the output in case of multiple definitions
    for definition in output:
        print(definition[0])
else:
    print(output) # prit the error string
