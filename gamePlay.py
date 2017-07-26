from game import SetCards, Player, CardsLine
from random import randint

class GamePlay(object):

    def __init__(self, set_players):

        if len(set_players) > 10 or len(set_players) < 2:
            print("Game for 2 up to 10 players")
            exit(1)

        self.used_cards = []

        self.set_players = set_players
        self.set_Cards = SetCards()
        self.cards_line = CardsLine()
        self._distribute_cards()
        self._start_line()

        self.start_game()

        print("Game Over")

    def _distribute_cards(self):
        given_cards = []


        for player in self.set_players:

            print ("Distribute cards for player " + player.name)

            count_cards = 0
            while(count_cards < 10):

                index = randint(0,103)

                if index not in given_cards:
                    player.cards_set.append(self.set_Cards.cards[index])
                    given_cards.append(index)
                    count_cards += 1

    def _start_line(self):

        count_cards = 1
        while (count_cards < 5):

            index = randint(0, 103)

            if index not in self.used_cards:
                self.cards_line.cards_line[count_cards] = [self.set_Cards.cards[index]]

                # insert cards in the used cards
                self.used_cards.append(index)
                count_cards += 1

    def start_game(self):

        round_play = 1
        while(round_play < 11):
            round_data = []
            for player in set_player:
                line_nb, card_player = player.play_card(self.cards_line, len(set_player), self.used_cards)
                if line_nb == '':
                    continue
                    round_play += 1


                round_data.append((card_player, line_nb, player))
            for rd in round_data:
                self.used_cards.append(rd[0].number -1)
                self.cards_line.update_line(rd[0], rd[1], rd[2])


            round_play += 1
        print("--------- ")
        for key in self.cards_line.cards_line.keys():
            print("line: " + str(key))
            line = ""
            for cards in self.cards_line.cards_line[key]:
                line += str(cards.number) + ", "
            print("\t" + line[:-1])


set_player = [Player("Marcinho"), Player("Bob Run"), Player("Suel"), Player("Amaro")]
game_play = GamePlay(set_player)



