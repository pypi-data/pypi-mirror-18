# Recursive function

def myfunction (cusine, levelOfIndentation):
    for i in cusine:
        if isinstance(i, list):
            myfunction(i, levelOfIndentation)
                else:
                    for tabCharacter in range(levelOfIndentation):
                        print("\t", end = '')
                    print(i)

#food = ["English","Italian","Indian",["Curry", ["Bindi","Dal","Aloo"]]]

#myfunction(food)
