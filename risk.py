import board
import player
import rules
import cards

def risk():
    map = board.make_map()
    players = player.make_players(3)
    rules.play_game(map, cards.Card_Deck(map), players)

if __name__ == '__main__':
    risk()
