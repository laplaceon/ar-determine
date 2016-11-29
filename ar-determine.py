from sklearn import tree
from bs4 import BeautifulSoup
import urllib2
import re
import pickle

baseUrl = "http://myanimelist.net/anime/"

expl_features = ['number of episodes', 'rating', 'age rating', 'action?', 'adventure?', 'comedy?', 'dementia?', 'drama?', 'ecchi?', 'romance?', 'sci-fi?', 'slice of life?']
expl_labels = ['good', 'meh', 'bad']

feedFeatures = pickle.load(open("ar-features", "rb"))
feedLabels = pickle.load(open("ar-labels", "rb"))

ratingMap = {"PG-13": 1, "R+": 2, "Rx": 3, "Rx": 4}
genresSet = ['action', 'adventure', 'comedy', 'dementia', 'drama', 'ecchi', 'romance', 'sci-fi', 'slice of life']

anime = raw_input("Enter ids seperated by commas: ").split(',')
features = []
titles = []

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
	
for series in anime:
	url = baseUrl + str(series)
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	episodes = soup.find('span', {'id': 'curEps'})
	rating = soup.find('span', {'itemprop': 'ratingValue'})
	title = soup.find('h1', {'class': 'h1'})
	titles.append(title.get_text())
	ageRating = getRating(soup.findAll('span', text = re.compile('Rating'))[0].parent.text)
	genres = getGenres(soup.findAll('span', text = re.compile('Genres'))[0].find_next_siblings("a"))
	featuresBlock = []
	featuresBlock.append(int(episodes.get_text()))
	featuresBlock.append(float(rating.get_text()))
	featuresBlock.append(int(ageRating))
	featuresBlock.extend(genres)
	features.append(featuresBlock)
	print(featuresBlock)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(feedFeatures, feedLabels)

from sklearn.externals.six import StringIO
import pydot

dot_data = StringIO()
tree.export_graphviz(clf, out_file=dot_data, feature_names=expl_features, class_names=expl_labels, filled=True, rounded=True, impurity=False)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("anime.pdf")

guesses = clf.predict(features)

i = 0

while i < len(titles):
	print(titles[i]),
	guess = guesses[i]
	if guess == 0:
		print("is a good anime")
	elif guess == 1:
		print("is a meh anime")
	else:
		print("is a bad anime")
	i = i + 1