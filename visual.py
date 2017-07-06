#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_LABELS = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
SAMPLE_DATA = [1,2,3,4,5,6,7]


def barplot(labels=SAMPLE_LABELS,data=SAMPLE_DATA):
    fig, ax = plt.subplots()

    pos=np.arange(len(data))
    ax.set_xticks(pos)
    ax.set_xticklabels(labels)
    ax.bar(pos,data)
    ax.set_ylabel('Hashtaganzahl')
    ax.set_title('Hashtag Performance')
    plt.show()
