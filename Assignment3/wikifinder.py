""" Daniel Linna
	0509355
	29.2.2020 """
import requests
from bs4 import BeautifulSoup
import threading
from multiprocessing import Manager
from multiprocessing.pool import ThreadPool
from collections import deque
import time


def find_path(start_page, end_page):
	path = Manager().dict()
	path[start_page] = [start_page]
	Q = deque([start_page])
	results = []
	while len(Q) != 0:
		current_page = Q.popleft()
		links = get_pages(current_page)
		if links:
			pool = ThreadPool(processes=4)
			for link in links:
				results.append(pool.apply(generate_path, args=(path, current_page, link, end_page)))
			pool.terminate()
			for result in results:
				if type(result) == list:
					return result
				Q.append(result)
		else:
			continue



""" This function checks if the given link
leads to the end page. If not, it generates a new
path from start page to the link for further processing. """
def generate_path(path, current_page, link, end_page):
	if link == end_page:
		return path[current_page] + [link]
	if link not in path:
		path[link] = path[current_page] + [link]
		return link


""" This function gets all the links on the current wikipedia page """
def get_pages(URL):
	try:
		r = requests.get(URL)
	except:
		return None
	s = BeautifulSoup(r.content, 'html.parser')
	links = []
	for a in s.select('p a[href]'):
		if(a['href'].startswith('/wiki/')):
			link = 'https://en.wikipedia.org' + a['href']
			links.append(link)
	return links


""" Just a simple function which does the request to the parameter
URL and returns 1 if it's a real page and 0 if not """
def confirm_page(URL):
	if requests.get(URL):
		return 1
	else:
		return 0


if __name__ == '__main__':
	# Ask for start and end pages as the last part of the URL
	#start_page = 'https://en.wikipedia.org/wiki/' + str(input('Insert start page as it is in the url (for example Barack_Obama): '))
	#end_page = 'https://en.wikipedia.org/wiki/' + str(input('Insert end page as it is in the url (for example Barack_Obama): '))
	# TEMPORARY VALUES, PLEASE DELETE
	start_page = 'https://en.wikipedia.org/wiki/Renault'
	end_page = 'https://en.wikipedia.org/wiki/Barack_Obama'
	# Confirm that both pages are real
	if confirm_page(start_page) and confirm_page(end_page):
		startTime = time.time()
		path = find_path(start_page, end_page)
		endTime = time.time()
		elapsedTime = endTime-startTime
		print('Found result in ' + str(elapsedTime) + ' seconds:')
		for link in path:
			print(link)
	else:
		print('Input is not a real wikipedia page')
