from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # If A is a knight, then A is telling the truth.
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave))),
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),
    Not(And(BKnight, BKnave)),
    Or(BKnight, BKnave),
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave))),
    Implication(BKnight, And(AKnave, BKnight)),
    Implication(BKnave, Not(And(AKnave, BKnight)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),
    Not(And(BKnight, BKnave)),
    Or(BKnight, BKnave),
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), 
    Implication(AKnave, Not(Or(And(AKnight, AKnave), And(AKnave, BKnave)))),
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),
    Not(And(BKnight, BKnave)),
    Or(BKnight, BKnave),
    Not(And(CKnight, CKnave)),
    Or(CKnight, CKnave),
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    Implication(BKnight, And(AKnave, CKnave)), # If B is a knight, then statement from A "B is a knave" is false, so A is a knave. And statement from B "C is a knave" is true, so C is a knave.
    Implication(BKnave, Not(And(AKnave, CKnave))), # If B is a knave, then statement from A "B is a knave" is true, so A is a knight. And statement from B "C is a knave" is false, so C is a knight.
    Implication(CKnight, AKnight), 
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
