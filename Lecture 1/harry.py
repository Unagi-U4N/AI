from logic import *

rain = Symbol("rain") # It's raining
hagrid = Symbol("hagrid") # He is in Hagrid
dumbledore = Symbol("dumbledore") # He is in Dumbledore

knowledge = And(
    Implication(Not(rain), hagrid), # If it's not raining, He is visiting Hagrid
    Or(hagrid, dumbledore),         # He is visiting Hagrid or Dumbledore
    Not(And(hagrid, dumbledore)),   # He is not visiting Hagrid and Dumbledore at the same time
    dumbledore                      # He is visiting Dubledore
)

print(model_check(knowledge, rain))

# sentence = And(rain, hagrid)
# print(sentence.formula())

# knowledge1 = Implication(Not(rain), hagrid)
# print(knowledge1.formula())