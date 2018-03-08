import logging
logging.basicConfig(level=logging.INFO)
import itertools
import sys

import trelloapi
import jira_import
from constants import *

# import jira issues
jira_epics, jira_issues = jira_import.read_jira_issues(jira_export_filename,
                                            jira_base_url)
if not jira_issues:
    logging.info("no issue can be imported")
    sys.exit(0)

# search for a named trello board
trello_board = trelloapi.get_board_by_name(board_name)
if not trello_board:
    logging.error("cannot find trello board: {}".format(board_name))
    sys.exit(0)
logging.info("found trello board: {}".format(trello_board['name']))

# search for epics list in trello board
epics_trello_list = trelloapi.get_or_create_list(trello_board,
                                                 epics_list_name)
# get trello board cards
board_trello_cards = trelloapi.get_board_cards(trello_board)
board_cards_dict = {}
for card in board_trello_cards:
    board_cards_dict[card['name']] = card
# get trello epics cards
epics_trello_cards = trelloapi.get_list_cards(epics_trello_list)
epics_cards_dict = {}
for card in epics_trello_cards:
    epics_cards_dict[card['name']] = card
# epics_trello_names = [_c['name'] for _c in epics_trello_cards]
# get trello board labels
board_labels = trelloapi.get_board_labels(trello_board)
board_labels_dict = {}
for label in board_labels:
    board_labels_dict[label['name']] = label
for sp in story_points:
    if not sp in board_labels_dict.keys():
        board_labels_dict[sp] = trelloapi.create_label(trello_board,
                                                       sp,
                                                       story_points_color)


# Update trello epics and labels to match jira export
for epic_id, (epic_summary, epic_name, epic_link) in jira_epics.items():
    # update labels with epic name
    board_label = board_labels_dict.get(epic_name)
    if not board_label:
        logging.info("adding board label: {}".format(epic_name))
        board_label = trelloapi.create_label(trello_board,
                                              epic_name,
                                              next(color))
        board_labels_dict[epic_name] = board_label

    # update epics trello list with jira epic
    epic_card = epics_cards_dict.pop(epic_name, None)
    if not epic_card:
        logging.info("adding epic card: {}".format(epic_name))
        epic_card = trelloapi.create_card(epics_trello_list,
                                          epic_name,
                                          [board_label['id']])
        # link the newly created epic with the corresponding jira issue
        attachment = trelloapi.create_attachment(epic_card,
                                                 epic_link,
                                                 epic_link)
    else:
        board_cards_dict.pop(epic_name)

# search for backlog list in trello board
backlog_trello_list = trelloapi.get_or_create_list(trello_board,
                                                   backlog_list_name)


# Update trello cards to match jira export
for issue_id, (issue_summary, epic_id, issue_link, issue_story_points) in jira_issues.items():
    issue_card = board_cards_dict.pop(issue_summary, None)
    if not issue_card:
        if epic_id:
            board_label = board_labels_dict[jira_epics[epic_id][1]]
            if board_label:
                board_label_id = [board_label['id']]
            else:
                board_label_id = []
        else:
            board_label_id = []
        if issue_story_points:
            try:
                board_label_id.append(board_labels_dict[issue_story_points]['id'])
            except:
                pass
        logging.info("adding card: {}\nlabels: {}".format(issue_summary,
                     ",".join(board_label_id)))
        issue_card = trelloapi.create_card(backlog_trello_list,
                                           issue_summary,
                                           ",".join(board_label_id))
        # link the newly created epic with the corresponding jira issue
        attachment = trelloapi.create_attachment(issue_card,
                                                 issue_link,
                                                 issue_link)

# Remove pending cards from trello board
#for card in board_cards_dict.values():
#    trelloapi.delete_card(card)
