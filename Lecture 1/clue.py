import termcolor

from logic import *

mustard = Symbol("ColMustard")
plum = Symbol("ProfPlum")
scarlet = Symbol("MsScarlet")
characters = [mustard, plum, scarlet]

ballroom = Symbol("ballroom")
kitchen = Symbol("kitchen")
library = Symbol("library")
rooms = [ballroom, kitchen, library]

knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench")
weapons = [knife, revolver, wrench]

symbols = characters + rooms + weapons


def check_knowledge(knowledge):
    for symbol in symbols:
        # If the knowledge base entails that a symbol is true, print it.
        if model_check(knowledge, symbol):
            termcolor.cprint(f"{symbol}: YES", "green")
        
        # If the knowledge base entails that a symbol is NOT entirely sure False, print it.
        elif not model_check(knowledge, Not(symbol)):
            print(f"{symbol}: MAYBE")

        # If the knowledge base entails that a symbol is entirely sure False, print it.
        else:
            termcolor.cprint(f"{symbol}: NO", "red")


# There must be a person, room, and weapon.
knowledge = And(
    Or(mustard, plum, scarlet),
    Or(ballroom, kitchen, library),
    Or(knife, revolver, wrench)
)

# Initial cards
knowledge.add(And(
    Not(mustard), Not(kitchen), Not(revolver)
))

# Unknown card
knowledge.add(Or(
    Not(scarlet), Not(library), Not(wrench) # Either Scarlet, Library, or Wrench is true
))

# Known cards
knowledge.add(Not(plum))
knowledge.add(Not(ballroom))

check_knowledge(knowledge)
