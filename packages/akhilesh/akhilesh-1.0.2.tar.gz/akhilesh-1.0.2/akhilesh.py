# Recursive function

def myfunction (cusine, indent = False ,level = 0):
    for i in cusine:
        if isinstance(i, list):
            myfunction(i, indent ,level + 1)
        else:
            if indent:
                for tabCharacter in range(level):
                    print("\t", end = '')
            print(i)

#food = ["English","Italian","Indian",["Curry", ["Bindi","Dal","Aloo"]]]

#myfunction(food)
