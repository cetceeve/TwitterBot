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
        self.string_amountoftweets = tk.StringVar()
        self.string_hashtag = tk.StringVar()
        self.boolean_geodatacheck = tk.BooleanVar()
        # variable info
        self.string_info_msg = tk.StringVar()

        # create widgets
        self.create_labels()
        self.create_entries()
        self.create_buttons()
        self.create_checkbutton()
        # packer
        self.auth_packer()

    def create_labels(self):
        # auth labels
        self.label_instr_link = tk.Label(self.auth_frame, textvariable=self.string_instr_link)
        self.label_instr_pin = tk.Label(self.auth_frame, textvariable=self.string_instr_pin)
        self.label_auth_info = tk.Label(self.auth_frame, textvariable=self.string_auth_info)
        # search labels
        self.label_amountoftweets = tk.Label(self.search_frame, textvariable=self.string_amountoftweets)
        self.label_hashtag = tk.Label(self.search_frame, textvariable=self.string_hashtag)
        # info label
        self.label_info_msg = tk.Label(self.info_frame, textvariable=self.string_info_msg)

    def create_entries(self):
        # auth entries
        self.entry_auth_link = tk.Entry(self.auth_frame, textvariable=self.string_auth_link, width=90, state="readonly")
        self.entry_auth_pin = tk.Entry(self.auth_frame, width=20)
        # search entries
        self.entry_search_amountoftweets = tk.Entry(self.search_frame, width=30)
        self.entry_search_hashtag = tk.Entry(self.search_frame, width=30)

    def create_buttons(self):
        # auth Buttons
        self.button_auth_ok = tk.Button(self.auth_frame, text="OK")
        self.button_auth_tryag = tk.Button(self.auth_frame, text="Try Again!")
        # search Buttons
        self.button_search = tk.Button(self.search_frame, text="Search!")

    def create_checkbutton(self):
        self.checkbutton_geodatacheck = tk.Checkbutton(
            self.search_frame, text="Display GeoData in 3D Plot", variable=self.boolean_geodatacheck, onvalue=True, offvalue=False)

    def auth_packer(self):
        self.auth_frame.pack()
        self.label_instr_link.pack()
        self.entry_auth_link.pack()
        self.label_instr_pin.pack()
        self.entry_auth_pin.pack()
        self.button_auth_ok.pack()
