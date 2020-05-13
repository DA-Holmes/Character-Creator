'''
This class is designed to create and assign character statistics.
'''

import random

class Stats:
    
    #Default stats, stat names, and stat bonuses
    def __init__(self):
        self.my_stats = [8,10,12,13,14,15]
        self.ordered_list = ['STR','DEX','CON','INT','WIS','CHA']
        self.ordered_list_variant = ['Strength','Dexterity','Constitution','Intelligence','Wisdom','Charisma']
        self.boost_list = [0,0,0,0,0,0]
        self.assigned_list = []
    
    def display_stats(self):
        print("Your stats:")
        for i in self.my_stats:
            print(i, '', end='')
        print()
    
    #For each stat, roll 4 six-sided dice and subtract the smallest from the sum 
    def roll_stats(self):      
        stats_rolled = []
        for i in range(6):
            die1 = random.randint(1,6)
            die2 = random.randint(1,6)
            die3 = random.randint(1,6)
            die4 = random.randint(1,6)
            lowest = min(die1, die2, die3, die4)
            total = die1 + die2 + die3 + die4 - lowest
            stats_rolled.append(total)
        
        #Make a list of the rolled stats
        self.my_stats = stats_rolled

    #Allow user to choose which stats values to put where
    def assign_stats(self):
        all_assigned = False
        while all_assigned == False:
            
            #Show stat values available and prompt for their decision
            for stat in self.ordered_list_variant:
                print("Remaining values:")
                for i in self.my_stats:
                    print(i, '', end='')
                print()
                print("Which value would you like to assign to ", stat, "?", sep='')
                
                #Assure their response is valid and not repeated
                assign_response_valid = False
                while assign_response_valid == False:
                    try:
                        assign_value = int(input("Value:"))
                        if assign_value in self.my_stats:
                            self.assigned_list.append(assign_value)
                            self.my_stats.remove(assign_value)
                            assign_response_valid = True
                        else:
                            print("Value must be from your list and may not be repeated.")
                    except:
                        print("Please enter a valid value.")            
                print()     
            all_assigned = True
    
    #Automate assignment for randomization
    def assign_stats_auto(self, main):
        self.assigned_list = [0,0,0,0,0,0]
        remaining = 6
        
        #Set main stat as highest
        for stat in self.ordered_list:
            if stat == main:
                main_index = self.ordered_list.index(stat)
                highest = max(self.my_stats)
                self.assigned_list[main_index] = highest
                self.my_stats.remove(highest)
                remaining -= 1
        
        #CON is always good
        if main != 'CON':
            highest = max(self.my_stats)
            self.assigned_list[2] = highest
            self.my_stats.remove(highest)
            remaining -= 1

        #Others
        #get indeces of unassigned stats
        remaining_indeces_list = []
        for i in range(6):
            if self.assigned_list[i] == 0:
                remaining_indeces_list.append(i)
                
        #Assign at random based on indeces
        while remaining > 0:
            highest = max(self.my_stats)
            index = random.choice(remaining_indeces_list)
            self.assigned_list[index] = highest
            self.my_stats.remove(highest)
            remaining_indeces_list.remove(index)
            remaining -= 1
    
    #Gather all of the relevant information and present the user with their character bio
    def results_data(self, name, race, subrace, speed, age, ch_class, base_hp, armor, shield, weapons):
        self.bio = [name,race,subrace,speed,age,ch_class,base_hp,armor,shield,weapons]
        
        #Starting health is determined by the class hit die and the constitution modifier
        con_mod = (self.assigned_list[2] - 10) // 2
        start_health = int(base_hp + con_mod)
        self.bio[6] = start_health
        
    def print_results(self):
        bio = self.bio       
        
        #Print out results
        print("This is your character bio:")
        print()
        print()
        print("Name:", bio[0])
        print("Age:", bio[4])
        if bio[2] == 'NA':
            print("Race:", bio[1])
        else:
            print("Race:", bio[2], bio[1])
        print("Class:", bio[5])
        print("Starting Health:", bio[6])
        print()
        for i in range(6):
            print(self.ordered_list[i], ": ", self.assigned_list[i], sep='')
        print()
        print("Proficiencies")
        if bio[7] == 'All':
            print("Armor: All armor types")
        elif bio[7] == 'NA':
            print("Armor: No armor types")
        else:
            print("Armor: Up to armor type", bio[7])
        print("Shield: ", end='')
        if bio[8] == 'NA':
            print("No")
        else:
            print(bio[8])
        print("Weapons: ", end='')
        if bio[9] == 'Martial':
            print("Any weapon")
        elif bio[9] == 'Simple':
            print("Simple weapons")
        else:
            print("You have a unique set of weapon proficiencies")
        print()
    
    def print_results_to_file(self, name, directory):
        
        
        title = "\\%s.txt" %(name)
        filename = "\\Character Bios" + title
        
        file_location = directory + filename
        outfile = open(file_location, 'w')
        
        bio = self.bio
        here = outfile
        
        #Print out results
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
            print(self.ordered_list[i], ": ", self.assigned_list[i], sep='', file=here)
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
            print(bio[8])
        print("Weapons: ", end='', file=here)
        if bio[9] == 'Martial':
            print("Any weapon", file=here)
        elif bio[9] == 'Simple':
            print("Simple weapons", file=here)
        else:
            print("You have a unique set of weapon proficiencies", file=here)
        print(file=here)
        
        here.close()
        