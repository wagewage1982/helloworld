#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calculate dealer PR"""

__author__ = 'Fei Deng'

# Imports
import re
import numpy as np
# import matplotlib.pyplot as plt
# import os
# import sys
# import random
CARD_LIST = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
DEALER_IL = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'A']
DEALER_OL = ['17', '18', '19', '20', '21', 'bj', 'bust']


def dealer_hit(dealer_hand):
    """Get probability of hit"""
    dealer_pr = np.zeros(24)
    for new_card in CARD_LIST:
        cards_value = 0
        soft_ace = 0
        cards = dealer_hand + [new_card]
        for i in list(range(len(cards))):
            if re.match(r'[TJQK]', cards[i]):
                value = 10
            elif re.match(r'A', cards[i]):
                soft_ace += 1
                value = 11
            else:
                value = int(cards[i])
            cards_value += value
            while cards_value > 21 and soft_ace > 0:
                cards_value -= 10
                soft_ace -= 1
        if cards_value >= 17:
            if cards_value > 21:
                index = 23
            elif cards_value == 21 and len(cards) == 2:
                index = 22
            else:
                index = cards_value
            dealer_pr[index] += (1.0/13)**(len(cards)-1)
        else:
            dealer_pr += dealer_hit(cards)
    return dealer_pr


if __name__ == '__main__':
    print("%2s" % ('PR'), end='')
    for o in DEALER_OL:
        print("%6s" % (o), end='')
    print('')
    for j in DEALER_IL:
        print("%s:" % (j), end='')
        f = dealer_hit([j])
        for o in DEALER_OL:
            if o == 'bust':
                o = '23'
            if o == 'bj':
                o = '22'
            print("%6.3f" % (f[int(o)]), end='')
        print('')
