#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calculate player PR"""

__author__ = 'Fei Deng'

# Imports
import re
import numpy as np
# import matplotlib.pyplot as plt
# import os
# import sys
import dealer_bj

SOFT = 0
CARD_LIST = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
if SOFT == 1:
    PLAYER_IL = ['13', '14', '15', '16', '17', '18', '19', '20', '21', 'bj']
else:
    PLAYER_IL = [
        '8', '9', '10', '11', '12', '13', '14',
        '15', '16', '17', '18', '19', '20', '21', 'bj'
    ]
PLAYER_OL = [
    '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', 'bust'
]
DEALER_IL = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'A']
DEALER_OL = ['17', '18', '19', '20', '21', 'bust']

N = 24
WIN = np.eye(N, N)
for i in range(N):
    for j in range(N):
        if i == N - 1:
            WIN[i, j] = -1
        elif j == N - 1:
            WIN[i, j] = 1
        elif i < j:
            WIN[i, j] = -1
        elif i > j:
            WIN[i, j] = 1
        else:
            WIN[i, j] = 0


def player_hit(player_hand, soft, double):
    """Get probability of hit"""
    player_pr = np.zeros(24)
    for new_card in CARD_LIST:
        cards_value = 0
        soft_ace = soft
        if isinstance(player_hand[0], list):
            cards = player_hand[0] + [new_card]
        else:
            cards = player_hand + [new_card]
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
        if (soft_ace > 0 and cards_value >= 18) or \
           (soft_ace <= 0 and cards_value >= 12) or double:
            if cards_value > 21:
                index = 23
            elif cards_value == 21 and len(cards) == 2:
                index = 22
            else:
                index = cards_value
            player_pr[index] += (1.0/13)**(len(cards)-1)
        else:
            player_pr += player_hit(cards, soft_ace, False)
    return player_pr


if __name__ == '__main__':
    print("%-3s" % ('BJS'), end='')
    for j in DEALER_IL:
        print("%20s" % (j), end='')
    print('')
    for i in PLAYER_IL:
        print("%2s:" % (i), end='')
        if i == 'bj':
            i = '22'
        player_pr_S = np.zeros(24)
        if len(i) > 1 and i[0] == 'A':
            index = 11 + int(i[1])
        else:
            index = int(i)
        player_pr_S[index] = 1
        player_pr_H = player_hit([i], SOFT, False)
        player_pr_D = player_hit([i], SOFT, True)
        for j in DEALER_IL:
            dealer_pr = dealer_bj.dealer_hit([j])
            x = np.dot(dealer_pr, WIN.T)
            return_S = np.dot(player_pr_S, x.T) * 100
            return_H = np.dot(player_pr_H, x.T) * 100
            return_D = np.dot(player_pr_D, x.T) * 200
            print("%6.1f" % (return_S), end='')
            print("%6.1f" % (return_H), end='')
            print("%6.1f" % (return_D), end='')
            action = 'H'
            return_A = return_H
            if return_D > return_A:
                action = 'D'
                return_A = return_D
            if return_S > return_A:
                action = 'S'
                return_A = return_S
            if return_A < -50 and int(i) > 11:
                action = 'R'
            print("%2s" % (action), end='')
        print('')
