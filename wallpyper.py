import praw
import ctypes
import random
import os
import urllib
import time
import threading
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

USER_AGENT = 'Wallpyper 1.0.0 by /u/Kai_'
SPI_SETDESKWALLPAPER = 20
LIMIT = 100

history = {}

r = praw.Reddit(user_agent = USER_AGENT)

def change(INTERVAL = 10, SUBNAMES = ['wallpaper', 'wallpapers'], TERMS = [''], AND_SEARCH = False, SORT = 'top', PERIOD = 'month', RES = ['1920x1080'], REPEAT = False, NSFW = False):
	print "Starting..."
	selected = False

	subnames = '+'.join(SUBNAMES)
	operator = ' AND ' if AND_SEARCH == True else ' OR '
	query = '({0}) AND ({1}) AND nsfw:{2}'.format(operator.join(TERMS), ' OR '.join(RES), int(NSFW))

	print "Searching with query: {0}".format(query)

	submissions = r.search(query, subreddit=subnames, sort=SORT, period=PERIOD, limit=max(1000,LIMIT))
	results = [x for x in submissions]

	while not selected:
		if not results:
			print "No new results found, exiting."
			exit()
		result = random.choice(results)
		results.remove(result)
		print "Trying: {0}".format(result.title)
		if result.url.startswith("http://i.imgur.com") and (REPEAT or result.url not in history):
			selected = True

	print "Selected: {0}".format(result.title)
	history[result.url] = result.title
	print history

	path = urllib.urlretrieve(result.url)[0]
	time.sleep(1)
	ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path, 2)
	time.sleep(1)
	os.remove(path)
	threading.Timer(max(INTERVAL * 60,15), change, [INTERVAL, SUBNAMES, TERMS, AND_SEARCH, SORT, PERIOD, RES, REPEAT, NSFW]).start()

change()
