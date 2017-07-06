#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_LABELS = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
SAMPLE_DATA = [1,2,3,4,5,6,7]
SAMPLE_LABELS_PIE = ['Norway', 'Sweden', 'Great Britain', 'France',  'Japan']
SAMPLE_DATA_PIE = [1000, 750, 500, 350, 100]


def barplot(labels=SAMPLE_LABELS,data=SAMPLE_DATA):
    fig, ax = plt.subplots()

    pos=np.arange(len(data))
    ax.set_xticks(pos)
    ax.set_xticklabels(labels)
    ax.bar(pos,data)
    ax.set_ylabel('Hashtaganzahl')
    ax.set_title('Hashtag Performance')

    plt.show()

def piechart(labels=SAMPLE_LABELS_PIE,data=SAMPLE_DATA_PIE):
    fig1, ax1 = plt.subplots()

    ax1.pie(data, labels=labels, autopct='%1.2f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
