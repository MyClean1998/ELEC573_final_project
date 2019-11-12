import csv
import json
from itertools import dropwhile, takewhile
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

teams = ['PHI', 'BOS', 'GSW', 'OKC', 'CHA', 'MIL', 'DET', 'BKN', 'MEM', 'IND', 'MIA', 'ORL', 'ATL', 'NYK', 'TOR', 'CLE',
				 'HOU', 'NOP', 'SAS', 'MIN', 'SAC', 'UTA', 'LAC', 'DEN', 'PHX', 'DAL', 'CHI', 'WAS', 'POR', 'LAL']

def read_json(team):
	with open("sub_18.json") as json_file:
		data = json.load(json_file)
		dict = {}
		for p in data[team]:
			dict[p] = data[team][p]
		# print(dict)
		return dict

def createGraph(dict, thres=20):
	G = nx.DiGraph()
	for key in dict:
		G.add_node(key, name=key)
		iso = False
		for v in dict[key]:
			if dict[key][v] > thres:
				G.add_edge(key, v, weight=dict[key][v])
				iso = True
		if not iso:
			G.remove_node(key)
	# # print(G.in_degree)
	return G

def showGraph(g, team):
	labels = {p: p for p in g.nodes}
	options = {
		# 'node_color': 'black',
		'node_size': 100,
		# 'width': 3,
		'labels': labels,
	}
	plt.figure()
	nx.draw_kamada_kawai(g, **options)
	# nx.draw(g, **options)
	plt.savefig(team + '.png')
	# plt.show()

# g = createGraph(read_json("PHI"))
# showGraph(g, "PHI")


# for team in teams:
# 	showGraph(createGraph(read_json(team)), team)

def getTeams():
	with open("sub_18.json") as json_file:
		teams = []
		data = json.load(json_file)
		for k in data:
			teams.append(k)
		print(teams)

def centrality_analysis(team):
	if team == "all":
		clusterings = []
		for t in teams:
			clusterings.append(nx.transitivity(createGraph	(read_json(t), 10)))
		fig = plt.figure()
		ax = fig.add_axes([0,0,1,1])
		ax.bar(teams, clusterings)
		ax.set_xticks(np.arange(30), teams)
		ax.set_xticklabels(teams, rotation = 45)

		plt.show()
		# centrality_analysis(t)
	else:
		g = createGraph	(read_json(team), 10)
		degrees = [d for e, d in g.degree]
		betweenness = [b for b in nx.betweenness_centrality(g, weight="weight").values()]
		clustering = [c for c in nx.clustering(g, weight="weight").values()]
		# print("average degree: ", sum(degrees) / float(len(degrees)))
		# print("average betweenness: ", sum(betweenness) / float(len(betweenness)))
		# print("average clustering: ", sum(clustering) / float(len(clustering)))

		print(sorted(g.degree, key=lambda t: t[1], reverse=True))
		print(sorted(nx.betweenness_centrality(g, weight="weight").items(), key=lambda t: t[1], reverse=True))
		print(sorted(nx.clustering(g, weight="weight").items(), key=lambda t: t[1], reverse=True))

		# plt.hist(degrees, bins=int(max(degrees) - min(degrees)))
		# plt.show()
		# plt.hist(betweenness, normed=True)
		# plt.show()
		# plt.hist(clustering, normed=True)
		# plt.show()
# def node_with_highest_centrality(g):

# getTeams()
# centrality_analysis("SAS")
centrality_analysis('all')