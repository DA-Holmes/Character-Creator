'''
Used to quickly retrieve background features (not main feature). Still need to work with equipment choices.
'''
import os
direct = os.getcwd()
class BackgroundInfo:

    def __init__(self, background):
        self.background = background
        file = open(direct + "\\DND Data\\Background_Concrete.txt", 'r')

        all_backgrounds = []
        for line in file:
            all_backgrounds.append(line.strip().split(';'))
        all_backgrounds.remove(all_backgrounds[0])

        for entry in all_backgrounds:
            if entry[0].lower() == self.background.lower():
                my_info = entry


        self.skills    = my_info[1].split(',')
        self.tools     = my_info[2].split(',')
        self.languages = my_info[3]
        self.equipment = my_info[4].split('&')


    def display(self):
        print("Background features for ", self.background, ':', sep='')
        print()
        print("Skill Proficiencies: ", self.skills[0], ',', self.skills[1], sep='')
        if self.tools != 'NA':
            print("Tool Proficiencies:", end='')
            if len(self.tools) == 1:
                print(self.tools[0])
            elif len(self.tools) == 2:
                print(self.tools[0], ", ", self.tools[1], sep='')
        if self.languages == 'Any1':
            print("Languages: One of your choice")
        elif self.languages == 'Any2':
            print("Languages: Two of your choice")
        print("Equipment:")
        for item in self.equipment:
            print('-', item, sep ='')
