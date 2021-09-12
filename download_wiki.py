from bs4 import BeautifulSoup
from urllib.request import urlopen
from random import choice
import os
import sys


def get_links(page_link):              # get from url: url of images and url's for another pages from wikipedia.

	with urlopen(page_link) as resp:
		response = BeautifulSoup(resp.read())
	
	imgs_link = clean_img_link(response)
	pages_link = clean_pages_link(response)

	return imgs_link , pages_link



def clean_img_link(response):

	imgs_raw_links = response.find_all('img')
	imgs_link = []
	for link in imgs_raw_links:
		if (link['src'][:6] == '/stati'):
			imgs_link.append(f"https://en.wikipedia.org{link['src']}")
		elif (link['src'][:4] == 'http'):
			imgs_link.append(link['src']) 	
		else:
			imgs_link.append(f"https:{link['src']}")

	return list(set(imgs_link))



def clean_pages_link(response):	

	pages_raw_links = response.find_all('a')
	pages_link = []
	for link in pages_raw_links:
		if (link.get('href') != None) and (link.get('href')[:5] == '/wiki'):
			pages_link.append(f"https://en.wikipedia.org{link.get('href')}")

	return pages_link



def download(img_link,name):               # download images from url of wikipedia to file with name of its page. 
	print(img_link)
	new_folder = (f"__save_wiki__/{name.split('/')[-1]}")
	if not os.path.exists(new_folder):	
		os.makedirs(new_folder)
	name_of_file = img_link.split('/')[-1][-250:]
	complete_directory = os.path.join(new_folder, name_of_file)
		
	with urlopen(img_link) as res:
		image = res.read()
	with open(complete_directory  , 'wb') as h_file:
		h_file.write(image)
			

def crawl(link,n):                       # recursion function to download images and get url to another pages with images.
			
	imgs_link, pages_link = get_links(link)
	for i in imgs_link:
		download(i, link)	
	new_link = choice(pages_link)	
	
	max_depth = int(sys.argv[2])

	if n < max_depth:
		n += 1
		print('new link')
		print(f"{new_link}\nnumber of page: {n}")
		crawl(new_link,n)
		

if len(sys.argv) != 3:
	print("error!\nenter 2 arguments!")
	exit()


start_link = sys.argv[1]
crawl(start_link,1)
