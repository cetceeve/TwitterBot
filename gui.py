#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Github: https://github.com/cetceeve/TwitterBot
# Fabian Zeiher
import Tkinter as tk


# class contains all variables and methods for the gui
class App(tk.Frame):
    def __init__(self, root):
        # frames stacked on top of each other.
        # primarily used to reduce grid sizes
        # authentication, search, information
        self.auth_frame = tk.Frame(root)
        self.search_frame = tk.Frame(root)
        self.info_frame = tk.Frame(root)
        # variables for the authentication frame
        self.string_instr_link = tk.StringVar()
        self.string_instr_pin = tk.StringVar()
        self.string_auth_info = tk.StringVar()
        self.string_auth_link = tk.StringVar()
        # variables for the search frame
        self.string_hashtag = tk.StringVar()
        self.string_amountoftweets = tk.StringVar()
        self.boolean_geodatacheck = tk.BooleanVar()
        # variable for the info frame
        self.string_info_msg = tk.StringVar()
        # the creation of all other widgets is placed in methods for visual clarity
        self.create_labels()
        self.create_entries()
        self.create_buttons()
        self.create_checkbutton()
        # some strings never change, set them upon initialization
        self.set_fix_strings()

    def create_labels(self):
        # labels for authentication frame
        self.label_instr_link = tk.Label(self.auth_frame, textvariable=self.string_instr_link)
        self.label_instr_pin = tk.Label(self.auth_frame, textvariable=self.string_instr_pin)
        self.label_auth_info = tk.Label(self.auth_frame, textvariable=self.string_auth_info)
        # labels for search frame
        self.label_search_hashtag = tk.Label(self.search_frame, textvariable=self.string_hashtag)
        self.label_search_amountoftweets = tk.Label(self.search_frame, textvariable=self.string_amountoftweets)
        # label for info frame
        self.label_info_msg = tk.Label(self.info_frame, textvariable=self.string_info_msg)

    def create_entries(self):
        # entries for authentication frame
        self.entry_auth_link = tk.Entry(self.auth_frame, textvariable=self.string_auth_link, width=90, state="readonly")
        self.entry_auth_pin = tk.Entry(self.auth_frame, width=20)
        # entries for search frame
        self.entry_search_hashtag = tk.Entry(self.search_frame, width=30)
        self.entry_search_amountoftweets = tk.Entry(self.search_frame, width=30)

    def create_buttons(self):
        # Buttons for authentication frame
        self.button_auth_ok = tk.Button(self.auth_frame, text="OK")
        self.button_auth_tryag = tk.Button(self.auth_frame, text="Try Again!")
        # Buttons for search frame
        self.button_search = tk.Button(self.search_frame, text="Search!")

    def create_checkbutton(self):
        # checkbutton for search frame
        self.checkbutton_geodatacheck = tk.Checkbutton(
            self.search_frame, text="Display geographical data in 3d plot", variable=self.boolean_geodatacheck, onvalue=True, offvalue=False)

    # some strings never change, set them upon initialization
    def set_fix_strings(self):
        # authentication instructions
        self.string_instr_link.set("Please enter the pin below and press 'OK'")
        self.string_instr_pin.set("Use this link to get an authentication pin:")
        # search describtion
        self.string_hashtag.set("Hashtag (without \"#\") :")
        self.string_amountoftweets.set("Tweets Number :")

    # methods binding several tkinter calls together
    # display all widgets for the authentication
    def display_auth(self):
        # pack all widgets in correct order
        self.auth_frame.pack()
        self.label_instr_link.pack()
        self.entry_auth_link.pack()
        self.label_instr_pin.pack()
        self.entry_auth_pin.pack()
        self.button_auth_ok.pack()

    # show user everything necessary for search
    def display_search(self):
        # show user that the authentication was successful
        self.button_auth_ok.config(state=tk.DISABLED)
        self.string_auth_info.set("Authentication successful - please enter the hashtag to search for and press 'Search'")
        self.label_auth_info.config(fg="forest green")
        self.label_auth_info.pack()
        # display all widgets for the search input using tkinker grid
        self.search_frame.pack()
        self.label_search_hashtag.grid(row=0, sticky=tk.E)
        self.label_search_amountoftweets.grid(row=1, sticky=tk.E)
        self.entry_search_hashtag.grid(row=0, column=1)
        self.entry_search_amountoftweets.grid(row=1, column=1)
        self.checkbutton_geodatacheck.grid(row=2, column=0, columnspan=2)
        self.button_search.grid(row=3, column=0, columnspan=2)
        # initialize the information area
        # note that the information frame only consists of one label
        # the string for this label is set in the info_message method
        self.info_frame.pack()
        self.label_info_msg.pack()

    # user feedback if something went wrong while trying to retrieve the authentication link
    def server_connection_error(self):
        self.string_auth_info.set("Server Connection failed! Please try again.")
        self.label_auth_info.config(fg='red')
        # show the retry button
        self.button_auth_ok.config(state=tk.DISABLED)
        self.label_auth_info.pack()
        self.button_auth_tryag.pack()

    # user feedback if twitter did not accept the authentication pin
    def authentication_error(self):
        self.string_auth_info.set("Authentication failed! Please try again.")
        self.label_auth_info.config(fg='red')
        # show the retry button
        self.button_auth_ok.config(state=tk.DISABLED)
        self.label_auth_info.pack()
        self.button_auth_tryag.pack()

    # when the authentication is tried again the retry stuff is cleared
    def clear_tryagain(self):
        self.button_auth_ok.config(state=tk.ACTIVE)
        self.button_auth_tryag.pack_forget()
        self.label_auth_info.pack_forget()

    # feed any string to the information label
    # if red is not appropriate the text color can also be configured
    def info_message(self, message, color='red'):
        self.string_info_msg.set(message)
        self.label_info_msg.config(fg=color)
