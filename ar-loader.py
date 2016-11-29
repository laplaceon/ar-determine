import pickle
from bs4 import BeautifulSoup
import urllib2
import re

baseUrl = "http://myanimelist.net/anime/"

feedFeatures = {0: [2167, 30, 5114, 1, 47, 43, 9790, 1840, 355, 1222, 6408, 3299, 8525, 51, 4382], 1: [5112, 9330, 5958, 3470, 6773, 2034, 7817, 195, 4551, 8481, 1965], 2: [2476, 1639, 1200, 9587, 30544, 5877, 7858, 147, 11617, 3503, 10611, 1723]}
# good = 0 2 = bad
ratingMap = {"PG-13": 1, "R+": 2, "Rx": 3, "Rx": 4}
genresSet = ['action', 'adventure', 'comedy', 'dementia', 'drama', 'ecchi', 'romance', 'sci-fi', 'slice of life']

features = []
labels = []

def getRating(ratingText):
	for ratingKey in ratingMap:
		if ratingKey in ratingText:
			return ratingMap[ratingKey]
	return 0

def getGenres(genres):
	genreValues = []
	filteredGenres = []
	for genre in genres:
		filteredGenre = genre.get_text().lower()
		filteredGenres.append(filteredGenre)
	for genre in genresSet:
		if genre in filteredGenres:
			genreValues.append(1)
		else:
			genreValues.append(0)
	return genreValues

for category in feedFeatures:
	categoryArray = feedFeatures[category]
	for id in categoryArray:
		url = baseUrl + str(id)
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page.read())
		episodes = soup.find('span', {'id': 'curEps'})
		rating = soup.find('span', {'itemprop': 'ratingValue'})
		ageRating = getRating(soup.findAll('span', text = re.compile('Rating'))[0].parent.text)
		genres = getGenres(soup.findAll('span', text = re.compile('Genres'))[0].find_next_siblings("a"))
		featuresBlock = []
		featuresBlock.append(int(episodes.get_text()))
		featuresBlock.append(float(rating.get_text()))
		featuresBlock.append(int(ageRating))
		featuresBlock.extend(genres)
		labels.append(category)
		features.append(featuresBlock)

pickle.dump(features, open("ar-features", "wb"))
pickle.dump(labels, open("ar-labels", "wb"))