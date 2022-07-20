import random

print("Tic-Tac-Toe - The Game")
print("----------------------")

#Setting game variables
numbers = [1,2,3,4,5,6,7,8,9]
game = [[1,2,3], [4,5,6], [7,8,9]]
rows = 3
cols = 3

#Creating a function that draws the game into the console
def printGame():
    for x in range(rows):
        print("\n+---+---+---+")
        print("|", end = "")
        for y in range(cols):
            print("", game[x][y], end = " |")
    print("\n+---+---+---+")

def modArray(num, turn):
    num -= 1
    if(num == 0):
        game[0][0] = turn
    elif(num == 1):
        game[0][1] = turn
    elif(num == 2):
        game[0][2] = turn
    elif(num == 3):
        game[1][0] = turn
    elif(num == 4):
        game[1][1] = turn
    elif(num == 5):
        game[1][2] = turn
    elif(num == 6):
        game[2][0] = turn
    elif(num == 7):
        game[2][1] = turn
    elif(num == 8):
        game[2][2] = turn

#Defining a function to check for a winner
def Winner(game):
    #X axis Win
    if (game[0][0] == 'X' and game[0][1] == 'X' and game[0][2] == 'X'):
        print("Player Wins!")
        return "X"
    elif (game[0][0] == 'O' and game[0][1] == 'O' and game[0][2] == 'O'):
        print("CPU Wins!")
        return "O"
    elif (game[1][0] == 'X' and game[1][1] == 'X' and game[1][2] == 'X'):
        print("Player Wins!")
        return "X"
    elif (game[1][0] == 'O' and game[1][1] == 'O' and game[1][2] == 'O'):
        print("CPU Wins!")
        return "O"
    elif (game[2][0] == 'X' and game[2][1] == 'X' and game[2][2] == 'X'):
        print("Player Wins!")
        return "X"
    elif (game[2][0] == 'O' and game[2][1] == 'O' and game[2][2] == 'O'):
        print("CPU Wins!")
        return "O"
    #Y axis Win
    if (game[0][0] == 'X' and game[1][0] == 'X' and game[2][0] == 'X'):
        print("Player Wins!")
        return "X"
    elif (game[0][0] == 'O' and game[1][0] == 'O' and game[2][0] == 'O'):
        print("CPU Wins!")
        return "O"
    elif (game[0][1] == 'X' and game[1][1] == 'X' and game[2][1] == 'X'):
        print("Player Wins!")
        return "X"
    elif (game[0][1] == 'O' and game[1][1] == 'O' and game[2][1] == 'O'):
        print("CPU Wins!")
        return "O"
    elif (game[0][2] == 'X' and game[1][2] == 'X' and game[2][2] == 'X'):
        print("Player Wins!")
        return "X"
    elif (game[0][2] == 'O' and game[1][2] == 'O' and game[2][2] == 'O'):
        print("CPU Wins!")
        return "O"
    #Cross win
    elif (game[0][0] == 'X' and game[1][1] == 'X' and game[2][2] == 'X'):
        print("Player Wins!")
        return "X"
    elif (game[0][0] == 'O' and game[1][1] == 'O' and game[2][2] == 'O'):
        print("CPU Wins!")
        return "O"
    elif (game[0][2] == 'X' and game[1][1] == 'X' and game[2][0] == 'X'):
        print("Player Wins!")
        return "X"
    elif (game[0][2] == 'O' and game[1][1] == 'O' and game[2][0] == 'O'):
        print("CPU Wins!")
        return "O"
    else:
        return "N"

turnCounter = 0
leaveloop = False

while(leaveloop == False):
    #players turn
    if(turnCounter % 2 == 1):
        printGame()
        numberPicked = int(input("\nChoose a number [1-9]: "))
        if(numberPicked >= 1 or numberPicked <= 9):
            modArray(numberPicked, 'X')
            numbers.remove(numberPicked)
        else:
            print("Not an Input, Try Again!")
            turnCounter += 1
            break
    #computers turn
    else:
        while(True):
            cpu = random.choice(numbers)
            print("\nCPU selection:", cpu)
            if(cpu in numbers):
                modArray(cpu, 'O')
                numbers.remove(cpu)
                turnCounter = 1
                leaveloop = False
                break

    winner = Winner(game)
    if(winner != 'N'):
        print("\nGame Over! Final Project | LIS4930")
        break






