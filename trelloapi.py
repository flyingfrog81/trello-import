import urllib.parse
import logging

import requests

import credentials

base_url = 'https://api.trello.com/1/'
default_params = dict(key=credentials.api_key,
                      token=credentials.app_token)

def trello_get(suffix="", **kwargs):
    composed_url = urllib.parse.urljoin(base_url, suffix)
    params = kwargs
    params.update(default_params)
    reply = requests.get(composed_url, params)
    return reply

def trello_post(suffix="", **kwargs):
    composed_url = urllib.parse.urljoin(base_url, suffix)
    params = kwargs
    params.update(default_params)
    reply = requests.request("POST", composed_url, params=params)
    return reply

def trello_delete(suffix="", **kwargs):
    composed_url = urllib.parse.urljoin(base_url, suffix)
    params = kwargs
    params.update(default_params)
    reply = requests.request("DELETE", composed_url, params=params)
    return reply

def get_board_by_name(board_name):
    boards = trello_get("members/me/boards")
    if not boards.ok:
        return None
    board = list(filter(lambda x : x['name'] == board_name, boards.json()))
    if not board:
        return None
    return board[0]

def get_board_lists(board, trello_filter="open"):
    lists_suffix = "boards/" + board['id'] + "/lists"
    lists = trello_get(lists_suffix, filter=trello_filter)
    if not lists.ok:
        return None
    return lists.json()

def get_board_cards(board, trello_filter="visible"):
    cards_suffix = "boards/" + board['id'] + "/cards/" + trello_filter
    cards = trello_get(cards_suffix)
    if not cards.ok:
        return None
    return cards.json()

def get_board_labels(board):
    labels_suffix = "boards/" + board['id'] + "/labels"
    labels = trello_get(labels_suffix)
    if not labels.ok:
        return None
    return labels.json()

def get_list_cards(trello_list):
    cards_suffix = "lists/" + trello_list['id'] + "/cards"
    cards = trello_get(cards_suffix)
    if not cards.ok:
        return None
    return cards.json()

def get_card_attachments(card):
    attachments_suffix = "cards/" + card['id'] + "/attachments"
    attachments = trello_get(attachments_suffix)
    return attachments.json()

def create_list(trello_board, list_name):
    logging.debug("creating trello list: {}".format(list_name))
    list_reply  = trello_post("lists",
                              name=list_name,
                              idBoard=trello_board['id'])
    return list_reply.json()

def get_board_list_by_name(trello_board, list_name):
    trello_lists = get_board_lists(trello_board)
    trello_list = [_l for _l in trello_lists if _l['name'] == list_name]
    if not trello_list:
        return None
    else:
        trello_list = trello_list[0]
        logging.debug("found trello list {}".format(list_name))
    return trello_list

def get_or_create_list(trello_board, list_name):
    trello_list = get_board_list_by_name(trello_board, list_name)
    if not trello_list:
        trello_list = create_list(trello_board, list_name)
    return trello_list

def create_label(trello_board, label_name, label_color="none"):
    logging.debug("create label: {}".format(label_name))
    trello_label = trello_post("boards/" +
                               trello_board['id'] +
                               "/labels",
                               name = label_name,
                               color = label_color).json()
    return trello_label

def create_card(trello_list, card_name, card_labels = []):
        logging.debug("creating trello card: {}".format(card_name))
        trello_card = trello_post("cards",
                                  idList = trello_list['id'],
                                  idLabels = card_labels,
                                  name = card_name).json()
        return trello_card

def create_attachment(trello_card, attachment_name, attachment_url):
        logging.debug("creating trello attachment: {}".format(attachment_name))
        trello_attachment = trello_post("cards/" +
                                        trello_card['id'] +
                                        "/attachments",
                                        name = attachment_name,
                                        url = attachment_url).json()
        return trello_attachment

def delete_card(trello_card):
        logging.debug("deleting trello card: {}".format(trello_card['name']))
        reply = trello_delete("/cards/" + trello_card['id'])
        return reply

def delete_label(trello_label):
        logging.debug("deleting trello label: {}".format(trello_label['name']))
        reply = trello_delete("/labels/" + trello_label['id'])
        return reply
