#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

SAMPLE_LABELS = np.asarray(['hashtag_1', 'hashtag_2', 'hashtag_3', 'hashtag_4', 'hashtag_5'])
SAMPLE_DATA = np.asarray([10,50,125,250,500])
SAMPLE_LABELS_PIE = np.asarray(['Norway', 'Sweden', 'Great Britain', 'France',  'Japan'])
SAMPLE_DATA_PIE = np.asarray([1000, 750, 500, 350, 200])
SAMPLE_LABELS_SCATTER = np.asarray(['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'])
SAMPLE_DATA_SCATTER = np.random.randn(24*7)
SAMPLE_GEO_DATA = np.asarray([[0,0],[90,0],[-90,0],[0,180],[0,90],[0,-90]])

class Visual(object):
    def __init__(self):
        fig = plt.figure(figsize=(13,5))

    def display(self):
        plt.tight_layout()
        plt.show()

    def barplot(self, labels=SAMPLE_LABELS,data=SAMPLE_DATA):
        ax1 = plt.subplot2grid((2,6), (0,0), rowspan=1)

        pos=np.arange(len(data))
        ax1.set_yticks(pos)
        ax1.set_yticklabels(labels)
        ax1.invert_yaxis()

        ax1.set_xlabel('Hashtag Count')
        ax1.set_title('Cluster')
        ax1.barh(pos,data)

    def piechart(self, labels=SAMPLE_LABELS_PIE,data=SAMPLE_DATA_PIE):
        ax2 = plt.subplot2grid((2,6), (0,1), colspan=2)

        ax2.pie(data, labels=labels, autopct='%1.2f%%', shadow=True, startangle=55)
        ax2.set_title('Origin')
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    def scatterplot(self, labels=SAMPLE_LABELS_SCATTER, data=SAMPLE_DATA_SCATTER):
        ax3 = plt.subplot2grid((2,6), (1,0), colspan=3)

        ticks = []
        pos = np.arange(len(data))
        for i in range(len(labels)):
            tmp = int((i+0.5)*len(data)//len(labels))
            ticks.append(pos[tmp])

        ax3.set_xticks(ticks)
        ax3.set_xticklabels(labels)

        ax3.set_ylabel('Hashtag Count')
        ax3.set_title('Performance')
        ax3.scatter(pos,data)

    def globalscatter(self, geoData=SAMPLE_GEO_DATA):
        loadList = ['america.csv', 'australia.csv', 'africa.csv', 'antarctica.csv', 'greenland.csv', 'europe_asia.csv']

        ax4 = plt.subplot2grid((2,6), (0,3), colspan=3, rowspan=2, projection='3d')

        for i in range(len(loadList)):
            data = np.genfromtxt(loadList[i], delimiter=',')
            x_array, y_array, z_array = dataconverter(data)

            ax4.scatter(x_array, y_array, z_array, c='b', marker='.', s=1)
            ax4.plot(x_array, y_array, z_array, color='b')

        x_array, y_array, z_array = dataconverter(geoData)
        ax4.scatter(x_array, y_array, z_array, c='r', marker='o', s=3)

        ax4.set_title('Geo Data')
        ax4.set_aspect('equal')
        ax4.axis('off')

def dataconverter(data):
    an = np.cos(data[:,0]*(np.pi/180))
    x_array = np.cos(data[:,1]*(np.pi/180))*an
    y_array = np.sin(data[:,1]*(np.pi/180))*an
    z_array = np.sin(data[:,0]*(np.pi/180))
    return x_array, y_array, z_array
