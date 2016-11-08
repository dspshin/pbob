#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, re, time, traceback
from pprint import pprint
import sqlite3
import telepot
import urllib2
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup

ROOT = '/home/dsp/git/pbob/'

conn = sqlite3.connect(ROOT+'subscribe.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS subscribe( user TEXT, name TEXT, PRIMARY KEY(user) )')
conn.commit()

def sendMessage(user,msg):
	try:
		bot.sendMessage(user,msg)
	except:
		traceback.print_exc(file=sys.stdout)


def crawl():

	# get articles
	today = time.strftime('%Y%m%d')
	cur_hour = time.strftime('%H')

	url = 'http://supportportal.skplanet.com/Cafeteria/Interface/getMenu.aspx?command=getMenu'
	req = urllib2.Request( url )
	response = urllib2.urlopen(req)
	contents = response.read()
	soup = BeautifulSoup(contents, 'html.parser')
	#print soup
	#print soup.date.string, today
	if soup.date.string != today:
		return

	msg=''

	for menu in soup.find_all('menu'):
		menuname = menu.menuname.string
		isLunch = menuname.startswith(u"중식")
		isDinner = menuname.startswith(u"석식")
		if cur_hour == '17' and isDinner:
			pass
		elif cur_hour == '11' and isLunch:
			pass
		else:
			continue

		msg += menuname+'\n'
		materials = []
		for material in menu.find_all('material'):
			materials.append(material.string)
		msg += ",".join(materials)+"\n\n"
		#msg += menu.country.string+'\n\n'

	#print msg

	users = []
	c.execute('SELECT user FROM subscribe') # get subscribing users
	for data in c.fetchall():
		users.append( data[0] )

	#print users

	for user in users:
		sendMessage( user, msg )

		#delay
		time.sleep(1)

now=datetime.now()

TOKEN = sys.argv[1]
print '[',now,']' #'received token :', TOKEN

bot = telepot.Bot(TOKEN)
pprint( bot.getMe() )

crawl()


