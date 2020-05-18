'''
This is to determine a character's attributes gained from their class. Still need to work out equip choices
'''
import os
direct = os.getcwd()
class ClassAttributes:

    def __init__(self):
        self.ch_class = ch_class
        file = open(direct + "\\DND Data\\ClassInfo_Expanded.txt", 'r')

        self.attribute_list = []
        for line in file:
            stripped_line = line.strip()
            attributes = stripped_line.split(';')
            self.attribute_list.append(attributes)
        self.attribute_list.remove(self.attribute_list[0])

        self.class_list = []
        for entry in self.attribute_list:
            self.class_list.append(entry[0])


    def set_class(self, ch_class)
        for entry in self.attribute_list:
            if ch_class.lower() == entry[0].lower():
                my_info = entry


        self.prim_stat      = my_info[1]
        self.sec_stat       = my_info[2]
        self.rec_background = my_info[3]
        self.hit_die        = my_info[4]
        self.armor          = my_info[5]
        self.weapon         = my_info[6]
        self.tool           = my_info[7]
        self.save1          = my_info[8]
        self.save2          = my_info[9]
        self.num_skills     = my_info[11]
        self.skill_list     = my_info[10].split(',')

        equip_raw = my_info[12].split('&')
        self.equip = []
        for item in equip_raw:
            equip_new = item.split('/')
            self.equip.append(equip_new)

    #Just to make sure it all checks out
    #If we decide to use this function, edit it to just show what we want it to
    def display(self):
        print("Class attributes for ", self.ch_class, ":", sep='')
        print()
        print("Primary Stat:", self.prim_stat)
        print("Secondary Stat:", self.sec_stat)
        print("Recommended Background:", self.rec_background)
        print("Hit Die:", self.hit_die)
        print()
        print("Proficiencies:")
        print("Armor:", self.armor)
        print("Weapons:", self.weapon)
        print("Tools:", self.tool)
        print()
        print("Saving Throws: ", self.save1, ", ", self.save2, sep='')

        if 'Any' in self.skill_list:
            print("Skills: Choose any", self.num_skills)
        else:
            print("Skills: Choose", self.num_skills, "from ", end='')
            count = len(self.skill_list) - 1
            for i in range(count-1):
                print(self.skill_list[i], ', ', sep='', end='')
            print('and ', self.skill_list[count],sep='')


        print()
        print("Starting Equipment:")
        for line in self.equip:
            if len(line) == 3:
                print('-(a)', line[0], ' OR (b)', line[1], ' OR (c)', line[2], sep='')
            elif len(line) == 2:
                print('-(a)', line[0], ' OR (b)', line[1], sep='')
            elif len(line) == 1:
                print('-', line[0], sep='')
