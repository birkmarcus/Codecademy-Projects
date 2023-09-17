# Magic Light
import collections
from dataclasses import dataclass
from operator import attrgetter
import random




@dataclass
class Card:
    card_type:str
    power:int
    cost:int
    color:str
    tapped:bool = False

    def __repr__(self):
        return f"{self.card_type} Cost: {self.cost} Power: {self.power} {'Tapped' if self.tapped else ''}\n"


    def tap(self) -> None:
        if self.tapped == False:
            self.tapped = True

    def untap(self) -> None:
        if self.tapped == True:
            self.tapped = False

class Deck:
    powers = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4]
    mana_cost = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2]
    
    def __init__(self, color) -> None:
        self.color = color
        self.creatures = [Card(card_type='Creature', color = self.color, power = pwr, cost = -pwr, tapped=True) 
                          for pwr in self.powers]    
        
        self.mana = [Card(card_type='Mana', color = self.color, power = 0, cost = cst) 
                          for cst in self.mana_cost]
        
        self.cards = self.mana + self.creatures
        self.shuffled_deck = ()

    def shuffle (self):
        self.shuffled_deck = random.sample(self.cards, k=len(self.cards))
        return self.shuffled_deck

    def __repr__(self) -> tuple[Card]:
        return self.shuffled_deck

class Player:
    def __init__(self, name:str, deck:Deck) -> None:
        self.hand:list[Card] = []
        self.life:int = 20
        self.name:str = name
        self.deck:Deck = deck
        self.table:list[Card] = []

    def draw_card(self) -> Card:
        if len(self.deck.shuffled_deck) != 0:
            self.hand.append(self.deck.shuffled_deck.pop(-1))
            return self.hand[-1]
        else:
            return None
        
    def show_hand(self):
        self.hand = sorted(self.hand, key=attrgetter('power'))
        print(self.name,'hand:')
        for index, item in enumerate(self.hand):
            print(f"{index}  {item.card_type} Cost: {item.cost} Power: {item.power} {'Tapped' if item.tapped else ''}")

    def play_card(self, index:int) -> None:
        if index <= len(self.hand):
            self.table.append(self.hand.pop(index))
        else:
            print(" That number card is not on your hand, try another number")

    def show_table(self) -> str:
        print(self.name,'table:')
        for index, item in enumerate(sorted(self.table, key=attrgetter('power'))):
            print(f"{index}  {item.card_type} Cost: {item.cost} Power: {item.power} {'Tapped' if item.tapped else ''}")
    
    def mana_pool(self) -> int:
        return sum([card.cost for card in self.table if card.card_type == "Mana"])
    
def attack(wizard:Player, index, other:Player):
        wizard.table = sorted(wizard.table, key=attrgetter('power'))
        other.table = sorted(other.table, key=attrgetter('power'))
        try:
            attacking_card:Card = wizard.table[index]
            defending_card:list[Card] = []
            if not attacking_card.tapped:
                for other_card in other.table:
                    if other_card.card_type == "Creature" and other_card.tapped == False: 
                        defending_card.append(other.table[-1])
                if len(defending_card) > 0:
                    print("attacking card: ", attacking_card, '\n', 
                            "defending card:", defending_card)
                else:
                    print("attacking card: ", attacking_card, '\n',
                        other.name, "has no defending card")
            else:
                print("That card is tapped out and cant attack")

            if len(defending_card) > 0:
                print_art(double_sword)
                if defending_card[0].power > attacking_card.power:
                    print(wizard.name, "attacking card: ", wizard.table.pop(index), '\n', 'died')
                    defending_card[0].tapped = True
                elif defending_card[0].power == attacking_card.power:
                    print(wizard.name, "attacking card: ", wizard.table.pop(index), '\n', other.name, "defending card", other.table.pop(-1), '\n both died')
                else:
                    print( "defending card", other.table.pop(-1), '\n', other.name,"s' card died")
                    attacking_card.tapped = True
            else:
                other.life -= attacking_card.power
                print(other.name, ' tuck damage and life is now', other.life)
                attacking_card.tapped = True
    
        except:
            print("That card can not attack")


def player_round(wizard:Player, other: Player):
    #Untap phase
    tapped_cards = [card for card in wizard.table if card.tapped]
    print(f"Untapping {len(tapped_cards)} cards")
    for card in tapped_cards: card.tapped = False

    #Draw phase
    wizard.draw_card()
    

    card_index:str = ""
    mana_to_play = 1
    table_mana = wizard.mana_pool()
    print(table_mana)
    while card_index.lower() != "n":
        wizard.show_hand()
        print(f"You currently have {table_mana} mana left")
        card_index = input("Want to play a card? Type card number otherwise press n: ")
        
        if card_index.lower() != 'n' and isinstance(int(card_index), int) and int(card_index) <= len(wizard.hand):
            #Play one mana
            if wizard.hand[int(card_index)].card_type == "Mana" and mana_to_play != 0:
                #Withdraw mana from tablemana
                table_mana += wizard.hand[int(card_index)].cost
                wizard.play_card(int(card_index))
                mana_to_play -= 1 
                
                #make sure he only plays one mana pr round
            elif  wizard.hand[int(card_index)].card_type == "Mana" and mana_to_play < 1:
                print("You can only play one mana each round")
                #Just play card
            else:
                if -wizard.hand[int(card_index)].cost <= table_mana:
                    #Update table mana
                    table_mana += wizard.hand[int(card_index)].cost
                    #Play card
                    wizard.play_card(int(card_index))
                    
                    print("Mana left: ", table_mana)
                else:
                    print(f"you don't have mana enough to play that card. You currently have {table_mana} mana left")

        else:
            break
    # Show table and opponants table before attacking
    wizard.show_table() 
    other.show_table()

    attacking_creature:str = input("Want to attack? Type number for creature to attack or type N otherwise \n")
    while attacking_creature.lower() != "n":
        attack(wizard, int(attacking_creature), other)
        attacking_creature = input("Want to attack again? Type number for creature to attack or type N otherwise \n")
        wizard.show_table() 
        other.show_table()

    print(f"{wizard.name} passed the round to {other.name}")

import time

# Thanks to: Alan De Smet http://www.highprogrammer.com/alan/ascpic/
# and Shanaka Dias, https://www.asciiart.eu/people/occupations/wizards
rat_art = '''
  ________________________________________________
 | Plague_Rats_____________________________(2)(M) |
 |  ||8888888888888888888888888888888888888888M|  |
 |  ||8888888888888888888888888888888888888888M|  |
 |  ||8888888888888888888888888888888888888888M|  |
 |  ||8888888888888888888888888888888888888888M|  |
 |  ||8888888888888888888888888888888888888888M|  |
 |  ||8888888888888888888888888888888888888888M|  |
 |  ||8888888888888P"´ ´´´ ,d8"Y88888888888888M|  |
 |  ||888888888888P         _,;888888888888888M|  |
 |  ||8888888"888P  _      (   ;,8888888888888M|  |
 |  ||888888; `-´    `-. a´ """   888888888888M|  |
 |  ||88888P'   :;      Y         888888888888M|  |
 |  ||8888P'  o  ':.    8      d  8=""__""Y888M|  |
 |  ||88,'            , 8      8  `888888b,""YM|  |
 |  ||;`._dd=".    ,,,',db.  888b.  """"´    8M|  |
 |  ||:;::;::N,; .´....´  a`.888888b.__.ad8888M|  |
 |  || . . :==;,;;´a" a  a ´´`888888 ANSON´93 M|  |
 |  `.========================================.´  |
 |   Summon Rats                                  |
 |    ,´"""""""""-"""""--"""""-""""""""""""""|    |
 |    | The *s below are the number of       |    |
 |    | Plague Rats in play, counting both   |    |
 |    | sides.  Thus if there are two Plague |    |
 |    `,Rats in play, each has a power and   |    |
 |    /´toughness 2/2.                       |    |
 |    | ``Should you a Rat to madness tease  |    |
 |    | Why ev´n a Rat may plague you..´´    \    |
 |    | --Samuel Coleridge, ``Recantation´´  |    |
 |    `.____,;;,__________,,______,__________|    |
 |                                                |
 |   Illus. (c) Anson Maddocks               */*  |
  """""""""""""""""""""""""""""""""""""""""""""""" 
'''


angel_art = """
  _______________________________________________  
 |Serra_Angel__________________________(3)(*)(*) | 
 |  ||     -======nnnq_____________^,  ..    #|  | 
 |  ||              ~/~~~~~~~~~~~^^'9)( -'nn #|  | 
 |  ||              |,`.           v',' ,'   #|  | 
 |  ||\             |,'`.           ,'  ;    #|  | 
 |  ||)`.           |_',`.         ,'  ;     #|  | 
 |  ||_)_).      ,-'~_=-'_;       ,'  ;      #|  | 
 |  ||)_)_)`.   :   |  ,' ^-_   ,'   ;       #|  | 
 |  ||_\')-) ;.:   (_       / ,'   ,'        #|  | 
 |  ||. ) / '.,'    .|     _-~   ,'          #|  | 
 |  || / / ) ;       .|`,  |    (            #|  | 
 |  ||/ / / /;    ...,'  `       \           #|  | 
 |  ||~/-/_/ ;:  :,^'       -,,' ,)          #|  | 
 |  || / / /;;:  :|   ........;;;;,.         #|  | 
 |  ||/ / / /;:::,';;;'''''''''   ; . . .    #|  | 
 |  || / / / /;'';   ;',         ,'. . . . . #|  | 
 |  ||  / / / /.;    ; ;         ;. . . . . .#|  | 
 |  `.=======================================.'  | 
 |  Summon_Angel_____________________________    | 
 |   |# , , , , , , , , , , , , , , , , , ,  |   | 
 |   |#'Flying ',',',',',',',',',',',',',',' |   | 
 |   |#'Does not tap when attacking ,',',',' |   | 
 |   |#'Born with wings of light and a sword |   | 
 |   |#'of faith, this heavenly incarnation' |   | 
 |   |#'embodies both fury and purity.,',',' |   | 
 |   |#',',',',',',',',',',',',',',',',',',' |   | 
 |   |m;m;m;m;m;m;m;m;m;m;m;m;m;m;m;m;m;m;m;,|   | 
 |    ---------------------------------------    | 
 |  Illus. (c) Douglas Schuler                   | 
 `-----------------------------------------------' 

 """

wizard_ball = """
                    ____ 
                  .'* *.'
               __/_*_*(_
              / _______ |
             _\_)/___\(_/_ 
            / _((\- -/))_ |
            \ \())(-)(()/ /
             ' \(((()))/ '
            / ' \)).))/ ' |
           / _ \ - | - /_  |
          (   ( .;''';. .'  )
          _\´__ /    )\ __´/_
            \/  \   ' /  \/
             .'  '...' ' )
              / /  |  \ p
             / .   .   . |
            /   .     .   7
           /   /   |   \   7
         .'   /    b    '.  '.
     _.-'    /     Bb     '-. '-._ 
 _.-'       |      BBb       '-.  '-. 
(________mrf\____.dBBBb.________)____)
"""
mgt_art = """
             _____     _____        ___  _.     __  ____  ____.          _      
           `~-,  \   `~-,  \       ~-_~~ \    /  ~~   / (    /' ,-~~~~~~,'     
             /    \    /'   \      /~>\   \  (  /~~~\/   )  | .'  /~~~)/       
            /      \  /      \    / /  \   \ | | ~==~~|  |  | |  (    '        
           /',/\    \/ '/\    \  / <_,'>\   \ \ \___) |  |  | |   \_  _____    
          /  /  \      /  \    \/     /  \   \ \  __  |  )  ( _`-_  ~~ ____]=='
         /  /    \     |   \    \~~~~~    `~~~~ ~~  ~\|(=~~~~~'   `~~~~___.   .
        /  /      \     \   \    \    ___         _                     | |\ /|
       /  /        |     |   \    \   `|''|      / '  _._|      .,_  _  | | V |
      /  /          \     \   \    \   |  |^ %) | __'T T |^ %)/^|| )/ \        
     /  (            |     |   \    \ .|. | |\,  \_|(] | | |\,[ || |\_/        
    /    \,           \     \   \    \             '                 \         
   /___---'            | ,-'~   .)    `.                            (~)        
.=~~                   `~       `~~~~~~~'                            ~         
                                                --chaos
"""
wizzard_gandalf = """
                                  ....
                                .'' .''
.                             .'   
\\                          .:    
 \\                        _:    :       ..----..
  \\                    .:::.....:::.. .'         ''
   \\                 .'  #-. .-######'     #        '
    \\                 '.##'/ ' ################       
     \\                  #####################         
      \\               ..##.-.#### .''''###'.._        
       \\             :--:########:            '.    .' 
        \\..__...--.. :--:#######.'   '.         '.     
        :     :  : : '':'-:'':'::        .         '.  .
        '---'''..: :    ':    '..'''.      '.        :
           \\  :: : :     '      ''''''.     '.      .
            \\ ::  : :     '            '.      '      
             \\::   : :           ....' ..:       '     '
              \\::  : :    .....####\\ .~~.:.             
               \\':.:.:.:'#########.===. ~ |.'-.   . '''.. 
                \\    .'  ########## \ \ _.' '. '-.       '''
                :\\  :     ########   \ \      '.  '-.        
               :  \\'    '   #### :    \ \      :.    '-.      
              :  .'\\   :'  :     :     \ \       :      '-.    
             : .'  .\\  '  :      :     :\ \       :        '.   
             ::   :  \\'  :.      :     : \ \      :          '. 
             ::. :    \\  : :      :    ;  \ \     :           '.
              : ':    '\\ :  :     :     :  \:\     :        ..
                 :    ' \\ :        :     ;  \|      :   .''
                 '.   '  \\:                         :.'
                  .:..... \\:       :            ..'
                 '._____|'.\\......'''''''.:..''
                            \
                            """
black_wind = """
 ▄▄▄▄    ██▓    ▄▄▄       ▄████▄   ██ ▄█▀    █     █░ ██▓ ███▄    █   ██████ 
▓█████▄ ▓██▒   ▒████▄    ▒██▀ ▀█   ██▄█▒    ▓█░ █ ░█░▓██▒ ██ ▀█   █ ▒██    ▒ 
▒██▒ ▄██▒██░   ▒██  ▀█▄  ▒▓█    ▄ ▓███▄░    ▒█░ █ ░█ ▒██▒▓██  ▀█ ██▒░ ▓██▄   
▒██░█▀  ▒██░   ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄    ░█░ █ ░█ ░██░▓██▒  ▐▌██▒  ▒   ██▒
░▓█  ▀█▓░██████▒▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄   ░░██▒██▓ ░██░▒██░   ▓██░▒██████▒▒
░▒▓███▀▒░ ▒░▓  ░▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒   ░ ▓░▒ ▒  ░▓  ░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░
▒░▒   ░ ░ ░ ▒  ░ ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░     ▒ ░ ░   ▒ ░░ ░░   ░ ▒░░ ░▒  ░ ░
 ░    ░   ░ ░    ░   ▒   ░        ░ ░░ ░      ░   ░   ▒ ░   ░   ░ ░ ░  ░  ░  
 ░          ░  ░     ░  ░░ ░      ░  ░          ░     ░           ░       ░  
      ░                  ░                                                   
     """                                                                    
white_wins = """
 █     █░ ██░ ██  ██▓▄▄▄█████▓▓█████     █     █░ ██▓ ███▄    █   ██████ 
▓█░ █ ░█░▓██░ ██▒▓██▒▓  ██▒ ▓▒▓█   ▀    ▓█░ █ ░█░▓██▒ ██ ▀█   █ ▒██    ▒ 
▒█░ █ ░█ ▒██▀▀██░▒██▒▒ ▓██░ ▒░▒███      ▒█░ █ ░█ ▒██▒▓██  ▀█ ██▒░ ▓██▄   
░█░ █ ░█ ░▓█ ░██ ░██░░ ▓██▓ ░ ▒▓█  ▄    ░█░ █ ░█ ░██░▓██▒  ▐▌██▒  ▒   ██▒
░░██▒██▓ ░▓█▒░██▓░██░  ▒██▒ ░ ░▒████▒   ░░██▒██▓ ░██░▒██░   ▓██░▒██████▒▒
░ ▓░▒ ▒   ▒ ░░▒░▒░▓    ▒ ░░   ░░ ▒░ ░   ░ ▓░▒ ▒  ░▓  ░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░
  ▒ ░ ░   ▒ ░▒░ ░ ▒ ░    ░     ░ ░  ░     ▒ ░ ░   ▒ ░░ ░░   ░ ▒░░ ░▒  ░ ░
  ░   ░   ░  ░░ ░ ▒ ░  ░         ░        ░   ░   ▒ ░   ░   ░ ░ ░  ░  ░  
    ░     ░  ░  ░ ░              ░  ░       ░     ░           ░       ░  
"""


double_sword = """
                     ___,  ___,   ____, ____, __    ____,
                    (-|_) (-|_\_,(-|   (-|   (-|   (-|_, 
                     _|__) _|  )  _|    _|    _|__, _|__,
                    (     (      (     (     (     (     

           |\                                                 /|
 _         )( ______________________   ______________________ )(         _
(_)///////(**)______________________> <______________________(**)\\\\\\\(_)
           )(                                                 )(
           |/                                                 \|
"""

def print_art(art):
    for line in art.split('\n'):
        print(line)
        time.sleep(0.02)


def main():
    print_art(mgt_art)
    # Instantiate decks
    white_deck = Deck("white")
    black_deck = Deck("Black")
    
    # Shuffle decks
    print("Shuffeling decks")
    white_deck.shuffle()
    black_deck.shuffle()
    
    # Instantiate Player: White and Black
    player1 = Player("White", white_deck)
    player2 = Player("Black", black_deck)
    print_art(wizzard_gandalf)
    print("First player is white \n\n")
    time.sleep(2)
    print_art(wizard_ball)
    print("Secund player is black \n\n")
    # Players draw 7 cards each
    print("Drawing cards")
    while len(player2.hand) < 7:
        player1.draw_card()
        player2.draw_card()

    while player1.life > 0 and player2.life > 0:
        player_round(player1, player2)
        player_round(player2, player1)


    if player1.life > player2.life:
        print(f"The winner is {player1.name}")
    else:
        print(f"The winner is {player2.name}")



    
        

if __name__ == '__main__':
    main()
