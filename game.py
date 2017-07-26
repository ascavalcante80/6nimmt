class SetCards(object):

    def __init__(self):

        self.cards = self._build_cards()

    def _build_cards(self):

        cards = []

        for number in range(1,105):

            if number == 55:
                cards.append(Card(number, 7))
            elif number % 11 == 0:
                cards.append(Card(number, 5))
            elif number % 10 == 0:
                cards.append(Card(number,3))
            elif number % 5 == 0:
                cards.append(Card(number, 2))
            else:
                cards.append(Card(number, 1))
        return cards


class Card(object):

    def __init__(self, number, cows):

        self.number = number
        self.cows = cows


class CardsLine(object):

    def __init__(self):
        self.cards_line = {1:[], 2:[], 3:[], 4:[]}

    def update_line(self, card_player, line_nb, player):

        if len(self.cards_line[line_nb]) == 5:

            for index, card in enumerate(self.cards_line[line_nb]):
                player.cards_taken.append(self.cards_line[line_nb].pop(index))

            self.cards_line[line_nb].append(card_player)
            print("buuu! levou")

        else:
            self.cards_line[line_nb].append(card_player)


class Player(object):

    def __init__(self, name):

        self.name = name

        self.cards_set = []
        self.cards_played = []
        self.cards_taken = []


    def play_card(self, start_line, adversary_nb, played_cards):

        if not isinstance(start_line, CardsLine):
            return None

        # choosing card 0 risk
        line_nb, card_played = self._follow_straight_seq(start_line)

        if card_played is not None:
            played_cards.append(card_played.number - 1)
            return line_nb, card_played

        line_nb, card_played = self._distance_calculated(start_line)

        if card_played is not None:
            played_cards.append(card_played.number - 1)
            return line_nb, card_played

        line_nb, card_played = self._count_played_cards(start_line, played_cards)

        if card_played is not None and card_played != "":
            played_cards.append(card_played.number - 1)
            return line_nb, card_played


        line_nb, card_played = self._playing_risky(start_line, played_cards)

        if card_played is not None and card_played != "":
            played_cards.append(card_played.number - 1)
            return line_nb, card_played

        return "",""


    def _follow_straight_seq(self, start_line):
        card_played = None
        line_nb_set = -1

        for line_nb in start_line.cards_line.keys():

            if card_played is not  None:
                break

            for index_card_played, player_card in enumerate(self.cards_set):

                if (player_card.number - start_line.cards_line[line_nb][-1].number) == 1 and (len(start_line.cards_line[line_nb]) < 5):

                    print(self.name + " FOLLOW_STRAIGHT_ - player_card " + str(player_card.number) + " table_card: "+ str(start_line.cards_line[line_nb][-1].number) + "- line size :" + str(len(start_line.cards_line[line_nb])))

                    card_played = player_card
                    line_nb_set = line_nb
                    break

        if card_played is not None:
            self.cards_set.pop(index_card_played)
            self.cards_played.append(player_card)

        return line_nb_set, card_played


    def _distance_calculated(self, start_line):
        card_played = None
        line_nb_set = -1

        for line_nb in start_line.cards_line.keys():

            if card_played is not None:
                break

            for index_card, player_card in enumerate(self.cards_set):

                distance = 5 - len(start_line.cards_line[line_nb])

                if (player_card.number - start_line.cards_line[line_nb][-1].number) < distance and len(start_line.cards_line[line_nb]) < 5  and (player_card.number > start_line.cards_line[line_nb][-1].number):

                    print(self.name + " DISTANCE_CALCULATED - player_card " + str(player_card.number) + " table_card: "+ str(start_line.cards_line[line_nb][-1].number) + "- line size :" + str(len(start_line.cards_line[line_nb])))

                    line_nb_set = line_nb
                    card_played = player_card
                    break
        if card_played is not None:
            self.cards_set.pop(index_card)
            self.cards_played.append(player_card)

        return line_nb_set, card_played


    def _count_played_cards(self, start_line, played_cards):

        card_played = None
        prev_diff = 107
        line_nb_set = -1


        for line_nb in start_line.cards_line.keys():

            if len(start_line.cards_line[line_nb]) > 4:
                continue

            for index_card, player_card in enumerate(self.cards_set):

                diff = player_card.number - start_line.cards_line[line_nb][-1].number

                if diff < prev_diff and diff > 0:
                    prev_diff = diff

                    # obtain range to check
                    index_to_search = range(start_line.cards_line[line_nb][-1].number + 1, player_card.number)

                    for index in index_to_search:

                        if index not in played_cards:
                            break
                    else:
                        card_played = player_card
                        index_card_to_pop = index_card
                        line_nb_set = line_nb

                        break

        if card_played is not None:
            print(self.name + " COUNTED_DISTANCE_ - player_card " + str(player_card.number) + " table_card: " + str(
                start_line.cards_line[line_nb][-1].number) + "- line size :" + str(len(start_line.cards_line[line_nb])))

            self.cards_set.pop(index_card_to_pop)
            self.cards_played.append(player_card)

            return line_nb_set, card_played
        else:
            return line_nb,None


    def _playing_risky(self, start_line, played_cards):

        card_played = None
        prev_diff = 107
        line_nb_set = -1
        previous_count_missing = 107

        for line_nb in start_line.cards_line.keys():

            if len(start_line.cards_line[line_nb]) > 4:
                continue

            for index_card, player_card in enumerate(self.cards_set):

                diff = player_card.number - start_line.cards_line[line_nb][-1].number

                if diff < prev_diff and diff > 0:
                    prev_diff = diff

                    # obtain range to check
                    index_to_search = range(start_line.cards_line[line_nb][-1].number + 1, player_card.number)
                    count_missing = 0
                    for index in index_to_search:

                        if index not in played_cards:
                            count_missing += 1

                    if count_missing < previous_count_missing:
                        previous_count_missing = count_missing
                        card_played = player_card
                        index_card_to_pop = index_card
                        line_nb_set = line_nb

                        break

        if card_played is not None:
            print(self.name + " PLAYING_RISKY_ - player_card " + str(player_card.number) + " table_card: " + str(
                start_line.cards_line[line_nb][-1].number) + "- line size :" + str(len(start_line.cards_line[line_nb])))

            self.cards_set.pop(index_card_to_pop)
            self.cards_played.append(player_card)

            return line_nb_set, card_played
        else:
            return line_nb, None


    def _playing_loosy(self, start_line, played_cards):
        pass
        #todo criar método para jogar quando todas as cartas disponíves sao menores do que as da mesa