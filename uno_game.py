"""
UNO! Game

This program lets the user play a UNO! game. The user can select the number of players (2-4) and
also choose to save and exit a game in process and choose to load one of the saved games later on.
The program repeatedly asks the user to input a value until the user inputs a valid value. For
simplicity, the UNO rule of shouting "uno!" when there is one card left in one's deck is not
considered. The program is composed of 11 functions - generate_deck, draw_cards, show_cards,
check_card_playable, check_player_playable, check_change_colour, check_win, play_card, play_game,
save_game, and load_game - in addition to the main function.
"""

import random
import os
import sys

def generate_deck():
    """
    Generates a UNO deck in a random order, made up of 108 cards
    Returns the deck, in a list (deck)
    """
    deck = []
    colours = ["Red","Yellow","Green","Blue"]
    attributes = [0,1,2,3,4,5,6,7,8,9,"Skip","Reverse","Draw Two"]
    for colour in colours:
        for attribute in attributes:
            card = "{} {}".format(colour, attribute)
            deck.append(card)
            if attribute != 0: #there is only one card of the number 0 per colour
                deck.append(card) #add cards that are not 0 once again
    for i in range(4):
        deck.append("Wild")
        deck.append("Draw Four") #add the Wild and Draw Four cards, four each
    for i in range(108):
        random.shuffle(deck) #shuffle the deck 108 times
    while True:
        #Let the card at the top be a number card
        if deck[0][-1] not in ("0","1","2","3","4","5","6","7","8","9"):
            random.shuffle(deck)
        else:
            break
    return deck

def draw_cards(num_players):
    """
    Randomly draws cards from the previously created deck for a specified number of players
    Argument - num_players
    """
    global deck
    for a in range(num_players):
        player_deck = []
        for b in range(7):
            player_deck.append(deck.pop(-1))
        players_decks.append(player_deck)

def show_cards(player_no):
    """
    Shows a player what cards they are holding and what card is on top of the deck
    Argument - player_no
    """
    global deck, players_decks
    print("-----------------")
    print("Player {}".format(player_no).center(18))
    print("-----------------")
    print("Card on top:",deck[0])
    print("Your cards:")
    num = 1
    for card in players_decks[player_no-1]:
        print("{}. {}".format(num,card))
        num += 1

def check_card_playable(player_no,card_no):
    """
    Checks if a card is playable
    Arguments - player_no, card_no
    Returns True/False
    """
    card = players_decks[player_no-1][card_no-1]
    if card == "Wild" or card == "Draw Four":
        return True
    else:
        colour, attribute = card.split(' ',1)
        if colour in deck[0] or attribute in deck[0]:
            return True
        else:
            return False

def check_player_playable(player_no):
    """
    Checks if a player has any card that is playable (if he/she has to draw a card)
    Argument - player_no
    Returns playable (Boolean)
    """
    playable = False  # could not play any card
    for i in range(1,len(players_decks[player_no - 1])+1):
        if check_card_playable(player_no, i) == True:
            playable = True
            break
    return playable

def check_change_colour():
    """
    Checks if the played card can change the colour and lets the player choose a new colour
    """
    global deck
    if deck[0] == "Wild" or deck[0] == "Draw Four":
        colour = input("Which colour would you like to choose?\n1.Red\n2.Blue\n3.Green\n4.Yellow\n")
        if colour == '1':
            deck[0] = "Red " + deck[0]
        if colour == '2':
            deck[0] = "Blue " + deck[0]
        if colour == '3':
            deck[0] = "Green " + deck[0]
        if colour == '4':
            deck[0] = "Yellow " + deck[0]
        print("Done!")

def check_win(player_no):
    """
    Checks if a player has won the game
    Argument - player_no
    Returns True if he/she has won; False otherwise
    """
    global players_decks
    if len(players_decks[player_no-1]) == 0:
        return True
    else:
        return False

def play_card(player_no):
    """
    Asks the user to choose a card to play until a valid card is chosen or a card is drawn
    Removes the chosen card from the user's deck and adds it to the main deck
    Argument - player_no (player number)
    Returns True/False (for if a card was played)
    """
    global deck, players_decks
    show_cards(player_no)
    if "Draw" in deck[0] and "*" not in deck[0]:
        #The '*' means that the draw two/four card is not effective anymore (someone has drawn already)
        if "Two" in deck[0]:
            print("Oops! You have to draw two cards.")
            print("You drew: {}, {}".format(deck[-1],deck[-2]))
            for i in range(2):
                players_decks[player_no - 1].append(deck.pop(-1))
        if "Four" in deck[0]:
            print("Oops! You have to draw four cards.")
            print("You drew: {}, {}, {}, {}".format(deck[-1],deck[-2],deck[-3],deck[-4]))
            for i in range(4):
                players_decks[player_no - 1].append(deck.pop(-1))
        deck[0] = deck[0] +" *"
        return False
    elif check_player_playable(player_no) == False:
        print("Cannot play any card. You have to draw a card.")
        print("Drawing a card...",deck[-1])
        players_decks[player_no-1].append(deck.pop(-1))
        if check_card_playable(player_no, len(players_decks[player_no-1])):
            print("This card can be and is automatically played.")
            deck.insert(0, players_decks[player_no - 1].pop(-1))
            return True
        else:
            print("This card cannot be played.")
            return False
    elif check_player_playable(player_no) == True:
        while True:
            try:
                play = int(input("Which card would you like to play?"))
                assert 0 < play <= len(players_decks[player_no-1])
            except:
                print("Please enter a valid number!\n")
                continue
            if check_card_playable(player_no, play) == True:
                deck.insert(0, players_decks[player_no-1].pop(play-1))
                print("Done!")
                break
            else:
                print("The card is not playable. Try again: ")
                continue
        return True

def play_game():
    """
    The actual function that plays the game
    Has the turn rotate from one player to another
    """
    global turn,turn_direction,no_wins1,no_wins2,no_wins3,no_wins4,deck,players_decks
    while True:
        if turn == 1:
            print(("Enter 'exit' to save game and exit."))
            enter = input("Hit any key to continue.")
            os.system('clear')
            if enter == "exit":
                save_game()
                sys.exit()
            if play_card(1) == True:
                if "Reverse" in deck[0]:
                    turn_direction *= -1
                if turn_direction == -1:
                    turn = num_players+1
                if "Skip" in deck[0]:
                    turn += turn_direction
                    if turn_direction == -1:
                        turn = num_players
                    if num_players == 2 and turn_direction == 1:
                        turn = 0
                if "Reverse" in deck[0] and num_players == 2:
                    turn = 1-turn_direction
            elif turn_direction == -1:
                    turn = num_players+1
            check_change_colour()
            if check_win(1):
                print("\nCongratulations! Player 1 has won.")
                no_wins1 += 1
                break
            turn += turn_direction
        if turn == 2:
            print(("Enter 'exit' to save game and exit."))
            enter = input("Hit any key to continue.")
            os.system('clear')
            if enter == "exit":
                save_game()
                sys.exit()
            if play_card(2) == True:
                if "Reverse" in deck[0]:
                    turn_direction *= -1
                if num_players == 2 and turn_direction == 1:
                    turn = 0
                if "Skip" in deck[0]:
                    turn += turn_direction
                    if turn_direction == -1:
                        turn = num_players+1
                    if num_players == 3 and turn_direction == 1:
                        turn = 0
                if "Reverse" in deck[0] and num_players == 2:
                    turn = 2-turn_direction
            else:
                if num_players == 2 and turn_direction == 1:
                    turn = 0
            check_change_colour()
            if check_win(2):
                print("\nCongratulations! Player 2 has won.")
                no_wins2 += 1
                break
            turn += turn_direction
        if turn == 3:
            print(("Enter 'exit' to save game and exit."))
            enter = input("Hit any key to continue.")
            os.system('clear')
            if enter == "exit":
                save_game()
                sys.exit()
            if play_card(3) == True:
                if "Reverse" in deck[0]:
                    turn_direction *= -1
                if num_players == 3 and turn_direction == 1:
                    turn = 0
                if "Skip" in deck[0]:
                    turn += turn_direction
                    if turn == 4:
                        turn = 0
            else:
                if num_players == 3 and turn_direction == 1:
                    turn = 0
            check_change_colour()
            if check_win(3):
                print("\nCongratulations! Player 3 has won.")
                no_wins3 += 1
                break
            turn += turn_direction
        if turn == 4:
            print(("Enter 'exit' to save game and exit."))
            enter = input("Hit any key to continue.")
            os.system('clear')
            if enter == "exit":
                save_game()
                sys.exit()
            if play_card(4) == True:
                if "Reverse" in deck[0]:
                    turn_direction *= -1
                if turn_direction == 1:
                    turn = 0
                if "Skip" in deck[0]:
                    turn += turn_direction
            else:
                if num_players == 4 and turn_direction == 1:
                    turn = 0
            check_change_colour()
            if check_win(4):
                print("\nCongratulations! Player 4 has won.")
                no_wins4 += 1
                break
            turn += turn_direction

def save_game():
    """
    Saves the game by creating a .txt file containing the game's information
    """
    global game_name, loaded
    if not loaded:
        filename = input("file name: ")
        a = open(os.path.join(os.getcwd()+"/uno","games.txt"),"a")
        a.write(filename+"\n")
        f = open(os.path.join(os.getcwd() + "/uno", filename + ".txt"), "w")
    else:
        f = open(os.path.join(os.getcwd() + "/uno", game_name + ".txt"), "w")
    f.write("""\
num_players:{}
turn_direction:{} 
turn:{}
no_wins1:{}
no_wins2:{}
no_wins3:{}
no_wins4:{}
deck:""".format(num_players,turn_direction, turn, no_wins1, no_wins2, no_wins3, no_wins4))
    for i in range(len(deck)):
        if i < len(deck) - 1:
            f.write(deck[i]+"/")
        else:
            f.write(deck[i])
    f.write("\nplayers_decks:")
    for i in range(len(players_decks)):
        for x in range(len(players_decks[i])):
            if x < len(players_decks[i])-1:
                f.write(players_decks[i][x]+"/")
            else:
                f.write(players_decks[i][x])
        f.write("|")
    sys.exit()

def load_game():
    """
    Loads a game by loading the game information stored in its .txt file
    """
    global no_wins1, no_wins2, no_wins3, no_wins4, num_players, turn, turn_direction, deck, players_decks, game_name
    print("Which game do you want to load?")
    a = open(os.path.join(os.getcwd() + "/uno", "games.txt"), "r")
    games = [game.rstrip() for game in a]
    for i in range(len(games)):
        print("{}. {}".format(i + 1, games[i])) #print saved games
    game_name = games[int(input(">> ")) - 1]
    f = open(os.path.join(os.getcwd() + "/uno", game_name + ".txt"), "r")
    num_players = int(f.readline().split(':')[1])
    turn_direction = int(f.readline().split(':')[1])
    turn = int(f.readline().split(':')[1])
    no_wins1 = int(f.readline().split(':')[1])
    no_wins2 = int(f.readline().split(':')[1])
    no_wins3 = int(f.readline().split(':')[1])
    no_wins4 = int(f.readline().split(':')[1])
    deck = list(f.readline().split(":")[1:][0].rstrip().split("/"))
    players_decks = list(f.readline().split(":")[1:][0].split("|"))
    for i in range(len(players_decks)):
        players_decks[i] = players_decks[i].split("/")
    players_decks.pop(-1)

#%%
def main():
    global no_wins1,no_wins2,no_wins3,no_wins4,num_players,turn,turn_direction,deck,\
        players_decks,loaded
    try:
        os.mkdir("uno")
        open(os.path.join(os.getcwd() + "/uno", "games.txt"), "x")
    except:
        pass
    if input("Do you want to load a saved game? (1 - yes / any other key - no)") == "1":
        a = open(os.path.join(os.getcwd() + "/uno", "games.txt"), "r")
        line_count = 0
        for line in a:
            if line != "\n":
                line_count += 1
        if line_count == 0:
            print("There is no game to load! Play and save a game first!")
            loaded = False
        else:
            loaded = True
            load_game()
    else:
        loaded = False
        no_wins1 = 0
        no_wins2 = 0
        no_wins3 = 0
        no_wins4 = 0
    while True:
        if not loaded:
            deck = generate_deck()
            players_decks = []
            turn = 1
            turn_direction = 1
            no_wins1 = 0
            no_wins2 = 0
            no_wins3 = 0
            no_wins4 = 0
            while True:
                try:
                    num_players = int(input("Please select the number of players (2-4): "))
                    assert num_players >= 2 and num_players <= 4
                except:
                    print("Invalid number of players. Please try again.")
                    continue
                break
            draw_cards(num_players)
            print("Drawing cards...")
            print("Let the game begin!")
            print()
        print("""\
██╗░░░██╗███╗░░██╗░█████╗░██╗
██║░░░██║████╗░██║██╔══██╗██║
██║░░░██║██╔██╗██║██║░░██║██║
██║░░░██║██║╚████║██║░░██║╚═╝
╚██████╔╝██║░╚███║╚█████╔╝██╗
░╚═════╝░╚═╝░░╚══╝░╚════╝░╚═╝""")
        play_game()
        print("Number of wins:\nplayer 1: {}\nplayer 2: {}\nplayer 3: {}\nplayer 4: {}"\
              .format(no_wins1,no_wins2,no_wins3,no_wins4))
        loaded = False
        if input("Do you want to play again? (1 - play again 2 - exit)") == "2":
            break

#%%
if __name__ == "__main__":
    main()