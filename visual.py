#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Github: https://github.com/cetceeve/TwitterBot
# Fabian Zeiher
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D


# Visual Class to contain all fuctions relevant to display a full plot window
class Visual(object):

    # sample data to pupulate the plots if there are no parameters given on function call
    SAMPLE_LABELS = np.asarray(['hashtag_1', 'hashtag_2', 'hashtag_3', 'hashtag_4', 'hashtag_5'])
    SAMPLE_DATA = np.asarray([10, 50, 125, 250, 500])
    SAMPLE_LABELS_PIE = np.asarray(['Norway', 'Sweden', 'Great Britain', 'France', 'Japan'])
    SAMPLE_DATA_PIE = np.asarray([1000, 750, 500, 350, 200])
    SAMPLE_LABELS_SCATTER = np.asarray(['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'])
    SAMPLE_DATA_SCATTER = np.random.randn(24 * 7)
    SAMPLE_GEO_DATA = np.asarray([[0, 0], [90, 0], [-90, 0], [0, 180], [0, 90], [0, -90]])

    # initialize the window that can be populated by plots
    def __init__(self, geoDataCheck):
        if geoDataCheck:
            self.fig = plt.figure(figsize=(12, 5))
            # use a grid with 2 rows and 6 columns
            # position barplot in the upper left place of the plotwindow
            self.barplot = plt.subplot2grid((2, 5), (0, 0), rowspan=1)
            # position piechart in the upper row on the second column of the plotwindow
            # span 2 columns wide
            self.piechart = plt.subplot2grid((2, 5), (0, 1), colspan=2)
            # position scatterplot in the lower left place on the pot window
            # span 3 columns wide
            self.scatterplot = plt.subplot2grid((2, 5), (1, 0), colspan=3)
            # position plot on the right side of the pot window
            # span 2 rows and colums wide
            # initialize a 3 dimensional plot
            self.globalscatter = plt.subplot2grid((2, 5), (0, 3), colspan=2, rowspan=2, projection='3d')
        else:
            self.fig = plt.figure(figsize=(8, 5))
            # use a grid with 2 rows and 6 columns
            # position barplot in the upper left place of the plotwindow
            self.barplot = plt.subplot2grid((2, 3), (0, 0), rowspan=1)
            # position piechart in the upper row on the second column of the plotwindow
            # span 2 columns wide
            self.piechart = plt.subplot2grid((2, 3), (0, 1), colspan=2)
            # position scatterplot in the lower left place on the pot window
            # span 3 columns wide
            self.scatterplot = plt.subplot2grid((2, 3), (1, 0), colspan=3)

    # display the plot window using a tight layout
    # waits till that window is closed
    def display(self):
        plt.tight_layout()
        plt.show()

    # plot with horizontal bars
    # uses a list of strings (labels) and a list of integers (data)
    def create_barplot(self, labels=SAMPLE_LABELS, data=SAMPLE_DATA):
        # craft y_axes and turn barplot horizontal
        pos = np.arange(len(data))
        self.barplot.set_yticks(pos)
        self.barplot.set_yticklabels(labels)
        self.barplot.invert_yaxis()

        # set labels for axes and plot title
        self.barplot.set_xlabel('Hashtag Count')
        self.barplot.set_title('Cluster')
        # display the plot
        self.barplot.barh(pos, data)

    # pieplot to visualize percentages
    # uses list of strings (labels) and list of integers (data)
    def create_piechart(self, labels=SAMPLE_LABELS_PIE, data=SAMPLE_DATA_PIE):
        # set plot title
        self.piechart.set_title('Origin')
        # ensure that pie is drawn as a circle
        self.piechart.axis('equal')
        # display the plot
        self.piechart.pie(data, labels=labels, autopct='%1.2f%%', shadow=True, startangle=90)

    # scatterplot meant to display 168 datapoints over 7 days time
    # uses list of strings (labels) with 7 expected items
    # and list of integers (data) with 168 expected items
    def create_scatterplot(self, labels=SAMPLE_LABELS_SCATTER, data=SAMPLE_DATA_SCATTER):
        # sort data to display most recent datapoints to the right (timeline)
        labels, data = sort_weekdays(labels, data)
        # set label to the far right as 'today'
        labels[-1] = 'Now'

        # use no labels on major ticks
        # use a fixed set of labels on minor ticks
        self.scatterplot.xaxis.set_major_formatter(ticker.NullFormatter())
        self.scatterplot.xaxis.set_minor_formatter(ticker.FixedFormatter(labels))

        # compute exact position for minor ticks
        ticks = []
        pos = np.arange(len(data))
        for i in range(len(labels)):
            # position seven ticks between the major ticks
            tmp = int((i + 0.5) * len(data) // len(labels))
            ticks.append(pos[tmp])

        # set major ticks to work with 7 labels (8 ticks will be set)
        # set minor ticks on their positions
        self.scatterplot.xaxis.set_major_locator(ticker.IndexLocator(24, 0))
        self.scatterplot.xaxis.set_minor_locator(ticker.FixedLocator(ticks))

        # hide minor tick markers
        for tick in self.scatterplot.xaxis.get_minor_ticks():
            tick.tick1line.set_markersize(0)

        # set labels for axes and plot title
        self.scatterplot.set_ylabel('Hashtag Count')
        self.scatterplot.set_title('Performance')
        # display the plot
        self.scatterplot.scatter(pos, data, marker='.', s=1)
        self.scatterplot.plot(pos, data)

    # Unfortunatly our "TwitterCrawl" (API query) turned out to NOT return enouph
    # geo-coordinates to be used in this plot. Although the API does support geo-coordinates
    # they are normally empty. This is why the plot most of the time shows only some sample data.
    # ----->  The 'globalscatter' function can be seen as a Tech Demo  <-----

    # 3D plot that displays a spherical worldmap and up to 100 geo-coordinates
    # uses 2D Array of geo-coordinates
    def create_globalscatter(self, geoData=SAMPLE_GEO_DATA, tracker=0):
        # list with all necessary datasets to populate the spherical worldmap with continents
        loadList = ['america.csv', 'australia.csv', 'africa.csv',
                    'antarctica.csv', 'greenland.csv', 'europe_asia.csv']

        # populate worldmap with continents
        # load every continent from loadList
        for i in range(len(loadList)):
            # load geo-coordinates from csv file
            data = np.genfromtxt(loadList[i], delimiter=',')
            # convert geo-coordinates to xyz-coordinates
            x_array, y_array, z_array = dataconverter(data)
            # display all datapoints of one dataset
            self.globalscatter.scatter(x_array, y_array, z_array, c='b', marker='.', s=1)
            # connect all datapoints in one dataset with lines
            self.globalscatter.plot(x_array, y_array, z_array, color='b')

        if tracker:
            # coordinates from twitter crawl have the position of longitude and latitude reversed
            # swich position of lonitude and latitude
            geoDataCorrection = np.zeros([len(geoData), 2])
            geoDataCorrection[:, 0] = geoData[:, 1]
            geoDataCorrection[:, 1] = geoData[:, 0]
            # convert corrected geo-coordinates from twitter crawl to xyz-coordinates
            x_array, y_array, z_array = dataconverter(geoDataCorrection)
        else:
            # convert geo-coordinates from sample data to xyz-coordinates
            x_array, y_array, z_array = dataconverter(geoData)
            self.globalscatter.text2D(0.415, 0.18, "Sample Data",
                                      transform=self.globalscatter.transAxes)

        # display all datapoints from twitter crawl
        self.globalscatter.scatter(x_array, y_array, z_array, c='r', marker='o', s=3)

        # set plot title
        self.globalscatter.set_title('Geo Data')
        # ensure that a globe is displayed
        self.globalscatter.set_aspect('equal')
        # hide all axes
        self.globalscatter.axis('off')


# convert geo-coordinates to xyz-coordinates
def dataconverter(data):
    # conversion from longitude/latitude to xyz is done via simple pytagoras functions
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
