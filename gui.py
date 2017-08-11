#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Github: https://github.com/cetceeve/TwitterBot
# Fabian Zeiher
import Tkinter as tk


# root = Tk()
# app = App(root)
# root.mainloop()
class App(tk.Frame):
    def __init__(self, root):
        # frames
        self.auth_frame = tk.Frame(root)
        self.search_frame = tk.Frame(root)
        self.info_frame = tk.Frame(root)

        # variables auth
        self.string_instr_link = tk.StringVar()
        self.string_instr_pin = tk.StringVar()
        self.string_auth_info = tk.StringVar()
        self.string_auth_link = tk.StringVar()
        # variables search
        self.string_hashtag = tk.StringVar()
        self.string_amountoftweets = tk.StringVar()
        self.boolean_geodatacheck = tk.BooleanVar()
        # variable info
        self.string_info_msg = tk.StringVar()

        # create widgets
        self.create_labels()
        self.create_entries()
        self.create_buttons()
        self.create_checkbutton()

        # set fixed strings
        self.set_fix_strings()

    def create_labels(self):
        # auth labels
        self.label_instr_link = tk.Label(self.auth_frame, textvariable=self.string_instr_link)
        self.label_instr_pin = tk.Label(self.auth_frame, textvariable=self.string_instr_pin)
        self.label_auth_info = tk.Label(self.auth_frame, textvariable=self.string_auth_info)
        # search labels
        self.label_search_hashtag = tk.Label(self.search_frame, textvariable=self.string_hashtag)
        self.label_search_amountoftweets = tk.Label(self.search_frame, textvariable=self.string_amountoftweets)
        # info label
        self.label_info_msg = tk.Label(self.info_frame, textvariable=self.string_info_msg)

    def create_entries(self):
        # auth entries
        self.entry_auth_link = tk.Entry(self.auth_frame, textvariable=self.string_auth_link, width=90, state="readonly")
        self.entry_auth_pin = tk.Entry(self.auth_frame, width=20)
        # search entries
        self.entry_search_hashtag = tk.Entry(self.search_frame, width=30)
        self.entry_search_amountoftweets = tk.Entry(self.search_frame, width=30)

    def create_buttons(self):
        # auth Buttons
        self.button_auth_ok = tk.Button(self.auth_frame, text="OK")
        self.button_auth_tryag = tk.Button(self.auth_frame, text="Try Again!")
        # search Buttons
        self.button_search = tk.Button(self.search_frame, text="Search!")

    def create_checkbutton(self):
        self.checkbutton_geodatacheck = tk.Checkbutton(
            self.search_frame, text="Display GeoData in 3D Plot", variable=self.boolean_geodatacheck, onvalue=True, offvalue=False)

    # set fixed strings
    def set_fix_strings(self):
        # authentication instructions
        self.string_instr_link.set("Please enter the pin below and press 'OK'")
        self.string_instr_pin.set("Use this link to get an authentication pin:")
        # search describtion
        self.string_hashtag.set("Hashtag (without \"#\") :")
        self.string_amountoftweets.set("Tweets Number:")

    # frames
    def display_auth(self):
        # pack it all
        self.auth_frame.pack()
        self.label_instr_link.pack()
        self.entry_auth_link.pack()
        self.label_instr_pin.pack()
        self.entry_auth_pin.pack()
        self.button_auth_ok.pack()

    def display_search(self):
        # clean auth frame
        self.button_auth_ok.config(state=tk.DISABLED)
        self.string_auth_info.set("Authentication successful - please enter the hashtag to search for and press 'Search'")
        self.string_auth_info.config(fg="forest green")
        self.label_auth_info.pack()
        # display search frame
        self.search_frame.pack()
        self.label_search_hashtag.grid(row=0)
        self.label_search_amountoftweets.grid(row=1)
        self.entry_search_hashtag.grid(row=0, column=1)
        self.entry_search_amountoftweets.grid(row=1, column=1)
        self.checkbutton_geodatacheck.grid(row=2)
        self.button_search.grid(row=3)
        # initialize info_frame
        self.info_frame.pack()
        self.label_info_msg.pack()

    # errors and warnings
    def server_connection_error(self):
        self.string_auth_info.set("Server Connection failed! Please try again.")
        self.label_auth_info.config(fg='red')
        # packer
        self.button_auth_ok.pack_forget()
        self.button_auth_tryag.pack()
        self.label_auth_info.pack()

    def authentication_error(self):
        self.string_auth_info.set("Authentication failed! Please try again.")
        self.label_auth_info.config(fg='red')
        # packer
        self.button_auth_ok.pack_forget()
        self.button_auth_tryag.pack()
        self.label_auth_info.pack()

    # clear ui elements
    def clear_tryagain(self):
        self.button_auth_tryag.grid_forget()
        self.label_auth_info.grid_forget()
        self.button_auth_ok.pack()

    # info message
    def info_message(self, message):
        self.string_info_msg.set(message)
        self.label_info_msg.config(fg='red')
        # self.label_info_msg.pack()
