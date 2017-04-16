import requests
from HTMLParser import HTMLParser
from collections import deque

language = 'it'
data = requests.get('https://support.riotgames.com/hc/{}'.format(language))
head_link = 'https://support.riotgames.com'
class LinkParser(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.queue = deque([])
		self.visited = {'https://support.riotgames.com/hc/{}'.format(language):True}
		self.results = []
		self.parent = None

	def handle_starttag(self,tag, attrs):
		if tag == 'a':
			for element in attrs:
				if element[0] == 'href':
					link = element[1]
					if link.startswith('/hc/{}'.format(language)) and 'signin' not in link:
						if '-' in link:
							link = link[:link.find('-')]
						elif '#' in link:
							link = link[:link.find('#')]
						if link not in self.visited:
							self.queue.append((link,self.parent))
							self.visited[link] = True
					elif not link.startswith('/hc/{}'.format(language)):
						if (self.parent != None and 'hc/{}'.format(language) in self.parent) and ((link.startswith('/hc/en-us') or link.startswith('https://support.riotgames.com/en-us'))):
							if 'request' not in link and 'change' not in link and link != 'https://support.riotgames.com/':
								self.results.append((link,self.parent))

parser = LinkParser()
parser.feed(data.text)
while parser.queue:
	print len(parser.queue)
	link,parent = parser.queue.popleft()
	if not link.startswith('http'):
		link = head_link + link
	data = requests.get(link)
	parser.parent = link
	parser.feed(data.text)


for item in parser.results:
	print item