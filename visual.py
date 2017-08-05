#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D

# sample data to pupulate the plots if there are no parameters given on function call
SAMPLE_LABELS = np.asarray(['hashtag_1', 'hashtag_2', 'hashtag_3', 'hashtag_4', 'hashtag_5'])
SAMPLE_DATA = np.asarray([10, 50, 125, 250, 500])
SAMPLE_LABELS_PIE = np.asarray(['Norway', 'Sweden', 'Great Britain', 'France', 'Japan'])
SAMPLE_DATA_PIE = np.asarray([1000, 750, 500, 350, 200])
SAMPLE_LABELS_SCATTER = np.asarray(['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'])
SAMPLE_DATA_SCATTER = np.random.randn(24 * 7)
SAMPLE_GEO_DATA = np.asarray([[0, 0], [90, 0], [-90, 0], [0, 180], [0, 90], [0, -90]])


# Visual Class to contain all fuctions relevant to display a full plot window
class Visual(object):
    # initialize the window that can be populated by plots
    def __init__(self):
        fig = plt.figure(figsize=(13, 5))

    # display the plot window using a tight layout
    # waits till that window is closed
    def display(self):
        plt.tight_layout()
        plt.show()

    # plot with horizontal bars
    # uses a list of strings (labels) and a list of integers (data)
    def barplot(self, labels=SAMPLE_LABELS, data=SAMPLE_DATA):
        # use a grid with 2 rows and 6 columns
        # position plot in the upper left place of the plotwindow
        ax1 = plt.subplot2grid((2, 6), (0, 0), rowspan=1)

        # craft y_axes and turn barplot horizontal
        pos = np.arange(len(data))
        ax1.set_yticks(pos)
        ax1.set_yticklabels(labels)
        ax1.invert_yaxis()

        # set labels for axes and plot title
        ax1.set_xlabel('Hashtag Count')
        ax1.set_title('Cluster')
        # display the plot
        ax1.barh(pos, data)

    # pieplot to visualize percentages
    # uses list of strings (labels) and list of integers (data)
    def piechart(self, labels=SAMPLE_LABELS_PIE, data=SAMPLE_DATA_PIE):
        # use a grid with 2 rows and 6 columns
        # position plot in the upper row on the second column of the plotwindow
        # span 2 columns wide
        ax2 = plt.subplot2grid((2, 6), (0, 1), colspan=2)

        # set plot title
        ax2.set_title('Origin')
        # ensure that pie is drawn as a circle
        ax2.axis('equal')
        # display the plot
        ax2.pie(data, labels=labels, autopct='%1.2f%%', shadow=True, startangle=90)

    # scatterplot meant to display 168 datapoints over 7 days time
    # uses list of strings (labels) with 7 expected items
    # and list of integers (data) with 168 expected items
    def scatterplot(self, labels=SAMPLE_LABELS_SCATTER, data=SAMPLE_DATA_SCATTER):
        # use a grid with 2 rows and 6 columns
        # position plot in the lower left place on the pot window
        # span 3 columns wide
        ax3 = plt.subplot2grid((2, 6), (1, 0), colspan=3)

        # sort data to display most recent datapoints to the right (timeline)
        labels, data = sort_weekdays(labels, data)
        # set label to the far right as 'today'
        labels[-1] = 'Now'

        # use no labels on major ticks
        # use a fixed set of labels on minor ticks
        ax3.xaxis.set_major_formatter(ticker.NullFormatter())
        ax3.xaxis.set_minor_formatter(ticker.FixedFormatter(labels))

        # compute exact position for minor ticks
        ticks = []
        pos = np.arange(len(data))
        for i in range(len(labels)):
            # position seven ticks between the major ticks
            tmp = int((i + 0.5) * len(data) // len(labels))
            ticks.append(pos[tmp])

        # set major ticks to work with 7 labels (8 ticks will be set)
        # set minor ticks on their positions
        ax3.xaxis.set_major_locator(ticker.IndexLocator(24, 0))
        ax3.xaxis.set_minor_locator(ticker.FixedLocator(ticks))

        # hide minor tick markers
        for tick in ax3.xaxis.get_minor_ticks():
            tick.tick1line.set_markersize(0)

        # set labels for axes and plot title
        ax3.set_ylabel('Hashtag Count')
        ax3.set_title('Performance')
        # display the plot
        ax3.scatter(pos, data, marker='.', s=1)
        ax3.plot(pos, data)

    # Unfortunatly our "TwitterCrawl" (API query) turned out to NOT return enouph
    # geo-coordinates to be used in this plot. Although the API does support geo-coordinates
    # they are normally empty. This is why the plot most of the time shows only some sample data.
    # ----->  The 'globalscatter' function can be seen as a Tech Demo  <-----

    # 3D plot that displays a spherical worldmap and up to 100 geo-coordinates
    # uses 2D Array of geo-coordinates
    def globalscatter(self, geoData=SAMPLE_GEO_DATA):
        # list with all necessary datasets to populate the spherical worldmap with continents
        loadList = ['america.csv', 'australia.csv', 'africa.csv', 'antarctica.csv', 'greenland.csv', 'europe_asia.csv']

        # use a grid with 2 rows and 6 columns
        # position plot on the right side of the pot window
        # span 2 rows and colums wide
        # initialize a 3 dimensional plot
        ax4 = plt.subplot2grid((2, 6), (0, 3), colspan=3, rowspan=2, projection='3d')

        # populate worldmap with continents
        # load every continent from loadList
        for i in range(len(loadList)):
            # load geo-coordinates from csv file
            data = np.genfromtxt(loadList[i], delimiter=',')
            # convert geo-coordinates to xyz-coordinates
            x_array, y_array, z_array = dataconverter(data)
            # display all datapoints of one dataset
            ax4.scatter(x_array, y_array, z_array, c='b', marker='.', s=1)
            # connect all datapoints in one dataset with lines
            ax4.plot(x_array, y_array, z_array, color='b')

        # convert geo-coordinates from twitter crawl to xyz-coordinates
        x_array, y_array, z_array = dataconverter(geoData)
        # display all datapoints from twitter crawl
        ax4.scatter(x_array, y_array, z_array, c='r', marker='o', s=3)

        # set plot title
        ax4.set_title('Geo Data')
        # ensure that a globe is displayed
        ax4.set_aspect('equal')
        # hide all axes
        ax4.axis('off')


# convert geo-coordinates to xyz-coordinates
def dataconverter(data):
    # conversion from longitude/latide to xyz is done via simple pytagoras functions
    # radius not necessary since line 133 ensures that a globe gets displayed and axes are hidden
    an = np.cos(data[:, 0] * (np.pi / 180))
    x_array = np.cos(data[:, 1] * (np.pi / 180)) * an
    y_array = np.sin(data[:, 1] * (np.pi / 180)) * an
    z_array = np.sin(data[:, 0] * (np.pi / 180))
    # returns tuple of xyz-coordinates
    return x_array, y_array, z_array


# sort data to display most recent datapoints to the right (timeline)
def sort_weekdays(labels, data):
    # find the users current weekday
    today = datetime.datetime.today().weekday()

    # change order of weekdays
    daysSorted = labels[today + 1:]
    daysSorted = np.append(daysSorted, labels[:today + 1])

    # scale up the current weekday to according hour (not current hour)
    boundryHours = today * 24
    # change order of datapoints
    hoursSorted = data[boundryHours + 24:]
    hoursSorted = np.append(hoursSorted, data[:boundryHours + 24])

    # return the sorted data
    return daysSorted, hoursSorted
