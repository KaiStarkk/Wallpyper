import praw
import ctypes
import random
import os
import urllib
import time
import threading

USER_AGENT = 'Wallpyper 1.0.0 by /u/Kai_'
SPI_SETDESKWALLPAPER = 20
LIMIT = 200

history = []

r = praw.Reddit(user_agent = USER_AGENT)

def change(INTERVAL = 10, SUBNAMES = ['wallpaper', 'wallpapers'], TERMS = [''], AND_SEARCH = False, SORT = 'top', PERIOD = 'month', RES = ['1920x1080'], NSFW=False):
	print "Starting..."
	threading.Timer(INTERVAL * 60, change).start()

	subnames = '+'.join(SUBNAMES)
	operator = ' AND ' if AND_SEARCH == True else ' OR '
	query = '({0}) AND ({1}) AND nsfw:{2}'.format(operator.join(TERMS), ' OR '.join(RES), int(NSFW))

	print "Searching with query: {0}".format(query)

	submissions = r.search(query, subreddit=subnames, sort=SORT, period=PERIOD, limit=LIMIT)
	results = [x for x in submissions]
	result = random.choice(results)
	results.remove(result)
	print "Trying: {0}".format(result.title)

	while result.title in history or not result.url.startswith('http://i.imgur.com'):
		if not results:
			print "No results found, exiting."
			exit()
		result = random.choice(results)
		results.remove(result)
		print "Trying: {0}".format(result.title)

	print "Selected: {0}".format(result.title)
	history.append(result.title)
	print history

	path = urllib.urlretrieve(result.url)[0]
	time.sleep(1)
	ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path, 2)
	time.sleep(1)
	os.remove(path)

change()
