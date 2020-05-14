'''
This class includes the optional additional information to be printed to keep the main file organized
'''
import tkinter as tk

class Information:

    def general(self, stringVar):
        print("Dungeons and Dragons is a tabletop roleplaying game in which you create a fictional character to")
        print("interact with the world around you. To create a character, you can either build one manually or")
        print("use the automated character generator.")
        stringVar.set("Dungeons and Dragons is a tabletop roleplaying game in which you create a fictional character to interact with the world around you. To create a character, you can either build one manually or use the automated character generator.")


    def race(self):
        print("There are a variety of different lands and cultures in the world of D&D, with a variety of races")
        print("to match. Each of the races comes with unique special abilities or skills, as shown below.")

    def dnd_class(self):
        print("Classes are essentially the job or role of your character. These influence a character's skills")
        print("and the methods they may use to interact with the world, wether it be through brute force or")
        print("more subtle tactics.")

    def stats(self):
        print("Stats are your character's proficiencies with different skills, such as strength or charisma. You")
        print("will use these stats when you interact with the world, to determine how efficient you are in the")
        print("task at hand. Higher stats mean you're more likely to be able to do an action, such as lifting a")
        print("boulder or shooting a bow. You can either accept the default stats or roll for your own.")
