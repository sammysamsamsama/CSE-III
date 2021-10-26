#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import threading
import time
from datetime import datetime

from selenium import webdriver
from twilio.base.exceptions import TwilioException

import client
import Tn_Settings
from Texternet import Texternet

"""
This is the main file to run the Server

"""

## Catches an error if ID file is not present
try:
    curr_mess = pickle.load(open("id.in", "rb"))
except Exception as dam:
    curr_mess = datetime.today()

TN = Texternet()


## Checks for new responses to the server
while 1:
    try:
        ## Retrieves Messages
        messages = TN.getMessages(curr_mess)
        for x in messages:  ## Checks for new messages
            ## If new message is present, enter options
            if not x.date_sent == curr_mess:
                # If message is equal to links, change message type sent to links
                if x.body[:1] == "/":
                    try:
                        # Passing message to separate process to configure settings
                        t = threading.Thread(
                            name="child procs", target=Tn_Settings.theSlash, args=(x,)
                        )
                        t.setDaemon(True)
                        t.start()
                        print("Settings")
                    except Exception as e:
                        TN.sendMessage(
                            x.from_, "Change failed: Try searching something first"
                        )
                        pickle.dump(x.date_sent, open("id.in", "wb"))
                        print(e)

                # Else run search protocol in seperate process
                else:
                    # Passing message to separate process
                    t = threading.Thread(
                        name="child procs", target=client.sender, args=(x,)
                    )
                    t.setDaemon(True)
                    t.start()
                # print("j")
        if not len(messages) == 0:
            curr_mess = messages[0].date_sent

    except KeyError as key:
        if not len(messages) == 0:
            curr_mess = messages[0].date_sent
    except TwilioException as tw:
        print("Twilio has rejected us! We will relaunch in 30 secs")
        time.sleep(30)
    except ConnectionError as con:
        print(e)
        print("Trying again in 1 minute")
        time.sleep(60)
