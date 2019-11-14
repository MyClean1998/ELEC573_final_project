import csv
import json
from itertools import dropwhile, takewhile
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


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


def extractAssistData():
	with open("Play_by_Play_data_csv.csv", "r") as csvfile:
		with open("assist_data_csv.csv", "w", newline='') as destfile:
			datareader = csv.reader(csvfile)
			datawriter = csv.writer(destfile)
			datawriter.writerow(next(datareader))
			for row in datareader:
				print(row[0])
				if (row[3] == '1'):
					datawriter.write(row)


def extractAssistDataYear(year):
	with open("assist_data_csv.csv", "r") as csvfile:
		with open("assist_data_" + str(year) + "_csv.csv", "w", newline='') as destfile:
			datareader = csv.reader(csvfile)
			datawriter = csv.writer(destfile)
			datawriter.writerow(next(datareader))
			for row in datareader:
				if len(row) > 2:
					if row[1][1:3] == str(year):
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


def parseAssistDescription(description):
	try:
		right_bracket = description.index("]")
		message = description[right_bracket + 2:]
		p1 = message.split(" ")[0]
		p2 = message.split("Assist: ")[1].split(" ")[0]
		return p2, p1
	except:
		print(description)


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

def getTeamName(desc, assist=False):
	left_bracket = desc.index("[")
	right_bracket = desc.index("]")
	if not assist:
		teamName = desc[left_bracket + 1: right_bracket]
	else:
		teamName = desc[left_bracket + 1: left_bracket + 4]
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


def getAssistDict(filename, outname):
	with open(filename, 'r') as infile:
		teams = {}
		datareader = csv.reader(infile)
		for row in datareader:
			if "Assist: " not in row[4]:
				continue
			team = getTeamName(row[4], assist=True)
			if team not in teams:
				teams[team] = {}
			p1, p2 = parseAssistDescription(row[4])
			if p1 not in teams[team]:
				teams[team][p1] = {}
			if p2 not in teams[team][p1]:
				teams[team][p1][p2] = 0
			teams[team][p1][p2] += 1
	saveToJson(teams, outname)


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


if __name__ == '__main__':
	# extractAssistDataYear("18")
	getAssistDict("assist_data_18_csv.csv", "assist_18.json")
	# extractSubstitutionDataYear("18")
	# getSpurs()
	# getAllTeams18()
	# parseDescription("(6:07)[SAS] White Substitution replaced by Mills", '1610612756')