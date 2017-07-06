#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

SAMPLE_LABELS = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
SAMPLE_DATA = [1,2,3,4,5,6,7]
SAMPLE_LABELS_PIE = ['Norway', 'Sweden', 'Great Britain', 'France',  'Japan']
SAMPLE_DATA_PIE = [1000, 750, 500, 350, 100]
SAMPLE_LABELS_SCATTER = np.arange(24*7-1)
SAMPLE_DATA_SCATTER = np.random.randn(24*7-1)


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

def scatterplot(labels=SAMPLE_LABELS_SCATTER, data=SAMPLE_DATA_SCATTER):
    fig, ax = plt.subplots()

    days = np.arange(len(labels))
    #ax.set_xticks(days)
    #ax.set_xticklabels(labels)
    ax.scatter(days,data)

    plt.show()

def globalscatter():
    data = np.genfromtxt('sample_geo_data_large.csv', delimiter=',')

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    an = np.sin(data[:,1]*(np.pi/180))*10
    x_array = np.cos(data[:,0]*(np.pi/180))*an
    y_array = np.sin(data[:,0]*(np.pi/180))*an
    z_array = np.cos(data[:,1]*(np.pi/180))*10
    ax.scatter(x_array, y_array, z_array, marker='.')
    #ax.axis('equal')
    ax.set_aspect('equal')

    plt.show()
