#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import hashlib
import json
import urllib
from collections import OrderedDict
#you might can delete the above
from twilio.rest import Client

class Twillio:
	
	account_sid = 'ACaf9b4eb8c9e433d2b3a42485c8f1f6c0'
	auth_token = '89dcdd5bf02fdd6c8ba365ba3e961def'

	def __init__(self):
		self.client = Client(account_sid, auth_token)
		self.Login = True
		self.username = None
		self.userInfo = None

	def getInfoAboutUser(self):
		if self.Login == False:
			return False

		return self.client.usage.records.last_month.list()

	def getMessages(self, start_message_id = 24340869891, page_size = 5, get_all = 1):
		if self.Login == False:
			return False

		node = 'users/%s/messages'%(self.username)
		query = '?client_type=TN_ANDROID&client_id=%s&get_all=%s&page_size=%s&start_message_id=%s'%(self.Login, get_all, page_size, start_message_id)
		sign = self.genSignature("GET", node, query)
		req = self.sendReq("GET", "%s%s%s"%(self.API_URL, node, query), sign)
		f = open("site.txt", 'w')
		f.write("GET" + " %s%s%s"%(self.API_URL, node, query) + " %s"%sign)
		f = open("json.txt", 'w')
		json.dump(req, f)
		return req

	def getWallet(self):
		if self.Login == False:
			return False

		node = 'users/%s/wallet'%(self.username)
		query = '?client_type=TN_ANDROID&client_id=%s'%(self.Login)
		sign = self.genSignature("GET", node, query)
		req = self.sendReq("GET", "%s%s%s"%(self.API_URL, node, query), sign)
		return req

	def sendMessage(self, number, msg):
		# return if logged in
		if self.Login == False:
			return False

		message = self.client.messages \
                        .create(
                                 body=msg,
                                 from_='+19565405619',
                                 to='+' + number
                        )

		return message.sid
	
	def sendImage(self, number, img):
		# return if logged in
		if self.Login == False:
			return False

		message = self.client.messages \
                        .create(
                                 # body='This is the ship that made the Kessel Run in fourteen parsecs?',
                                 from_='+19565405619',
                                 media_url='https://terxernet.tk/images/' + img,
                                 to='+' + number
                        )
		
		return message.sid
	
	def changeFullName(self, first_name, last_name):
		# return if logged in
		if self.Login == False:
			return False

		node = 'users/%s'%(self.username)
		query = '?client_type=TN_ANDROID&client_id=%s'%(self.Login)

		msgData = OrderedDict([
			('first_name', first_name),
			('last_name', last_name)
			])
		jsonData = self.genJson(msgData)
		sign = self.genSignature("PATCH", node, query + jsonData)
		req = self.sendReq("PATCH", "%s%s%s"%(self.API_URL, node, query), sign, jsonData)
		if req == "[]":
			return True
		else:
			return False

	def changeEmail(self, email):
		# return if logged in
		if self.Login == False:
			return False

		node = 'users/%s'%(self.username)
		query = '?client_type=TN_ANDROID&client_id=%s'%(self.Login)

		msgData = OrderedDict([
			('email', email)
			])
		jsonData = self.genJson(msgData)
		sign = self.genSignature("PATCH", node, query + jsonData)
		req = self.sendReq("PATCH", "%s%s%s"%(self.API_URL, node, query), sign, jsonData)
		if req == "[]":
			return True
		else:
			return False

	def changePassword(self, old_password, new_password):
		# return if logged in
		if self.Login == False:
			return False

		node = 'users/%s'%(self.username)
		query = '?client_type=TN_ANDROID&client_id=%s'%(self.Login)

		msgData = OrderedDict([
			('old_password', old_password),
			('password', new_password)
			])
		jsonData = self.genJson(msgData)
		sign = self.genSignature("PATCH", node, query + jsonData)
		req = self.sendReq("PATCH", "%s%s%s"%(self.API_URL, node, query), sign, jsonData)
		if req == "[]":
			return True
		else:
			return False

if __name__ == "__main__":
	print("can't run this file.")
