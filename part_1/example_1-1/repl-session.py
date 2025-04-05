exit
exit()
beer_card = Card('7', 'diamonds')
beer_card
deck = FrenchDeck()
len(deck)
deck[0]
deck[52]
deck[51]
deck[50]
from random import choice
choice(deck)
deck[:3]
deck[12::13]
for card in deck:
print(card)
for card in deck:
	print(card)
for card in reversed(deck):
	print(card)
Card('Q', 'hears') in deck
Card('Q', 'hearts') in deck
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
def spades_high(card):
	rank_value = FrenchDeck.ranks.index(card.rank)
	return rank_value * len(suit_values) + suit_values[card.suit]
for card in sorted(deck, key=spades_high):
	print(card)
import readline
readline.write_history_file("repl-session.py")
