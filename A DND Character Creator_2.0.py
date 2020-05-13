'''
The D&D Character Creation Program

Author: David Holmes
Coauthor: Bryce Valley



Urgent Bugs:
-error after trying to use "/" in character name; use a try-except block to override possible input error

Goals:

[Mechanics]
*Simplify all the additional info into one opt-in tutorial question
*expand random name bank to include names from different races
*GUI, improve interface
*clean up code for readability
    -if needed, make functions
        >function to make lists based on a few parameters?
*update boolean so it takes arguements for the different possible answers (default set to yes/no)
-allows us to ask "manual or automatic"
*half-elf (manual) - clean up stat customization option
*fix weird line spacing with boolean ouptuts
    -fix line spacing in general
    -line spacing when printing descriptions is off (race but not class)
*figure out why it prints "yes" after printing to file question
*repeat question when retrieving boolean response

[Content]
*add additional info for manual vs automatic creation
*add subclasses from Xanathar's
*include skill proficiencies
*remove "(d)" from text file names
*expand weapon, tool, etc. proficiency details
*race/class feats

[General]
*Have fun
*Use characters made from the program

[Big Ideas]
*Set up Larger function that has subfunctions:
-Character Creation
-Character input (allowing user to enter in data from a preexisting character *insert stats manually*)
-leveling up a preset character
'''

#Import the good stuff
import random
import os
from StatBuilder import *
from Information import *
from pathlib import Path
direct = os.getcwd()

###
###Replaced with tutorial option
###
def helper(topic):
    prompt = "Would you like to learn more about " + topic + "? "
    response = input(prompt)
    return response

#Makes sure the user responds competently
def boolean(response):
    boolean_answered = False
    while boolean_answered == False:
        if response.lower() == ('yes' or 'y'):
            answer = True
            boolean_answered = True
        elif response.lower() == ('no' or 'n'):
            answer = False
            boolean_answered = True
        else:
            print()
            response = input("Yes or No: ")
    return answer

def main():

    #Get data from text files
    race_data = open(direct + "\DND Data\RaceInfo(d).txt", 'r')
    race_descriptions = open(direct + "\DND Data\RaceDescriptions(d).txt", 'r')
    class_data = open(direct + "\DND Data\ClassInfo(d).txt", 'r')
    class_descriptions = open(direct + "\DND Data\ClassDescriptions(d).txt", 'r')

    #Read files into lists
    race_data_list = []
    for line in race_data:
        stripped_line = line.strip()
        entry_list = stripped_line.split(',')
        race_data_list.append(entry_list)

    class_data_list = []
    for line in class_data:
        stripped_line = line.strip()
        entry_list = stripped_line.split(',')
        class_data_list.append(entry_list)

    race_list = []
    for i in range(1,len(race_data_list)):
        if race_data_list[i][0] not in race_list:
            race_list.append(race_data_list[i][0])

    class_list = []
    for i in range(1,len(class_data_list)):
        class_list.append(class_data_list[i][0])

    race_descriptions_list = []
    for line in race_descriptions:
        stripped_line = line.strip()
        race_descriptions_list.append(stripped_line)

    class_descriptions_list = []
    for line in class_descriptions:
        stripped_line = line.strip()
        class_descriptions_list.append(stripped_line)


    '''''''''''''''''''''''''''''''''
    Begin constructing your character
    '''''''''''''''''''''''''''''''''
    #Option to restart the program
    restart = True
    while restart == True:
        for i in range(5):
            print()
        print("Welcome to The D&D Character Creation Program!")
        print()

        #Opt-In for Tutorial
        tutorial_prompt = input("Would you like assistance using this program? ")
        if boolean(tutorial_prompt) == True:
            tutorial = True
        else:
            tutorial = False
        print()

        #Randomization Station
        if tutorial == True:

#add_info for auto v manual

            print("Here's some info about manual v. automatic.")
            print()
        random_response = input("Create random character? ")
        print()

#Eventually change to 'manual or automatic'?

        if boolean(random_response) == True:

            '''''''''''''''''
            Automated Builder
            '''''''''''''''''
            auto_stats = Stats()

            #Race & Subrace
            auto_race = race_list[random.randint(0,len(race_list)-1)]

            subrace_list = []
            for i in range(len(race_data_list)):
                if race_data_list[i][0] == auto_race:
                    if race_data_list[i][1] != 'NA':
                        subrace = True
                        subrace_list.append(race_data_list[i][1])
                        auto_subrace = subrace_list[random.randint(0,len(subrace_list)-1)]
                    else:
                        auto_subrace = 'NA'

            #Auto Class
            auto_class = class_list[random.randint(0,len(class_list)-1)]
            for i in range(len(class_list)):
                if auto_class == class_list[i]:
                    class_index = i

            #Auto Roll Stats
            auto_stats.roll_stats()

            #Race Indices
            race_index = 0
            for index in range(len(race_data_list)):
                if race_data_list[index][0] == auto_race and race_data_list[index][1] == auto_subrace:
                    race_index = index
            rec_age = int(race_data_list[race_index][10])
            speed = race_data_list[race_index][8]

            #Race Bonuses (Half-Elves Special)
            if auto_race != 'Half-Elf':
                for i in range(6):
                    boost = int(race_data_list[race_index][i+2])
                    auto_stats.boost_list[i] = boost
            else:
                auto_stats.boost_list[5] = 2

            #Assigning Class Data
            main_stat = class_data_list[class_index+1][1]
            main_stat_index = -1
            for i in range(6):
                if main_stat == auto_stats.ordered_list[i]:
                    main_stat_index = i
            armor = class_data_list[class_index+1][5]
            shield = class_data_list[class_index+1][6]
            weapons = class_data_list[class_index+1][7]
            base_hp = int(class_data_list[class_index+1][2])

            #Hill Dwarf Extra Health
            if race_index == 1:
                base_hp +=1

            #Auto Age & Name
            age = random.randint(18,round(.6*rec_age))
            name_list = ['Jane Doe', 'John Doe']
            name = random.choice(name_list)

            #Auto Stats
            auto_stats.assign_stats_auto(main_stat)
            print("(Your primary stat is ", main_stat, " and your rolled stats are: ", auto_stats.assigned_list, ")", sep='')
            print()

            #Race bonuses
            for i in range(6):
                auto_stats.assigned_list[i] += auto_stats.boost_list[i]

            #Half-Elf optimization
            if auto_race == "Half-Elf":
                remaining_bonus = 2
                copy_list = auto_stats.assigned_list

                while remaining_bonus > 0:
                    main = False
                    con = False

                    #Prioritize main stat
                    if (auto_stats.assigned_list[main_stat_index] % 2) == 1 and main_stat != 'CHA':
                        auto_stats.assigned_list[main_stat_index] += 1
                        main = True
                        remaining_bonus -= 1

                    #Next is CON
                    if (auto_stats.assigned_list[2] % 2) == 1:
                        auto_stats.assigned_list[2] += 1
                        con = True
                        remaining_bonus -= 1

                    #Remaining
                    if remaining_bonus > 0:

                        #Start by topping off odds

#Make it choose which odd at random#

                        odd_list = []
                        odd_stat_index = -1
                        for i in range(5):
                            if auto_stats.assigned_list[i] % 2 == 1:
                                odd_list.append(auto_stats.assigned_list[i])
                        if len(odd_list) > 0:
                            odd_stat = max(odd_list)
                            odd_stat_index = copy_list.index(odd_stat)
                            auto_stats.assigned_list[odd_stat_index] += 1
                            #print("Topping odds:", auto_stats.assigned_list)
                            remaining_bonus -= 1
                        else:

                            #If no odds are left, add to main stat if not already done
                            if main == False:
                                auto_stats.assigned_list[main_stat_index] += 1
                                main = True
                                remaining_bonus -= 1
                                #print("even more main:", auto_stats.assigned_list)
                            else:

#Make it choose which even at random#

                                #Finally boost evens if no other option
                                even_list = []
                                for i in range(5):
                                    if i != (2 or 5 or odd_stat_index):
                                        even_list.append(auto_stats.assigned_list[i])
                                even_stat = max(even_list)
                                even_stat_index = copy_list.index(even_stat)
                                auto_stats.assigned_list[even_stat_index] += 1
                                print("Adding to evens:", auto_stats.assigned_list)
                                remaining_bonus -= 1

            #Print Automated Results
            auto_stats.results_data(name, auto_race, auto_subrace, speed, age, auto_class, base_hp, armor, shield, weapons)
            auto_stats.print_results()

            name_change = True
            while name_change == True:
                name_response = input("Would you like to change your character name? ")
                if boolean(name_response) == True:
                    print()
                    name = input("What is the name of your character? ")
                    auto_stats.results_data(name, auto_race, auto_subrace, speed, age, auto_class, base_hp, armor, shield, weapons)
                    auto_stats.print_results()
                else:
                    name_change = False
                print()
            final = auto_stats



            '''''''''''''''
            Manual Builder
            '''''''''''''''
        else:
            stat_values = Stats()
            add_info = Information()

            '''''''''''''''''
            Choose Your Race
            '''''''''''''''''
            #Include option to choose a different race
            repeat_race = True
            while repeat_race == True:
                print("We are going to start by choosing a race from the D&D Player's Handbook.")

                #Optional info about the races
                #race_info = helper('races')
                if tutorial == True:
                    add_info.race()
                    print()
                    for entry in race_descriptions_list:
                        print(entry)
                        print()

                #Provide condensed list for user's decision
                race_chosen = False
                while race_chosen == False:
                    print("Choose a race from the following list:")
                    for i in range(len(race_list)):
                        if i < len(race_list)-1:
                            print(race_list[i], ', ', sep='', end='')
                        else:
                            print(race_list[i])
                    print()

                    #Make sure the user chooses a valid option
                    my_race = input("My race: ")
                    for race in race_list:
                        if my_race.lower() == race.lower():
                            my_race = race
                            race_chosen = True
                    if race_chosen == False:
                        print("Try again.")

                #Does the race have a subrace?
                subrace = False
                subrace_options = []
                subrace_bonuses = []
                for i in range(len(race_data_list)):
                    if race_data_list[i][0] == my_race:
                        if race_data_list[i][1] != 'NA':
                            subrace = True
                            subrace_options.append(race_data_list[i][1])
                            subrace_bonuses.append(race_data_list[i][11])
                        else:
                            my_subrace = 'NA'

                #Choose a subrace if available
                if subrace == True:
                    print()
                    print("The race you chose has additional subrace options!")
                    subrace_chosen = False
                    while subrace_chosen == False:
                        print("Please choose one of the following:")
                        for i in range(len(subrace_options)):
                            print(subrace_options[i], ": ", subrace_bonuses[i], sep='')
                        print()
                        my_subrace = input("My subrace: ")

                        #Check for valid response
                        for subrace in subrace_options:
                            if my_subrace[:4].lower() == subrace[:4].lower():
                                my_subrace = subrace
                                subrace_chosen = True
                        if subrace_chosen == False:
                            print("Try again.")

                #Display their choice
                    print("You have chosen to be a ", my_subrace, " ", my_race, "!", sep='')
                elif subrace == False:
                    print("You have chosen to be a ", my_race, "!", sep='')
                print()

                #Redo option
                race_response = input("Would you like to choose a different race? ")
                if boolean(race_response) == False:
                    repeat_race = False
                print()


            '''''''''''''''''
            Choose Your Class
            '''''''''''''''''
            #Include option to choose a different class
            repeat_class = True
            while repeat_class == True:
                print("Next, you will choose a class for your character.")

                #Optional info about the classes
                #class_info = helper('classes')
                if tutorial == True:
                    add_info.dnd_class()
                    print()
                    for entry in class_descriptions_list:
                        print(entry)
                print()

                #Provide condensed list for user's decision
                class_chosen = False
                while class_chosen == False:
                    print("Choose a class from the following list:")
                    for i in range(1,len(class_data_list)):
                        if i < len(class_data_list)-1:
                            print(class_data_list[i][0], ', ', sep='', end='')
                        else:
                            print(class_data_list[i][0])
                    print()

                    #Make sure the user chooses a valid option
                    my_class = input("My class: ")
                    for entry in class_list:
                        if my_class.lower() == entry.lower():
                            my_class = entry
                            class_index = class_list.index(entry)
                            class_chosen = True
                    if class_chosen == False:
                        print("Try again.")

                #Display their decision
                print("You have chosen to be a ", my_class, "!", sep='')
                print()

                #Redo option
                class_response = input("Would you like to choose a different class? ")
                if boolean(class_response) == False:
                    repeat_class = False
                print()


            #Global data:

            #Index of race on compiled list
            race_index = 0
            for index in range(len(race_data_list)):
                if race_data_list[index][0] == my_race and race_data_list[index][1] == my_subrace:
                    race_index = index
            rec_age = int(race_data_list[race_index][10])
            speed = race_data_list[race_index][8]

            #Race Bonuses; half-elf has different options for its bonuses
            if my_race != 'Half-Elf':
                for i in range(6):
                    boost = int(race_data_list[race_index][i+2])
                    stat_values.boost_list[i] = boost
            else:
                stat_values.boost_list[5] = 2

            #Sorting class data
            main_stat = class_data_list[class_index+1][1]
            armor = class_data_list[class_index+1][5]
            shield = class_data_list[class_index+1][6]
            weapons = class_data_list[class_index+1][7]
            base_hp = int(class_data_list[class_index+1][2])

            #Hill Dwarves get an extra hit point
            if race_index == 1:
                base_hp +=1


            '''''''''''''''''''''
            Setting Up Your Stats
            '''''''''''''''''''''
            print("Now we are going to determine your character stats for Strength (STR), Dexterity (DEX),")
            print("Constitution (CON), Intelligence (INT), Wisdom (WIS), and Charisma (CHA).")

            #Optional info on stats
            #stat_info = helper('stats')
            if tutorial == True:
                add_info.stats()
            print()

            #Display the default
            print("The default stats are:")
            for i in stat_values.my_stats:
                print(i, '', end='')
            print()
            print()

            #Option to roll for stats and replace the default values
            roll_response = input("Would you like to roll for your stats? ")
            if boolean(roll_response) == True:
                print()
                stat_values.roll_stats()
            else:
                print("You have chosen the default values.")
            print()

            #Assigning stats
            print("Now, choose which value you want for each stat.")
            print("Each value can only be used once.")
            print()
            print("The most important stat for a ", my_class, " is ", main_stat, ".", sep='')
            print()
            stat_values.assign_stats()

            #Half-Elves choose which stats to boost
            if my_race == 'Half-Elf':
                print("Because you are a Half-Elf, you may add 1 to two different stats besides CHA.")

                #Choose two stats from the list that are not already boosted.
                extra1_good = False
                while extra1_good == False:
                    extra1 = input("First stat to boost: ")
                    first = extra1.lower()
                    for i in range(len(stat_values.ordered_list)):
                        if  first == stat_values.ordered_list[i].lower():
                            if first != 'cha':
                                stat_values.boost_list[i] += 1
                                extra1_good = True
                            else:
                                print("Charisma already has a bonus")
                    if extra1_good == False:
                        print("Please enter a valid stat (e.g. 'STR').")
                    print()

                extra2_good = False
                while extra2_good == False:
                    extra2 = input("Second stat to boost: ")
                    second = extra2.lower()
                    for i in range(len(stat_values.ordered_list)):
                        if  second == stat_values.ordered_list[i].lower():
                            if second != 'cha' and second != first:
                                stat_values.boost_list[i] += 1
                                extra2_good = True
                            else:
                                print("Has to be a different stat.")
                    if extra2_good == False:
                        print("Please enter a valid stat (e.g. 'STR').")
                    print()

            #Add bonuses to stats
            for i in range(6):
                stat_values.assigned_list[i] += stat_values.boost_list[i]

            '''''''''''''''''''''''''''
            Choose Your Age and Name
            '''''''''''''''''''''''''''
            print("Looks good! Now all you need is to set your age and choose a name!")
            print("The average lifespan of a", my_race, "is", rec_age, "years.")
            print()

            age_chosen = False
            while age_chosen == False:

                #Assures the age input is valid
                #Does allow age over the average lifespan to encourage creativity
                try:
                    age = int(input("Your age: "))
                    if age > rec_age:
                        age_response = input("You have chosen an age past your average lifespan. Are you sure? ")
                        if boolean(age_response) == True:
                            age_chosen = True
                    elif age > 0:
                        age_chosen = True
                    else:
                        print("Please enter an age above 0.")
                except:
                    print("Please enter a whole number.")
                print()
            name = input("What is the name of your character? ")
            print()


            '''''''''''
            The Results
            '''''''''''
            stat_values.results_data(name, my_race, my_subrace, speed, age, my_class, base_hp, armor, shield, weapons)
            stat_values.print_results()
            final = stat_values
        '''''''''
        The End
        '''''''''

        new_file_response = input("Would you like to write this bio into a file? ")
        if boolean(new_file_response) == True:

#For some reason pringtng out "Yes" is user answers yes here, but nowhere else

            final.print_results_to_file(name, direct)

        print()
        restart_response = input("Thank you for using the Character Creation Program! Would you like to start over? ")
        if boolean(restart_response) == False:
            restart = False
            print()
            print("Goodbye!")

    #Close text files
    race_data.close()
    race_descriptions.close()
    class_data.close()
    class_descriptions.close()

main()
