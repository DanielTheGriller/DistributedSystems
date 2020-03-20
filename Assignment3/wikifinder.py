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


""" This function does the searching and handling of
different links that are found on wikipedia pages. """
def find_path(start_page, end_page):
	path = Manager().dict()
	path[start_page] = [start_page]
	Q = deque([start_page])
	results = []
	while len(Q) != 0: # Run a loop as long as there is things on queue
		current_page = Q.popleft()
		links = get_pages(current_page)
		if links:
			pool = ThreadPool(processes=len(links)+1)
			for link in links:
				if (len(links) > 16): # This if-else pair is limiting the amount of workers to max 16
					workers = 16
				else:
					workers = len(links)
				pool = ThreadPool(processes=workers) # Generate a threadpool
				for link in links: # Iterate over the links and assign the workers to the task
					results.append(pool.apply(generate_path, args=(path, current_page, link, end_page)))
				pool.terminate()
				for result in results:
					if type(result) == list:
						return result
					if result: # Just to make sure that None values won't get to the queue
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
	s = BeautifulSoup(r.content, 'html.parser') # Parse the content to a readable form
	links = []
	for a in s.select('p a[href]'): # Iterate over the a href links found
		if(a['href'].startswith('/wiki/')): # Make sure that link is wiki-page
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
	start_page = 'https://en.wikipedia.org/wiki/' + str(input('Insert start page as it is in the url (for example Barack_Obama): '))
	end_page = 'https://en.wikipedia.org/wiki/' + str(input('Insert end page as it is in the url (for example Barack_Obama): '))
	# Confirm that both pages are real
	if confirm_page(start_page) and confirm_page(end_page):
		startTime = time.time()
		path = find_path(start_page, end_page) # Initiate the function to find the path
		endTime = time.time()
		elapsedTime = round(endTime-startTime,3)
		print('Found result in ' + str(elapsedTime) + ' seconds:')
		for link in path: # Print the result one link at a time
			print(link)
	else:
		print('Input is not a real wikipedia page')
