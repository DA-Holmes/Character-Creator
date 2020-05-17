'''
The D&D Character Creation Program

Author: David Holmes
Coauthor: Bryce Valley



Current Goals:
1. GUI, improve interface
2. Make Half-Elf customization function in StatBuilder (manual and automatic)


Urgent Bugs:

Things to work on:

[Mechanics]
*GUI, improve interface
*clean up code for readability
    -if needed, make functions
        >function to make lists based on a few parameters?
*half-elf (manual) - clean up stat customization option
    >Maybe create a function for both manual and auto in StatBuilder
*stat manual assignment - reiterate values and current stat after invalid response
*still printing out 'yes' after write to file question
*create function to clear out character bios folder
    >Make user triple check their answer
*reads and assigns additional race and class info for both manual and auto; very bulky
    >ajusting this may cause a need to readjust the auto result printing as well
*allow manual entry the rename option
*move results functions to a new class and try to simplify the printing


[Content]
*expand random name bank to include names from different races
*add additional info for manual vs automatic creation
*add subclasses from Xanathar's
*include skill proficiencies
*expand weapon, tool, etc. proficiency details
*race/class feats

[Big Ideas]
*Within manual, allow user to enter "Random"/"Auto" if they want to randomly choose a specific
-This could theoretically lead to a merging of the manual and automated system
    >simply setting each option to have the option of automation, and then offering an opt-in to do completely random
    >half-elf custom will be a pain, but it always is
*Set up Larger function that has subfunctions:
-Character Creation
-Character input (allowing user to enter in data from a preexisting character *insert stats manually*)
-leveling up a preset character
-export to form fillable pdf character sheet
'''

# Import Tools
import random
import os
import tkinter as tk
# import tkFont
from tkinter import ttk
from StatBuilder import *
from Information import *
from pathlib import Path
direct = os.getcwd()

checkResponse = None
window = tk.Tk()

# Yes or No Questions


def boolean(prompt):
    boolean_answered = False
    while boolean_answered == False:
        response = input(prompt)
        if response.lower() == 'yes' or response.lower() == 'y':
            answer = True
            boolean_answered = True
        elif response.lower() == 'no' or response.lower() == 'n':
            answer = False
            boolean_answered = True
        else:
            print()
            print("Please answer Yes or No.")
    return answer

def yesResponse():
    global checkResponse
    checkResponse = True
    window.quit()

def noResponse():
    global checkResponse
    checkResponse = False
    window.quit()

def main():

    # Retrieve Data from Files
    race_data = open(direct + "\\DND Data\\RaceInfo.txt", 'r')
    race_descriptions = open(direct + "\\DND Data\\RaceDescriptions.txt", 'r')
    class_data = open(direct + "\\DND Data\\ClassInfo.txt", 'r')
    class_descriptions = open(
        direct + "\\DND Data\\ClassDescriptions.txt", 'r')

    # Read Files into Lists
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
    for i in range(1, len(race_data_list)):
        if race_data_list[i][0] not in race_list:
            race_list.append(race_data_list[i][0])

    class_list = []
    for i in range(1, len(class_data_list)):
        class_list.append(class_data_list[i][0])

    race_descriptions_list = []
    for line in race_descriptions:
        stripped_line = line.strip()
        race_descriptions_list.append(stripped_line)

    class_descriptions_list = []
    for line in class_descriptions:
        stripped_line = line.strip()
        class_descriptions_list.append(stripped_line)

    '''''''''''''''
    Begin Program
    '''''''''''''''
    # accessing a global variable
    global checkResponse
    dialogColor = "#d4c7b2"
    fontsize = 16

    # Creating window for GUI
    window.title("DnD Character Creator")
    window.columnconfigure(0, weight = 1)
    window.rowconfigure(0, weight=1)

    mainframe = tk.Frame(master = window, bg = "#654321", borderwidth=2, relief=tk.RAISED)
    mainframe.grid(column = 0, row = 0, pady = 5, padx = 5, sticky = "nsew")

    mainframe.rowconfigure([x for x in range(16)], weight = 1, minsize=50)
    mainframe.columnconfigure([x for x in range(16)], weight = 1, minsize=50)

    currentDialog = tk.StringVar()
    mainDialog = tk.Message(master = mainframe, textvariable = currentDialog,
        anchor = "center", width = 800, font = ("times", fontsize), bg = dialogColor,
        justify = "left")
    mainDialog.grid(column = 0, row = 0, columnspan = 16, rowspan = 11, sticky = "nsew", padx = 10, pady = 10)

    noBut = tk.Button(master = mainframe, text = "NO", font = ("courier new", 16, "bold"), command = noResponse)
    noBut.grid(column = 2, row = 13, columnspan = 2, sticky = "nsew")
    yesBut = tk.Button(master = mainframe, text = "YES", font = ("courier new", 16, "bold"), command = yesResponse)
    yesBut.grid(column = 12, row = 13, columnspan = 2, sticky = "nsew")

    # Restart Option
    restart = True
    while restart:
        currentDialog.set("Welcome to The D&D Character Creation Program!\nWould you like assistance using this program?")

        add_info = Information()
        checkResponse = None
        window.mainloop()

        # Tutorial for More Information
        tutorial = False
        if checkResponse:
            add_info.general(currentDialog)
            tutorial = True

        '''''''''''''''''
        Automatic Generator
        '''''''''''''''''
        currentDialog.set(currentDialog.get() + "\n\nUse automatic generator?")
        window.mainloop()
        if checkResponse:
            auto_stats = Stats()
            print()

            #Race & Subrace
            auto_race = race_list[random.randint(0, len(race_list) - 1)]
            subrace_list = []
            for i in range(len(race_data_list)):
                if race_data_list[i][0] == auto_race:
                    if race_data_list[i][1] != 'NA':
                        subrace = True
                        subrace_list.append(race_data_list[i][1])
                        auto_subrace = subrace_list[random.randint(
                            0, len(subrace_list) - 1)]
                    else:
                        auto_subrace = 'NA'

            # Auto Class
            auto_class = class_list[random.randint(0, len(class_list) - 1)]
            for i in range(len(class_list)):
                if auto_class == class_list[i]:
                    class_index = i

            # Auto Roll Stats
            auto_stats.roll_stats()

            # Race Indices
            race_index = 0
            for index in range(len(race_data_list)):
                if race_data_list[index][0] == auto_race and race_data_list[index][1] == auto_subrace:
                    race_index = index
            rec_age = int(race_data_list[race_index][10])
            speed = race_data_list[race_index][8]

            # Race Bonuses (Half-Elves Special)
            if auto_race != 'Half-Elf':
                for i in range(6):
                    boost = int(race_data_list[race_index][i + 2])
                    auto_stats.boost_list[i] = boost
            else:
                auto_stats.boost_list[5] = 2

            # Assigning Class Data
            main_stat = class_data_list[class_index + 1][1]
            main_stat_index = -1
            for i in range(6):
                if main_stat == auto_stats.ordered_list[i]:
                    main_stat_index = i
            armor = class_data_list[class_index + 1][5]
            shield = class_data_list[class_index + 1][6]
            weapons = class_data_list[class_index + 1][7]
            base_hp = int(class_data_list[class_index + 1][2])

            # Hill Dwarf Extra Health
            if race_index == 1:
                base_hp += 1

            # Auto Age & Name
            age = random.randint(18, round(.6 * rec_age))
            name_list = ['Jane Doe', 'John Doe']
            name = random.choice(name_list)

            # Auto Stats
            print("Your primary stat is ", main_stat,
                  " and your rolled stats are: ", auto_stats.my_stats, "", sep='')
            currentDialog.set("Your primary stat is " + str(main_stat) +
                  " and your rolled stats are: \n" + str(auto_stats.my_stats))
            auto_stats.assign_stats_auto(main_stat)
            print()

            # Race Bonuses
            for i in range(6):
                auto_stats.assigned_list[i] += auto_stats.boost_list[i]

            # Half-Elf Optimization
            if auto_race == "Half-Elf":
                remaining_bonus = 2
                copy_list = auto_stats.assigned_list

                while remaining_bonus > 0:
                    main = False
                    con = False

                    # Prioritize Main Stat
                    if (auto_stats.assigned_list[main_stat_index] % 2) == 1 and main_stat != 'CHA':
                        auto_stats.assigned_list[main_stat_index] += 1
                        main = True
                        remaining_bonus -= 1

                    # Next is CON
                    if (auto_stats.assigned_list[2] % 2) == 1:
                        auto_stats.assigned_list[2] += 1
                        con = True
                        remaining_bonus -= 1

                    # Remaining
                    if remaining_bonus > 0:

                        # Start by topping off odds
                        # Make it choose which odd at random
                        odd_list = []
                        odd_stat_index = -1
                        for i in range(5):
                            if auto_stats.assigned_list[i] % 2 == 1:
                                odd_list.append(auto_stats.assigned_list[i])
                        if len(odd_list) > 0:
                            odd_stat = max(odd_list)
                            odd_stat_index = copy_list.index(odd_stat)
                            auto_stats.assigned_list[odd_stat_index] += 1
                            remaining_bonus -= 1
                        else:

                            # Double-Check Main Stat
                            if main == False:
                                auto_stats.assigned_list[main_stat_index] += 1
                                main = True
                                remaining_bonus -= 1
                            else:

                                #Make it choose which even at random
                                # Boost Evens Last
                                even_list = []
                                for i in range(5):
                                    if i != (2 or 5 or odd_stat_index):
                                        even_list.append(
                                            auto_stats.assigned_list[i])
                                even_stat = max(even_list)
                                even_stat_index = copy_list.index(even_stat)
                                auto_stats.assigned_list[even_stat_index] += 1
                                print("Adding to evens:",
                                      auto_stats.assigned_list)
                                remaining_bonus -= 1

            # Print Automated Results
            auto_stats.results_data(name, auto_race, auto_subrace,
                                    speed, age, auto_class, base_hp, armor, shield, weapons)
            statShowcase = tk.StringVar()
            mainDialog.grid(column = 0, row = 0, columnspan = 12, rowspan = 11, sticky = "nsew", padx = 10, pady = 10)
            statDialog = tk.Message(master = mainframe, textvariable = statShowcase,
                anchor = "center", width = 200, font = ("times", fontsize), bg = "#d4c7b2",
                justify = "left")
            statDialog.grid(column = 12, row = 0, columnspan = 4, rowspan = 11, sticky = "nsew", padx = (0, 10), pady = 10)
            auto_stats.print_results(currentDialog, statShowcase)

            # Allow Name Change
            name_change = True
            while name_change == True:
                currentDialog.set(currentDialog.get() + "Would you like to change your character's name?")
                window.mainloop()
                if checkResponse:
                    currentDialog.set("Enter the new name of your character below.\nPress yes once done.")

                    nameEntry = tk.Entry(master = mainframe)
                    nameEntry.grid(column = 7, row = 13, columnspan=2, sticky = "nsew")
                    window.mainloop()

                    auto_stats.results_data(
                        nameEntry.get(), auto_race, auto_subrace, speed, age, auto_class, base_hp, armor, shield, weapons)
                    auto_stats.print_results(currentDialog, statShowcase)
                    nameEntry.grid_remove()
                else:
                    name_change = False
                print()
            final = auto_stats

        else:
            '''''''''''''''
            Manual Builder
            '''''''''''''''
            # Choose Your Race
            print()
            stat_values = Stats()
            repeat_race = True
            while repeat_race == True:
                currentDialog.set("We are going to start by choosing" + 
                    " a race from the D&D Player's Handbook.\n")
                if tutorial == True:
                    add_info.race(currentDialog)
                    for entry in race_descriptions_list:
                        print(entry)
                        currentDialog.set(currentDialog.get() + entry + "\n\n")


                # Race Options
                race_chosen = False
                while race_chosen == False:
                    print("Choose a race from the list:")
                    currentDialog.set(currentDialog.get() + "Choose a race from the list and press yes when done:")
                    selectBox = tk.Listbox(master = mainframe, height = len(race_list), selectbackground = dialogColor,
                        selectmode = "SINGLE", font = ("times", fontsize-2))

                    for i in range(len(race_list)):
                        selectBox.insert(i, race_list[i])

                    selectBox.grid(column = 7, row = 12, columnspan=2, rowspan = 3, sticky = "nsew")

                    window.mainloop()
                    if len(selectBox.curselection()) == 1:
                        my_race = race_list[selectBox.curselection()[0]]
                        race_chosen = True


                # Subrace Options
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

                # Choose Subrace
                if subrace == True:
                    currentDialog.set("The race you chose has additional subrace options!\n" +
                        "Please choose one of the following:\n\n")
                    selectBox.delete(0, selectBox.size())
                    for i in range(len(subrace_options)):
                        currentDialog.set(currentDialog.get() + "%s:\t\t%s\n" % (subrace_options[i], subrace_bonuses[i]))
                        selectBox.insert(i, subrace_options[i])
                    subrace_chosen = False
                    while subrace_chosen == False:
                        window.mainloop()
                        if len(selectBox.curselection()) == 1:
                            my_subrace = selectBox.get([selectBox.curselection()[0]])
                            subrace_chosen = True

                # Display Decision
                    currentDialog.set("You have to chosen to be a %s %s!\n\nWould you like to choose a different race?" % (my_subrace, my_race))
                elif subrace == False:
                    currentDialog.set("You have to chosen to be a %s!\n\nWould you like to choose a different race?" % (my_race))
                
                window.mainloop()
                if not checkResponse:
                    repeat_race = False

            # Choose Your Class
            repeat_class = True
            while repeat_class == True:
                selectBox.delete(0, selectBox.size())
                currentDialog.set("Next, you will choose a class for your character:\n\n")
                print("")
                if tutorial == True:
                    add_info.dnd_class(currentDialog)
                    print()
                    for entry in class_descriptions_list:
                        print(entry)
                        currentDialog.set(currentDialog.get() + entry + "\n\n")
                else:
                    # print("Choose a class from the following list:")
                    for i in range(1, len(class_data_list)):
                        if i < len(class_data_list) - 1:
                            currentDialog.set(currentDialog.get() + class_data_list[i][0] + ", ")
                        else:
                            currentDialog.set(currentDialog.get() + class_data_list[i][0])
                        selectBox.insert(i-1, class_data_list[i][0])

                # Class Options
                class_chosen = False
                while class_chosen == False:


                    window.mainloop()
                    if len(selectBox.curselection()) == 1:
                        my_class = selectBox.get([selectBox.curselection()[0]])
                        class_index = selectBox.curselection()[0]
                        class_chosen = True

                currentDialog.set("You have chosen to be a %s!\nWould you like to choose a different class?" % (my_class))
                window.mainloop()
                if not checkResponse:
                    repeat_class = False
            selectBox.grid_remove()

            # Data From Race & Class
            race_index = 0
            for index in range(len(race_data_list)):
                if race_data_list[index][0] == my_race and race_data_list[index][1] == my_subrace:
                    race_index = index
            rec_age = int(race_data_list[race_index][10])
            speed = race_data_list[race_index][8]
            main_stat = class_data_list[class_index + 1][1]
            armor = class_data_list[class_index + 1][5]
            shield = class_data_list[class_index + 1][6]
            weapons = class_data_list[class_index + 1][7]
            base_hp = int(class_data_list[class_index + 1][2])

            # Race Bonuses (Half-Elf Special)
            if my_race != 'Half-Elf':
                for i in range(6):
                    boost = int(race_data_list[race_index][i + 2])
                    stat_values.boost_list[i] = boost
            else:
                stat_values.boost_list[5] = 2

            # Hill Dwarf Extra Health
            if race_index == 1:
                base_hp += 1

            # Setting Stats
            print(
                "Now we are going to determine your character stats for Strength (STR), Dexterity (DEX),")
            print(
                "Constitution (CON), Intelligence (INT), Wisdom (WIS), and Charisma (CHA).")
            print()
            if tutorial == True:
                add_info.stats()
            print()

            # Display Defaults
            print("The default stats are:")
            for i in stat_values.my_stats:
                print(i, '', end='')
            print()
            print()

            # Roll for Stats
            if boolean("Would you like to roll for your stats? ") == True:
                stat_values.roll_stats()
            else:
                print("You have chosen the default values.")
            print()

            # Assigning Stats
            print("Now, choose which value you want for each stat.")
            print("Each value can only be used once.")
            print()
            print("The most important stat for a ",
                  my_class, " is ", main_stat, ".", sep='')
            print()
            stat_values.assign_stats()

            # Half-Elf Customization
            if my_race == 'Half-Elf':
                # Perform function for this

                print(
                    "Because you are a Half-Elf, you may add 1 to two different stats besides CHA.")

                # Choose Stats to Boost
                extra1_good = False
                while extra1_good == False:
                    extra1 = input("First stat to boost: ")
                    first = extra1.lower()
                    for i in range(len(stat_values.ordered_list)):
                        if first == stat_values.ordered_list[i].lower():
                            if first != 'cha':
                                stat_values.boost_list[i] += 1
                                extra1_good = True
                                first_index = i
                            else:
                                print("CHA already has a bonus.")
                    if extra1_good == False:
                        print("Please enter a valid stat (e.g. 'STR').")
                    print()
                extra2_good = False
                while extra2_good == False:
                    extra2 = input("Second stat to boost: ")
                    second = extra2.lower()
                    for i in range(len(stat_values.ordered_list)):
                        if second == stat_values.ordered_list[i].lower():
                            if second != 'cha' and second != first:
                                stat_values.boost_list[i] += 1
                                extra2_good = True
                            elif second == first:
                                print(
                                    stat_values.ordered_list[first_index], "already has a bonus.")
                            elif second == 'cha':
                                print("CHA already has a bonus.")
                    if extra2_good == False:
                        print("Please enter a valid stat (e.g. 'STR').")
                    print()
            # Add Stat Bonuses
            for i in range(6):
                stat_values.assigned_list[i] += stat_values.boost_list[i]

            # Choose Age
            print("Looks good! Now all you need is to set your age and choose a name!")
            print("The average lifespan of a",
                  my_race, "is", rec_age, "years.")
            print()
            age_chosen = False
            while age_chosen == False:
                try:
                    age = int(input("Your age: "))
                    if age > rec_age:
                        if boolean("You have chosen an age past your average lifespan. Are you sure? ") == True:
                            age_chosen = True
                    elif age > 0:
                        age_chosen = True
                    else:
                        print("Please enter an age above 0.")
                except:
                    print("Please enter a whole number.")
                print()

            # Choose Character Name
            name = input("What is the name of your character? ")
            print()

            # Print Results
            stat_values.results_data(
                name, my_race, my_subrace, speed, age, my_class, base_hp, armor, shield, weapons)
            stat_values.print_results()
            final = stat_values

        # Create New File for Bio
        if boolean("Would you like to write this bio into a file? ") != False:
            final.print_results_to_file(name, direct)

        # End of Program
        print()
        if boolean("Thank you for using the Character Creation Program! Would you like to start over? ") == False:
            restart = False
            print()
            print("Goodbye!")

    # Close Files
    race_data.close()
    race_descriptions.close()
    class_data.close()
    class_descriptions.close()


main()
