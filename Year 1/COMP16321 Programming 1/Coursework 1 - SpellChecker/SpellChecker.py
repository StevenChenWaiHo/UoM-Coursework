import os
from datetime import datetime
from difflib import SequenceMatcher
import time

width = 78
height = 22


def displayCurrentSentence(finalSentence):
    return "================================================================================\nYour Sentence(s):\n\n" + finalSentence + "\n================================================================================\n"


def spellCheck(userSentence):
    startTime = datetime.now()
    statistics = [0, 0, 0, 0, 0]
    # 0: total number of word
    # 1: Correct
    # 2: Incorrect
    # 3: Add to Dict
    # 4: Accepting Suggestion
    dictionary = open("EnglishWords.txt", "r")
    words = dictionary.readlines()  # Create a list for all words in dictionary
    suggestions = []  # Create suggestion words list
    corrSentence = ""
    word = ""
    flag = 0
    corr_index = 0
    for user_index in range(len(userSentence)):  # Check for all char in user Input
        if not userSentence[user_index].isalpha():
            if flag == 1:  # Previous char is alpha
                maxR = 0
                for w in words:  # Compare all words in dictionary
                    ratio = SequenceMatcher(None, word.lower(), w.strip()).ratio()
                    if ratio > maxR:  # A more probable word
                        maxR = ratio
                        suggestions.clear()
                        suggestions.append(w.strip())
                    elif ratio > maxR:
                        suggestions.append(w.strip())
                    elif ratio == maxR:  # Two words that have same ratio
                        suggestions.append(w.strip())
                os.system('clear')
                winText = displayCurrentSentence(corrSentence)
                print(winText)
                if maxR != 1:  # Word does not match dictionary
                    corr_index += len(word) + 1
                    winText += "Spelling Mistake for \"" + word + "\"?"
                    selection = optionSelect(winText,
                                             {1: "Ignore", 2: "Mark", 3: "Add to Dictionary", 4: "Suggestions"})
                    if selection == 1:  # Ignore
                        statistics[2] += 1  # Number of Wrong Words + 1
                        corrSentence = corrSentence[:corr_index] + word + userSentence[user_index] + corrSentence[
                                                                                                     corr_index + 1:]
                        corr_index += len(word) + 1
                    if selection == 2:  # Mark
                        statistics[2] += 1  # Number of Wrong Words + 1
                        corrSentence = corrSentence[:corr_index] + "?" + word + "?" + userSentence[
                            user_index] + corrSentence[corr_index + 1:]
                        corr_index += len(word) + 3
                    if selection == 3:  # add word to dict
                        statistics[1] += 1  # Number of Correct Words + 1
                        statistics[3] += 1  # Number of Add Dict + 1
                        dictionary.close()
                        dictionary = open("EnglishWords.txt", "a")
                        dictionary.write("\n" + word)
                        dictionary.close()
                        dictionary = open("EnglishWords.txt", "r")
                        words = dictionary.readlines()  # Lookup New Words
                        corrSentence = corrSentence[:corr_index] + word + userSentence[user_index] + corrSentence[
                                                                                                     corr_index + 1:]
                        os.system('clear')
                        print(winText, "\n\nWord \"", word, "\" added to Dictionary")
                        time.sleep(2)
                        corr_index += len(word) + 1
                        pass
                    if selection == 4:  # Suggestion
                        winText += "\n\nMay be you mean {" + ', '.join(map(str, suggestions)) + "} ?"
                        suggestionList = {-1: "Reject Suggestion"}
                        for j in range(len(suggestions)):  # Add suggestion to Option List
                            suggestionList[j] = suggestions[j]
                        selectedOption = optionSelect(winText, suggestionList)  # Ask for selection
                        if selectedOption != -1:  # Use Suggestion
                            statistics[1] += 1  # Number of Correct Word + 1
                            statistics[4] += 1  # Number of Suggestions + 1
                            selectedSuggestion = suggestions[selectedOption]
                            corrSentence = corrSentence[:corr_index] + selectedSuggestion + userSentence[
                                user_index] + corrSentence[corr_index + 1:]
                            corr_index += len(selectedSuggestion) + 1
                        else:  # Reject Suggestion
                            statistics[2] += 1  # Number of Wrong Word + 1
                            # if optionSelect(windowText,{1: "Use Original", 2: "Type it Yourself"}) == 2:
                            #    word = input("Correction: " + word + "----> ")
                            corrSentence = corrSentence[:corr_index] + word + userSentence[user_index] + corrSentence[
                                                                                                         corr_index + 1:]
                            corr_index += len(word) + 1
                else:  # Word match dictionary
                    statistics[1] += 1  # Number of Correct Word + 1
                    corrSentence = corrSentence[:corr_index] + word + userSentence[user_index] + corrSentence[
                                                                                                 corr_index + 1:]
                    corr_index += len(word) + 1
                statistics[0] += 1  # Number of Word + 1
                os.system('clear')
                print(displayCurrentSentence(corrSentence))
            else:  # previous char is not alpha
                corrSentence = corrSentence[:corr_index] + userSentence[user_index] + corrSentence[corr_index + 1:]
                corr_index += 1
            word = ""
            flag = 0
        else:
            word = word + userSentence[user_index]
            flag = 1
    os.system('clear')  # Final Sentence(s) & Statistics
    output = "\n================================================================================\n\nYour Sentence(s):\n\n"
    output = output + corrSentence
    output = output + "\n\n================================================================================\n"
    output = output + "\nTotal Number of Words: " + str(statistics[0]) + "\nNumber of Correct Words: " + str(
        statistics[1])
    output = output + "\nNumber of Incorrect Words: " + str(
        statistics[2]) + "\nNumber of Words Added to Dictionary: " + str(statistics[3])
    output = output + "\nNumber of accepting Suggestion Words: " + str(statistics[4]) + "\nInput Time: "
    output = output + startTime.strftime("%d/%m/%Y %H:%M:%S")
    output = output + "\nTime Spent: " + str(datetime.now() - startTime)
    return output


def optionSelect(winText, options):
    selection = -999
    if selection in options.keys():  # Ensure No options is -999
        quit("-999 cannot be a key")
    invalid = 0
    while not (selection in options.keys()):
        os.system('clear')
        print(winText)
        print("================================================================================\n")  # Print Option List
        for i, option in options.items():
            temp = "\t\t\t      "
            if i < 0:
                temp = "\t\t\t     "
            print(temp, i, ": ", option)
        print("\n________________________________________________________________________________")
        if invalid == 1 and not (selection in options.keys()):
            print("\t\t\t       Invalid Input")
        invalid = 1
        print("Input (", ('/'.join(map(str, options.keys()))), sep="", end="")
        selection = input("): ")
        if selection.lstrip('-').isdigit():
            selection = int(selection)
    return selection


def menu():
    os.system('clear')
    winText = "\t\t\t   __  __                  \n\t\t\t  |  \/  | ___ _ __  _   _ \n\t\t\t  | |\/| |/ _ \ '_ \| | | |\n\t\t\t  | |  | |  __/ | | | |_| |\n\t\t\t  |_|  |_|\___|_| |_|\__,_|"
    menuOptions = {1: "Sentence", 2: "File", 3: "Display Window Size", 0: "Quit"}
    return optionSelect(winText, menuOptions)


def Quit():
    os.system('clear')
    print("Have a good day, Bye")
    exit()


def displayWindowSize():
    global width, height
    os.system('clear')
    print('┌', end='')
    for w in range(width):
        print('─', end='')
    print('┐', end='')
    for h in range(height):
        print('|', end='')
        for w in range(width):
            print(' ', end='')
        print('|', end='')
    print('└', end='')
    print("Resize Your Window According to the Boarder", end="")
    for w in range(width - 43):
        print('─', end='')
    print('┘', end='')
    input("Press Any Enter to Quit")


def resizeWindow():
    selection = optionSelect("Window Size ", {0: "Display Window Size", -1: "Menu"})
    while selection != -1:
        displayWindowSize()
        selection = optionSelect("Window Size ", {0: "Display Window Size", -1: "Menu"})
    return selection


def sentence():
    os.system('clear')
    winText = spellCheck(input("Input Sentence: ") + " ")
    return optionSelect(winText, {1: "Try Again", 2: "File", -1: "Menu", 0: "Quit"})


def file():
    os.system('clear')
    fileName = input("Input Filename(Exclude .txt): ") + ".txt"
    while not os.path.isfile(fileName):
        os.system('clear')
        print("Invalid Input")
        fileName = input("Input Filename(Exclude .txt): ") + ".txt"
    inputFile = open(fileName, "r+")
    fileData = (spellCheck(inputFile.read() + " "))
    outputFile = open(input("SPELL CHECKED\nName for the New File(Exclude .txt): ") + ".txt", "a")
    outputFile.write(fileData)
    outputFile.close()
    winText = "File Created"
    return optionSelect(winText, {1: "Sentence", 2: "Try Again", -1: "Menu", 0: "Quit"})


choice = -1
while True:
    if choice == -1:
        choice = menu()
    if choice == 0:
        Quit()
    if choice == 1:
        choice = sentence()
    if choice == 2:
        choice = file()
    if choice == 3:
        choice = resizeWindow()
