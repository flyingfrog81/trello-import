import logging
logging.basicConfig(level=logging.DEBUG)

import trelloapi
from constants import *

trello_board = trelloapi.get_board_by_name(board_name)
if not trello_board:
    logging.error("cannot find trello board: {}".format(board_name))
    sys.exit(0)
logging.info("found trello board: {}".format(trello_board['name']))

epics_trello_list = trelloapi.get_or_create_list(trello_board,
                                                 epics_list_name)
epics_trello_cards = trelloapi.get_list_cards(epics_trello_list)
for card in epics_trello_cards:
    trelloapi.delete_card(card)
backlog_trello_list = trelloapi.get_or_create_list(trello_board,
                                                   backlog_list_name)
backlog_trello_cards = trelloapi.get_list_cards(backlog_trello_list)
for card in backlog_trello_cards:
    trelloapi.delete_card(card)

board_labels = trelloapi.get_board_labels(trello_board)
for label in board_labels:
    trelloapi.delete_label(label)
