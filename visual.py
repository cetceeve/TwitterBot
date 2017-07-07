#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json

SAMPLE_LABELS = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
SAMPLE_DATA = [1,2,3,4,5,6,7]
SAMPLE_LABELS_PIE = ['Norway', 'Sweden', 'Great Britain', 'France',  'Japan']
SAMPLE_DATA_PIE = [1000, 750, 500, 350, 100]
SAMPLE_LABELS_SCATTER = np.arange(24*7-1)
SAMPLE_DATA_SCATTER = np.random.randn(24*7-1)
SAMPLE_GEO_DATA = np.asarray([[12,125],[89,105],[27,110],[24,113]])

class Visual(object):
    def barplot(self, labels=SAMPLE_LABELS,data=SAMPLE_DATA):
        fig, ax = plt.subplots()

        pos=np.arange(len(data))
        ax.set_xticks(pos)
        ax.set_xticklabels(labels)
        ax.bar(pos,data)
        ax.set_ylabel('Hashtaganzahl')
        ax.set_title('Hashtag Performance')

        plt.show()

    def piechart(self, labels=SAMPLE_LABELS_PIE,data=SAMPLE_DATA_PIE):
        fig1, ax1 = plt.subplots()

        ax1.pie(data, labels=labels, autopct='%1.2f%%', shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()

    def scatterplot(self, labels=SAMPLE_LABELS_SCATTER, data=SAMPLE_DATA_SCATTER):
        fig, ax = plt.subplots()

        days = np.arange(len(labels))
        #ax.set_xticks(days)
        #ax.set_xticklabels(labels)
        ax.scatter(days,data)

        plt.show()

    def globalscatter(self, geoData=SAMPLE_GEO_DATA):
        loadList = ['global_boundries.csv', 'australien.csv']

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for i in range(len(loadList)):
            data = np.genfromtxt(loadList[i], delimiter=',')
            x_array, y_array, z_array = dataconverter(data)

            ax.scatter(x_array, y_array, z_array, c='b', marker='.')
            ax.plot(x_array, y_array, z_array, c='b')

        x_array, y_array, z_array = dataconverter(geoData)
        ax.scatter(x_array, y_array, z_array, c='r', marker='^')

        ax.set_aspect('equal')
        ax.axis('off')
        plt.show()

def dataconverter(data):
    an = np.cos(data[:,0]*(np.pi/180))*1
    x_array = np.cos(data[:,1]*(np.pi/180))*an
    y_array = np.sin(data[:,1]*(np.pi/180))*an
    z_array = np.sin(data[:,0]*(np.pi/180))*1
    return x_array, y_array, z_array
