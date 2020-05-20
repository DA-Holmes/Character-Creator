'''
This class is designed to create and assign character statistics.
'''

import random

class Stats:

    # Default Stats, Stat Names, and Bonuses
    def __init__(self):
        self.my_stats = [15, 14, 13, 12, 10, 8]
        self.ordered_list = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
        self.ordered_list_variant = [
            'Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
        self.boost_list = [0, 0, 0, 0, 0, 0]
        self.assigned_list = []

    # Show Current Base Stats
    def display_stats(self):
        print("Your stats:")
        for i in self.my_stats:
            print(i, '', end='')
        print()

    # Roll 4d6 & Subtract Lowest
    def roll_stats(self):
        stats_rolled = []
        for i in range(6):
            die1 = random.randint(1, 6)
            die2 = random.randint(1, 6)
            die3 = random.randint(1, 6)
            die4 = random.randint(1, 6)
            lowest = min(die1, die2, die3, die4)
            total = die1 + die2 + die3 + die4 - lowest
            stats_rolled.append(total)

        # Replace Default Stats
        self.my_stats = stats_rolled

    # Manual Stat Assignment
    def assign_stats(self, stringVar, prefix, listbox, window):
        copy_list = self.my_stats
        remaining = []
        for i in range(6):
            remaining.append(max(copy_list))
            copy_list.remove(max(copy_list))
            listbox.insert(i, remaining[i])

        # Display Available Stats and Assign Next
        for stat in self.ordered_list_variant:
            statText = "Remaining values: "
            for i in remaining:
                statText += "%d " % i
            statText += "\n\nWhich value would you like to assign to %s?" % stat
            stringVar.set(prefix + statText)
            
            while len(listbox.curselection()) != 1:
                window.mainloop()

            assign_value = listbox.curselection()[0]
            self.assigned_list.append(listbox.get(assign_value))
            remaining.remove(listbox.get(assign_value))
            listbox.delete(assign_value)

    # Automated Stat Assignment
    def assign_stats_auto(self, main):
        self.assigned_list = [0, 0, 0, 0, 0, 0]
        remaining = 6

        # Prioritize Main Stat
        for stat in self.ordered_list:
            if stat == main:
                main_index = self.ordered_list.index(stat)
                highest = max(self.my_stats)
                self.assigned_list[main_index] = highest
                self.my_stats.remove(highest)
                remaining -= 1

        #Constitution is Handy
        if main != 'CON':
            highest = max(self.my_stats)
            self.assigned_list[2] = highest
            self.my_stats.remove(highest)
            remaining -= 1

        # Randomly Assign Remaining Stats
        remaining_indeces_list = []
        for i in range(6):
            if self.assigned_list[i] == 0:
                remaining_indeces_list.append(i)
        while remaining > 0:
            highest = max(self.my_stats)
            index = random.choice(remaining_indeces_list)
            self.assigned_list[index] = highest
            self.my_stats.remove(highest)
            remaining_indeces_list.remove(index)
            remaining -= 1

    # Gather Relevant Character Data
    def results_data(self, name, race, subrace, speed, age, ch_class, base_hp, armor, shield, weapons):
        self.bio = [name, race, subrace, speed, age,
                    ch_class, base_hp, armor, shield, weapons]

        # Starting Health
        con_mod = (self.assigned_list[2] - 10) // 2
        self.bio[6] = int(base_hp + con_mod)

    # Printing to Interface
    def print_results(self, stringVar, statBlock):
        bio = self.bio
        finalString = "This is your character bio:\n\nName:\t\t%s \nAge:\t\t%d \n" % (bio[0], bio[4])
        statString = "STATS:\n\n"

        if bio[2] == 'NA':
            finalString += "Race:\t\t%s \n" % bio[1]
        else:
            finalString += "Race:\t\t%s %s \n" % (bio[2], bio[1])
        finalString += "Class:\t\t%s \n" % bio[5]
        finalString += "Starting Health:\t%d \n\n" % bio[6]
        for i in range(6):
            statString += "%s:\t%d\n" % (self.ordered_list[i], self.assigned_list[i])
        finalString += "\nProficiencies\n"
        if bio[7] == 'All':
            finalString += "Armor: All armor types"
        elif bio[7] == 'NA':
            finalString += "Armor: No armor types"
        else:
            finalString += "Armor: Up to armor type %s" % bio[7]
        finalString += "\nShield: "
        if bio[8] == 'NA':
            finalString += "No"
        else:
            finalString += "Yes"
        finalString += "\nWeapons: "
        if bio[9] == 'Martial':
            finalString += "Any weapon"
        elif bio[9] == 'Simple':
            finalString += "Simple weapons"
        else:
            finalString += "You have a unique set of weapon proficiencies"
        stringVar.set(finalString)
        statBlock.set(statString)

    # Printing to File
    def print_results_to_file(self, name, directory):
        file_location = directory + "\\Character Bios\\%s.txt" % (name)
        outfile = open(file_location, 'w')
        bio = self.bio
        here = outfile
        print("Name:", bio[0], file=here)
        print("Age:", bio[4], file=here)
        if bio[2] == 'NA':
            print("Race:", bio[1], file=here)
        else:
            print("Race:", bio[2], bio[1], file=here)
        print("Class:", bio[5], file=here)
        print("Starting Health:", bio[6], file=here)
        print(file=here)
        for i in range(6):
            print(self.ordered_list[i], ": ",
                  self.assigned_list[i], sep='', file=here)
        print(file=here)
        print("Proficiencies", file=here)
        if bio[7] == 'All':
            print("Armor: All armor types", file=here)
        elif bio[7] == 'NA':
            print("Armor: No armor types", file=here)
        else:
            print("Armor: Up to armor type", bio[7], file=here)
        print("Shield: ", end='', file=here)
        if bio[8] == 'NA':
            print("No", file=here)
        else:
            print(bio[8], file=here)
        print("Weapons: ", end='', file=here)
        if bio[9] == 'Martial':
            print("Any weapon", file=here)
        elif bio[9] == 'Simple':
            print("Simple weapons", file=here)
        else:
            print("You have a unique set of weapon proficiencies", file=here)
        here.close()
