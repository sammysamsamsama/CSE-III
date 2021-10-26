#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import json
import urllib
from collections import OrderedDict
from datetime import datetime

import requests
from twilio.rest import Client


class Texternet:
    """This is the class that manages communication between the Texternet server and the Twilio API."""

    def __init__(self):
        """
                This method sets up a new connection to the Twilio API.

                """
        self.account_sid = "ACaf9b4eb8c9e433d2b3a42485c8f1f6c0"
        self.auth_token = "89dcdd5bf02fdd6c8ba365ba3e961def"
        self.Login = False
        self.username = None
        self.userInfo = None
        self.client = Client(self.account_sid, self.auth_token)

    def getMessages(self, date):
        """
                Using a given time, you get the messages from that point on.
                
                Parameters
                ----------
                date : datetime.datetime
                    The date of the starting point.
                    
                """
        messages = self.client.messages.list(
            date_sent_after=date,
            to="+19565405619",
        )
        return messages

    def sendMessage(self, number, msg):
        """
                Sends a given text message to a given number.
                
                Parameters
                ----------
                number : str
                    given phone number preceded by the counry code. (ex. '+18171111111')

                msg : str
                    The message to be sent to the specified number.

                """
        message = self.client.messages.create(body=msg, from_="+19565405619", to=number)
        return message.sid

    def sendImage(self, number, file):
        """
                Sends a given file to a given number.
                
                Parameters
                ----------
                number : str
                    given phone number preceded by the counry code. (ex. '+18171111111')

                file : str
                    The name of the file to be sent to the specified number.

                """
        message = self.client.messages.create(
            from_="+19565405619",
            media_url=file,
            to=number,
        )
        return message.sid


if __name__ == "__main__":
    print("can't run this file.")
