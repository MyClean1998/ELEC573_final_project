import csv
import json
from itertools import dropwhile, takewhile
import networkx as nx
import matplotlib.pyplot as plt

def getdata(filename):
	with open(filename, "r") as csvfile:
		datareader = csv.reader(csvfile)
		yield next(datareader)
		for row in datareader:
				yield row

def extractSubstitutionData():
	# for i in range(10):
		# print(getdata("Play_by_Play_data_csv.csv"))
	with open("Play_by_Play_data_csv.csv", "r") as csvfile:
		with open("substitution_data_csv.csv", "w") as destfile:
			datareader = csv.reader(csvfile)
			datawriter = csv.writer(destfile)
			games = set()
			count = 0
			# print(next(datareader))
			datawriter.writerow(next(datareader))
			for row in datareader:
				# if not row[1] in games:
				# 	games.add(row[1])
				# 	# datawriter.writerow(row)
				# 	print(row)
				# count+=1
				# if count > 1000:
				# 	break
				if (row[3] == '8'):
					datawriter.writerow(row)

def extractSubstitutionDataYear(year):
	with open("substitution_data_csv.csv", "r") as csvfile:
		with open("substitution_data_" + year + "_csv.csv" , "w") as destfile:
			datareader = csv.reader(csvfile)
			datawriter = csv.writer(destfile)
			datawriter.writerow(next(datareader))
			for row in datareader:
				if row[1][1:3] == year:
					datawriter.writerow(row)

def saveToJson(dict, fileName):
	j = json.dumps(dict)
	f = open(fileName,"w")
	f.write(j)
	f.close()

def readFromJson(fileName):
	f = open(fileName,"r")
	f.read()

def parseDescription(row):
	# if teamid == '1610612756':
	# left_bracket = row.index("[")
	try:
		right_bracket = row.index("]")
		subText = "Substitution replaced by"
		# teamName = row[left_bracket + 1: right_bracket]
		# if (teamName == "SAS" or teamName == "SAN"):
		sub = row.index(subText)
		subEnd = sub + len(subText)
		p1 = row[right_bracket + 2: sub - 1]
		p2 = row[subEnd + 1: ]
		return p1, p2
	except:
		print(row)
	# print (teamName)

def isTeam(row):
	try:
		teamName = getTeamName(row)
		if (teamName == "SAS" or teamName == "SAN"):
			return True
	except:
		print(row)

	return False

def getSpurs():
	with open("substitution_data_csv.csv", "r") as csvfile:
		dict = {}
		datareader = csv.reader(csvfile)
		next(datareader)
		for row in datareader:
			if (isTeam(row[4])):
				p1, p2 = parseDescription(row[4])
				if not p1 in dict:
					dict[p1] = {}
				if not p2 in dict[p1]:
					dict[p1][p2] = 0
				dict[p1][p2] += 1
		# print("keys")
		# print (dict.keys())
		createGraph(dict)

def getTeamName(desc):
	left_bracket = desc.index("[")
	right_bracket = desc.index("]")
	teamName = desc[left_bracket + 1: right_bracket]
	return teamName

def getAllTeams18():
	with open("substitution_data_18_csv.csv", "r") as csvfile:
		teams = {}
		datareader = csv.reader(csvfile)
		next(datareader)
		for row in datareader:
			team = getTeamName(row[4])
			if not team in teams:
				teams[team] = {}
			p1, p2 = parseDescription(row[4])
			if not p1 in teams[team]:
				teams[team][p1] = {}
			if not p2 in teams[team][p1]:
				teams[team][p1][p2] = 0
			teams[team][p1][p2] += 1
	saveToJson(teams, "sub_18.json")

selected_players = ['White', 'Anderson', 'Green', 'Mills', 'Belinelli', 'Aldridge', 'Gasol', 'Forbes', 'Bertans', 'Murray', 'Gay', 'Poeltl', 'DeRozan', 'Cunningham']
players2014 =['Ginobili', 'Duncan', 'Parker', 'Bonner', 'Anderson', 'Splitter', 'Green', 'Leonard', 'Joseph', 'Diaw', 'Mills', 'Baynes', 'Belinelli']

selected_players = players2014

labels = {p: p for p in selected_players}

def createGraph(dict):
	G = nx.DiGraph()
	G.add_nodes_from(selected_players)
	for key in dict:
		if key in selected_players:
			for v in dict[key]:
				if v in selected_players and dict[key][v] > 50:
					G.add_edge(key, v, weight=dict[key][v])
	# print(G.in_degree)
	return G
	# options = {
	# 	# 'node_color': 'black',
	# 	'node_size': 100,
	# 	# 'width': 3,
	# 	'labels': labels,
	# }
	# nx.draw_spring(G, **options)
	# # nx.draw(G, **options)
	#
	# plt.show()

# def createGraphs():

# extractSubstitutionDataYear("18")
# getSpurs()
# getAllTeams18()
# parseDescription("(6:07)[SAS] White Substitution replaced by Mills", '1610612756')